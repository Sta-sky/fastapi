import secrets
import string
import time

import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional

def gengate_secret_key():
	sinum = string.ascii_letters + string.digits
	passwd = ''.join(secrets.choice(sinum) for i in range(50))
	return passwd
app_06 = APIRouter()

oauth2_schema = OAuth2PasswordBearer('/chapter_06/token') # 请求token的url 127.0.0.1:7000/chapter_06/token
JWT_TOKEN_KEY = 'vUM7EfC9YvMAqY7oGiTkgYlUdsr4MZL9a2vVcH3ulbV57WrOXL'

"""
OAuth2PasswordBearer 是接收URL作为参数的一个类 客户端回向该 url 发送 username。 password参数， 然后得到一个token值
OAuth2PasswordBearer 并不会创建相应的url路径操作， 只是指明客户端用来请求token的URl地址
当请求来到时 FastApi会检测 Authorization头信息，如果没有找到 Authorization头信息， 或者头信息 不是Bearer token 他会返回401状态码UNAUTHORIZED

"""

# 基于Password 和 Bearer token的 oauth2认证

fake_user_db = {
	'张三': {
		'username': '张三',
		'full_name': '张三',
		'email': 'zhangsan@zhunda.com',
		'hash_password': 'fakehashsecret1',
		'disabled': False
	},
	'李四': {
		'username': '李四',
		'full_name': '李四',
		'email': 'lisi@zhunda.com',
		'hash_password': 'fakehashsecret2',
		'disabled': True
	}
}

class UserInfo(BaseModel):
	username: str
	full_name: Optional[str] = None
	email: EmailStr
	disabled: Optional[bool] = None
	
class UserAllInfo(UserInfo):
	hash_password: str

@app_06.post('/token')
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
	info = form_data.__dict__
	username = form_data.username
	password = form_data.password
	user = get_user(fake_user_db, username)
	if not user or fask_password(password) != user.hash_password:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='username == or password is wrong')
	token = make_token(user.username)
	response = {
		'access_token': token,
		'token_type': 'bearer',
		'dic_info': info
	}
	return response

def get_user(db, username):
	""" 获取所有用户 """
	if username in db:
		user_dict = db[username]
		users = UserAllInfo(**user_dict)
		return users
	else:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user not fount')
	
def fask_password(password: str):
	return 'fakehash' + password

def make_token(username, exp=3600 * 24):
	""" 创建token """
	key = JWT_TOKEN_KEY
	now = time.time()
	payload = {'username': username, 'exp': exp + now}
	return jwt.encode(payload=payload, key=key, algorithm='HS256')

def fake_decode_token(token: str):
	""" 解码token """
	try:
		username = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
	except Exception as e:
		print(e)
		return None
	user = get_user(fake_user_db, username.get('username'))
	return user

@app_06.get('/get_current_user')
async def get_current_user(request: Request, id: int, token: str = Depends(oauth2_schema)):
	user = fake_decode_token(token)
	dic = user.dict()
	dic.update({'header': request.headers.get('authorization')})
	dic.update({'token': token})
	dic.update({'id': id})
	if user:
		return dic
	else:
		return {'status': 400}
