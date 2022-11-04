import json
from typing import List, Optional, Tuple

from pydantic import BaseModel, ValidationError,constr
from datetime import datetime
from pathlib import Path
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

class User(BaseModel):
	id: int
	name: str = 'Jone Sonw'
	sinup_ts: Optional[datetime] = None
	firends: List[int]

parse_dic = {
	"id": "123",
	"sinup_ts": str(datetime.now()),
	"firends": [1, 2]
}
user = User(**parse_dic)

print('1 传值方式','++' * 100)
print(user.sinup_ts)
print(repr(user.sinup_ts))
print(type(repr(user.sinup_ts)))
# 字典方式输出
print(user.dict())


print('2 错误捕获','++' * 100)
try:
	users = User(id="12", sinup_ts="23", firends=[12, "2"], name=12 )
	print('==', users.json())
except ValidationError as e:
	print('error', e.json())

print('3 模型类的属性跟方法','++' * 100)
print(user.dict())
print(type(user.dict()))
print(user.json())
print(type(user.json()))

# 解析字典
print('解析字典')
print(User.parse_obj(obj=parse_dic))
# 解析字符串
print('解析字符串')
print(User.parse_raw(
	'{"id": "123", "name": "jone dan", "sinup_ts": "2021-06-23 10:12", "firends": ["12", "23"]}'
))
# 解析文件
path = Path('pydandic.json')
path.write_text(json.dumps(parse_dic))
print(User.parse_file(path))
# 查看类模型中的所有字段
print(user.__fields__.keys())


print('4 递归模型','++' * 100)

class Sound(BaseModel):
	wang: str

class Dog(BaseModel):
	color: str
	age: int
	whight: float = Optional[None]
	sound: List[Sound]
	
	
dog = Dog(color='white', age=1, whight=12.4, sound=[{'wang': 'aaa'}, {'wang': 'bbb'}])
print(dog.dict())


print('5 从类的实例，创建符合ORM模型对象的模型','++' * 100)

# 创建模型类
Base = declarative_base()
class ComPanysORM(Base):
	__tablename__ = 'companys'
	id = Column(Integer, primary_key=True, nullable=False)
	publick_key = Column(String(20), unique=True, nullable=False)
	name = Column(String(25), unique=True)
	domains = Column(ARRAY(String(255)))


class ComPanysModel(BaseModel):
	id: int
	publick_key: constr(max_length=20)
	name: constr(max_length=25)
	domains: List[constr(max_length=255)]
	
	class Config:
		orm_mode = True
		
orm_c = ComPanysORM(
	id = "1",
	publick_key = 'frewbgsf&(&)_)',
	name = '黄不够发达发达',
	domains = ['baidu.com', 'aliyun.com']
)

print("模型")
try:
	print(ComPanysModel.from_orm(orm_c))
except Exception as e:
	print(str(e))
	




