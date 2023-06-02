from passlib.context import CryptContext

# Create a CryptContext object with the desired hash algorithm(s)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"])


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)