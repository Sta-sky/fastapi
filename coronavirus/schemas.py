"""
	基于pydantic 的响应数据格式
"""
from datetime import datetime, date
from pydantic import BaseModel


class CreateData(BaseModel):
	data_date: date
	confirmed: int = 0
	deathed: int = 0
	recovered: int = 0


class CreateCity(BaseModel):
	province: str
	country: str
	country_code: str
	country_population: int

class ResponseData(CreateData):
	id: int
	city_id: int
	create_time: datetime
	update_time: datetime

	class Config:
		orm_mode = True


class ResponseCity(CreateCity):
	id: int
	create_time: datetime
	update_time: datetime

	class Config:
		orm_mode = True
