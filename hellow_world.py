"""
fastapi 基础
	模型定义
	接口使用
"""

import json
from typing import List, Optional

from pydantic import BaseModel
from fastapi import FastAPI

class CityInfo(BaseModel):
	province: str
	country: str
	is_anran: Optional[bool] = None
	

my_app = FastAPI()

@my_app.get('/')
async def hollew_world():
	return {'hellow': 'world'}


@my_app.get('/city/{city_parse}')
async def city_info(city_parse: str, parse_data: Optional[str] = None):
	return json.dumps({
		"city": city_parse,
		"parse data": parse_data
	})
	
@my_app.put('/city/{parse_city}')
async def put_city_data(parse_city: str, city_info: CityInfo):
	return {
		'city': parse_city,
		'country': city_info.country,
		'is_ganran': city_info.is_anran,
		'provice': city_info.province
	}