import jwt


SECRET_KEY = 'buibbiikb4hyy2cg4cx4cjxuj4v1xcxd'
ALGO_JWT = "HS256"

def add_prefix(token):
    return f'Bearer {token}'

def remove_prefix(token):
    return token.replace('Bearer ', '')

# 유저 정보[user_list] 정보를 이용해서 JWT 생성.
def make_token(result):
    return jwt.encode(result, SECRET_KEY, algorithm=ALGO_JWT)

# JWT를 해독해서 로그인 주체의 유저 정보[user_list] 정보를 추출.
def decode_token(token):
    token_extracted = remove_prefix(token)
    try:
        return jwt.decode(token_extracted, SECRET_KEY, algorithms=[ALGO_JWT])
    except jwt.ExpiredSignatureError:
        print("Token expired")
    except jwt.InvalidTokenError:
        print("Invalid token")
    