from passlib.context import CryptContext


# 密码加密上下文，使用 bcrypt 算法进行密码哈希处理
pwd_context =  CryptContext(schemes=["bcrypt"], deprecated="auto")

# 定义一个函数来加密密码，接受一个明文密码作为输入，并返回加密后的哈希值
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 定义一个函数来验证密码，接受一个明文密码和一个已加密的哈希值作为输入，并返回布尔值表示是否匹配
def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
