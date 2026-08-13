from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.generator import generate_answer
from app.auth.dependencies import get_current_user
from app.chat.schemas import ChatRequest, ChatResponse
from app.db.dependencies import get_db
from app.models.user import User
from app.services.citation_service import build_citations
from app.services.context_service import build_context
from app.services.conversation_service import (
    add_message,
    get_recent_messages,
    get_user_conversation,
)
from app.services.hybrid_search_service import hybrid_search


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Verify conversation ownership
    conversation = get_user_conversation(
        db=db,
        conversation_id=request.conversation_id,
        user_id=current_user.id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    # 2. Load previous conversation messages
    messages = get_recent_messages(
        db=db,
        conversation_id=conversation.id,
        limit=10,
    )

    conversation_history = "\n".join(
        f"{message.role.upper()}: {message.content}"
        for message in messages
    )

    # 3. Save current user message
    add_message(
        db=db,
        conversation_id=conversation.id,
        role="user",
        content=request.query,
    )

    # 4. Perform hybrid RAG search
    results = hybrid_search(
        db=db,
        query=request.query,
        user_id=current_user.id,
        limit=5,
    )

    # 5. Handle no relevant results
    if not results:
        answer = (
            "I couldn't find any relevant information "
            "in your accessible documents."
        )

        add_message(
            db=db,
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
        )

        return ChatResponse(
            answer=answer,
            citations=[],
        )

    # 6. Build retrieved context
    context = build_context(results)

    # 7. Generate grounded answer using conversation history
    answer = generate_answer(
        query=request.query,
        context=context,
        conversation_history=conversation_history,
    )

    # 8. Save assistant response
    add_message(
        db=db,
        conversation_id=conversation.id,
        role="assistant",
        content=answer,
    )

    # 9. Build citations
    citations = build_citations(results)

    return ChatResponse(
        answer=answer,
        citations=citations,
    )