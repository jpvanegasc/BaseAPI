from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


def check_password_hash(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)
