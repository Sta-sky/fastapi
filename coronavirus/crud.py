"""
	数据库操作
"""
from sqlalchemy.orm import Session

from . import models, schemas


def get_city_by_id(db: Session, city_id: int):
	""" 根据 id 获取城市信息"""
	data = db.query(models.City).filter(models.City.id == city_id).first()
	return data


def get_city_by_name(db: Session, city_name: str):
	""" 根据 name 获取城市信息"""
	return db.query(models.City).filter(models.City.province == city_name).first()


def get_many_city(db: Session, start: int = 0, ends: int = 10):
	""" 根据 数据条数 获取城市信息"""
	city_data = db.query(models.City).offset(start).limit(ends).all()
	return city_data


def create_city(db: Session, city: schemas.CreateCity):
	db_dict = models.City(**city.dict())
	db.add(db_dict)
	db.commit()
	db.refresh(db_dict)
	return db_dict


def get_city_data_by_choice(db: Session, city_name: str = None, start: int = 0, end: int = 1000):
	if city_name:
		return db.query(models.Data).filter(models.Data.city.has(province=city_name))
	return db.query(models.Data).offset(start).limit(end).all()

def create_city_data(db: Session, data: schemas.CreateData, city_id: int):
	data_dict = models.Data(**data.dict(), city_id=city_id)
	db.add(data_dict)
	db.commit()
	db.refresh(data_dict)
	return data_dict
