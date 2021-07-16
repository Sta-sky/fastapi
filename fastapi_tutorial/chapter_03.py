# -*- coding: utf8 -*-
from typing import Optional, List

from fastapi import APIRouter, Path, Query, Cookie, Header, Request
from enum import Enum
from datetime import date
from pydantic import BaseModel, Field

"""
	路径参数校验，使用 Path 类
	查询参数校验，使用 Query 类
	pydantic 参数校验，使用 Field 类
"""

app_03 = APIRouter()

# 1、基础路径
@app_03.get('/index/{info}')
def index_03_path(info: str):
	return {'Message': info, 'code': 200}

# 2、枚举类型参数传递
class CityName(str, Enum):
	beijing = 'beijing china'
	shanghai = 'shanghai china'

@app_03.get('/city/{parse_city}')
def get_city(parse_city: str):
	if parse_city == CityName.beijing:
		return {'city': parse_city, 'person': '1242', 'death': 8}
	if parse_city == CityName.shanghai:
		return {'city': parse_city, 'person': '1542', 'death': 4}
	return {'city': parse_city, 'parse': 'error'}


# 3、文件路径 验证
@app_03.get('/base_path/{file_path:path}')
def file_path_parse(file_path: str):
	return {'curr_file_path': file_path}

# 4、数字参数的验证
@app_03.get('/num_path/{num}')
def path_num(
		num: int = Path(..., title='num_title', ge=1, le=10)):
	return num

# 5、查询参数选填
@app_03.get('/query_parse/')
def query_parse(page: int = 1, limit: Optional[int] = None):
	if limit:
		return {'page': page, 'limit': limit}
	return {'query parse': page}

# 6、bool参数验证
@app_03.get('/bool_parse')
def bool_parse_verfer(parmse: bool):
	"""
	    当 parmse ==
	        Ture ture 1 yes on 都表示 ture
	        FLALSE， false，no 0  都表示
	"""
	if parmse:
		return True
	return False

# 7、字符串的验证
@app_03.get('/verify_str')
def verfiry_str(
		parse_str: str = Query(..., max_length=5, min_length=1, regex='^a'),
		parse_list: List[str] = Query(default=['val_1', 'val_2'], alias='alias_name')
):
	return {'Message_1': parse_str, 'Message_2': parse_list}

# 8、请求体和字段
class CityInfo(BaseModel):
	name: str = Field(..., example='Beijing')
	country: str
	country_code: Optional[str] = None
	country_peprson: int = Field(..., title='人口数量', description='国家的人口数量', ge=800)

	class Config:
		schema_extra = {
			'example': {
				'name': 'BeiJing',
				'country': 'China',
				'country_code': 'CN',
				'country_peprson': 140000000
			}
		}
		
@app_03.post('/city/city_info')
def request_body(info: CityInfo):
	return info.dict()

# 9、多种请求混合解析  路径参数  请求体参数  查询参数
@app_03.post('/all_parse/{city_name}')
def all_parse(
	city_name: str,
	city_info_01: CityInfo,
	city_info_02: CityInfo,  # body 类型参数是可以定义多个的
	confreamed: int = Query(default=0, title='确诊人数', ge=0),
	death: int = Query(default=0, ge=0, title='死亡人数')):
	if city_name == 'beijing':
		return {'beijing': {
				'city_name' : city_name,
				'city_info': city_info_01.dict(),
				'city_info_02': city_info_02.dict(),
				'confremed': confreamed,
				'death': death
			}}
	
# 10、数据格式嵌套的请求体

class Data(BaseModel):
	city: List[CityInfo]
	date: date
	confirmed: int = Field(default=0, ge=0, title='确诊人数')
	deaths: int = Field(default=0, ge=0, title='死亡人数')
	recovered: int = Field(default=0, ge=0, title='治愈人数')

@app_03.put('/model_data')
def data_model(data: Data):
	return data.dict()

# 11 获取Cookie 跟 Header参数

@app_03.get('/cookie')
def get_cookie(cookie_id: Optional[str] = Cookie(None)):
	return {'cookie_id': cookie_id}

@app_03.get('/header')
def header_get(
		request: Request,
		cookie: Optional[str] = Header(None, convert_underscores=True),
		x_token: List[str] = Header(None)
):
	print(request.headers)
	for item in request.headers.items():
		print(item)
	return {'User-Agent': cookie, 'x_token': x_token, 'request': request.headers}
