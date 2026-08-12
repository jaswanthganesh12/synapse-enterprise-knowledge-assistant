from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai.generator import generate_answer
from app.auth.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.services.citation_service import build_citations
from app.services.context_service import build_context
from app.services.hybrid_search_service import hybrid_search
from app.chat.schemas import ChatRequest, ChatResponse


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
    results = hybrid_search(
        db=db,
        query=request.query,
        user_id=current_user.id,
        limit=5,
    )
    if not results:
        return ChatResponse(
        answer="I couldn't find any relevant information in your accessible documents.",
        citations=[],
    )

    context = build_context(results)

    answer = generate_answer(
        query=request.query,
        context=context,
    )

    citations = build_citations(results)

    return ChatResponse(
        answer=answer,
        citations=citations,
    )