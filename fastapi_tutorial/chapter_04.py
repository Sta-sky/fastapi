from fastapi import APIRouter, status, Form, Body, File, UploadFile, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union
app_04 = APIRouter()

""" Response Model  响应模型 """

class UserIn(BaseModel):
	""" 请求体验证模型 """
	username: str
	password: str
	email: EmailStr
	moblie: str = Field(default=10086, regex='\d+')
	address: str = None
	full_name: Optional[str]

class UserOut(BaseModel):
	""" 响应体模型 """
	username: str
	email: EmailStr
	moblie: str = Field(default=10086, regex='\d+')
	address: str = None
	full_name: Optional[str]


users = {
	'user01': {'username': 'user01', 'password': 123456, 'email': 'user01@test.com', 'full_name': 'china'},
	'user02': {'username': 'user02', 'password': 123456, 'email': 'user02@test.com', 'address': '中国',},
}

# 1、设置响应模型
@app_04.post('/response_model', response_model=UserOut, response_model_exclude_unset=False)
async def response_model_def(user: UserIn):
	"""
		response_model_exclude_unset: 设置有默认值，或可选参数  用户未传进来时 不返回
		response_model: 设置响应体模型
	:param user: 请求体验证模型
	:return:
	"""
	print(user.password)
	return users['user01']

# 2、设置并集响应模型
@app_04.post('/union_response_model',
             # response_model=Union[UserIn, UserOut],
             response_model = List[UserOut],
             response_model_include = ['username', 'email'],
			 response_model_exclude = ['password']
             )
async def union_response(user: UserIn):
	"""
		Union: 取响应模型的并集
		List:  可响应多个 符合 UserOut 模型的 数据
		response_model_include：包含那些响应字段
		response_model_exclude： 排除那些响应字段
	:param user:
	:return:
	"""
	print(user.password)
	# 当不需要返回密码时  删除
	# del user.password
	return [user, user]
	
# 3、状态码的调用
@app_04.get('/status')
async def status_code():
	return {'status code': 200}

@app_04.get('status_attribute')
async def status_attribute():
	return {'status code': status.HTTP_200_OK}


# 4、表单数据处理
@app_04.post('/login')
async def login(username:str = Form(..., min_length=5), password: str = Form(..., max_length=10)):
	return {'username': username, 'password': password}


# 5、body 数据处理
@app_04.post('/body_handle')
async def body_handle(
		username: str = Body(..., title='用户名'),
		password: str = Body(...),
		body_info: str = Body(...)
):
	return {
		'body_info': body_info,
		'user_name': username,
		'password': password,
		'status code': status.HTTP_200_OK
	}

# 6、上传文件处理

# 上传单个文件 、小文件
@app_04.post('/upload_one_file')
async def upload_one_file(file: bytes = File(...)):
	""" 单个小文件 上传，  会写入内存"""
	return {'data': file, 'statuc code': status.HTTP_200_OK, 'len': len(file)}

# 上传多个文件
@app_04.post('/upload_many_file')
async def upload_many_file(files: List[bytes] = File(...,)):
	title_list = [item.title() for item in files]
	content_list = [item for item in files]
	return {
		'file_title': title_list,
		'file_content': content_list,
		'statuc': status.HTTP_200_OK
	}

# 上传视频、大文件  UploadFile
@app_04.post('/upload_big_file')
async def upload_big_file(files: List[UploadFile] = File(...)):
	file_name_list = [item.filename for item in files]
	print(file_name_list)
	for item in files:
		content = await item.read()
		print(content)
	return {
		'statuc_code': status.HTTP_200_OK,
		'file name': file_name_list,
	}


class my_exception(HTTPException):
	def __init__(self):
		super(my_exception, self).__init__()
	

# 7、框架错误处理
@app_04.get('/http_exception')
async def http_exception(city: str):
	if city != 'beijing':
		raise HTTPException(status_code=status.HTTP_200_OK,
		                    detail='city error',
		                    headers={'X-Error': 'Error'})
	return {'city': city}
