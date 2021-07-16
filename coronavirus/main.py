"""
	项目入口
"""
from fastapi import Depends, HTTPException, status, Request, APIRouter
from fastapi.templating import Jinja2Templates
from typing import Optional
from coronavirus.database import database_engine, Base, SessionLocal
from coronavirus import schemas, crud
from sqlalchemy.orm import Session


async def get_user_agent(reqest: Request):
	print({'user-agent': reqest.headers['User-Agent']})
	

app_coronavirus = APIRouter(
	# prefix='/big_application',
	dependencies=[Depends(get_user_agent)]
)

# jinja2模板配置
# templates = Jinja2Templates(directory='模板相对于run.py的相对位置')
templates = Jinja2Templates(directory='./coronavirus/templates')

# 创建数据库
Base.metadata.create_all(bind=database_engine)

# 创建会话
async def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
		
@app_coronavirus.post('/create/city')
async def create_city(city_info: schemas.CreateCity, db: Session = Depends(get_db)):
	""" 创建城市的数据 """
	city = crud.get_city_by_name(db=db, city_name=city_info.province)
	if city:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='City information already exists')
	city = crud.create_city(db=db, city=city_info)
	return {'status code': status.HTTP_200_OK, 'succeed': True, 'info': city}


@app_coronavirus.post('/create/data')
async def create_data(data_info: schemas.CreateData, city_id: int, db: Session = Depends(get_db)):
	""" 上传病毒的数据 """
	data = crud.create_city_data(db=db, data=data_info, city_id=city_id)
	if not data:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='create data failed')
	return {'status code': status.HTTP_200_OK, 'succeed': True}


@app_coronavirus.get('/get_city', response_model=schemas.ResponseCity)
async def get_city(
		city_id: Optional[int] = None,
		city_name: Optional[str] = None ,
		db: Session = Depends(get_db)):
	
	""" 根据城市 id / name 获取城市信息 """
	if not city_id and not city_name:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='query param is wrong')
	if city_id:
		data = crud.get_city_by_id(db=db, city_id=city_id)
	else:
		data = crud.get_city_by_name(db=db, city_name=city_name)
	if data is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='city is not found')
	return data


@app_coronavirus.get('/get_data', response_model=schemas.ResponseData)
async def get_data(city_name: str, db: Session = Depends(get_db)):
	""" 获取单个城市的数据 """
	if not city_name:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='query param is wrong')
	data = crud.get_city_data_by_choice(db=db, city_name=city_name)
	return data


@app_coronavirus.get('/start_end_data')
async def start_end_data(start: int = 0, end: int = 10, db: Session=Depends(get_db)):
	""" 自定义 获取数据数量， 分页处理 """
	return crud.get_city_data_by_choice(db=db, start=start, end=end)


# 前后端不分离的模板接口
@app_coronavirus.get('/')
async def get_template_data(request: Request, city_name: str = None, start: int = 0, end: int = 10, db: Session = Depends(get_db)):
	data = crud.get_city_data_by_choice(db=db, city_name=city_name, start=start, end=end)
	print(data)
	if not data:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='City Info Not Found')
	return templates.TemplateResponse(
		'home.html',
		{
			'request': request,
			'data': data,
			'sycn_data_url': '/coronavirus/sync_coronavirus_data/jhu'
		}
	)

