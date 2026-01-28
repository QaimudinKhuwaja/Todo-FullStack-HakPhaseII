from passlib.context import CryptContext

# Configuration for password hashing
# We use bcrypt for hashing, which is a good default choice
# Check https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html for more options
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a plain password using the configured CryptContext.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password using the configured CryptContext.
    """
    return pwd_context.verify(plain_password, hashed_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password using the configured CryptContext.
    """
    return pwd_context.verify(plain_password, hashed_password)

