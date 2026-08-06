from app.auth.jwt import (
    create_access_token,
    verify_access_token,
)

token = create_access_token(
    {
        "sub": "jaswanth@gmail.com",
        "role": "employee",
    }
)

print("Generated Token:")
print(token)

payload = verify_access_token(token)

print("\nDecoded Payload:")
print(payload)