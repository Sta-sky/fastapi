"""
	项目入口
"""
from fastapi import Depends, HTTPException, status, Request, APIRouter, BackgroundTasks
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import HttpUrl
from coronavirus.database import database_engine, Base, SessionLocal
from coronavirus import schemas, crud
from sqlalchemy.orm import Session

from coronavirus.models import City, Data
from coronavirus.utils import return_requests_data


async def get_user_agent(reqest: Request):
    return {'user-agent': reqest.headers['User-Agent']}


app_coronavirus = APIRouter(
    prefix='/big_application',
    dependency_overrides_provider=[Depends(get_user_agent)]
)

# jinja2模板配置
# templates = Jinja2Templates(directory='模板相对于run.py(主程序入口)的相对位置')
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
        city_name: Optional[str] = None,
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
async def start_end_data(start: int = 0, end: int = 10, db: Session = Depends(get_db)):
    """ 自定义 获取数据数量， 分页处理 """
    return crud.get_city_data_by_choice(db=db, start=start, end=end)


# 前后端不分离的模板接口
@app_coronavirus.get('/')
async def get_template_data(request: Request, city_name: str = None, start: int = 0, end: int = 1000,
                            db: Session = Depends(get_db)):
    data = crud.get_city_data_by_choice(db=db, city_name=city_name, start=start, end=end)
    return templates.TemplateResponse(
        'home.html',
        {
            'request': request,
            'data': data,
            'sycn_data_url': '/coronavirus/big_application/sync_coronavirus_data/jhu'
        }
    )


def tasks(url: HttpUrl, db: Session):
    """ 不要再后台任务中导入依赖 db: Session = Depends(get_db) """
    print('数据开始请求...')
    city = return_requests_data(param_url=f'{url}?source=jhu&country_code=CN&timelines=false')
    print(city)
    print('开始同步 城市 数据...')
    if city.status_code == 200:
        city_obj = db.query(City)
        city_obj.delete()
        for location in city.json()['locations']:
            province = location['province']
            population = location['country_population']
            if not population:
                population = 0
            city_info = {
                'province': province,
                'country': location['country'],
                'country_code': location['country_code'],
                'country_population': population
            }
            crud.create_city(db=db, city=schemas.CreateCity(**city_info))

    print('请求详细数据...')
    data = return_requests_data(param_url=f'{url}?source=jhu&country_code=CN&timelines=true')
    print('同步详细数据...')
    if data.status_code == 200:
        data_obj = db.query(Data)
        data_obj.delete()
        for city_ in data.json()['locations']:
            db_city = crud.get_city_by_name(db, city_name=city_['province'])
            for date, confirmed in city_['timelines']['confirmed']['timeline'].items():
                data_info = {
                    'data_date': date.split('T')[0],
                    'confirmed': confirmed,
                    'deathed': city_["timelines"]["deaths"]["timeline"][date],
                    'recovered': 0
                }
                crud.create_city_data(db=db, data=schemas.CreateData(**data_info), city_id=db_city.id)
    print('所有数据同步完成')


@app_coronavirus.get('/sync_coronavirus_data/jhu')
async def get_source_data(back_end: BackgroundTasks, db: Session = Depends(get_db)):
    print("开始")
    back_end.add_task(tasks, 'https://coronavirus-tracker-api.herokuapp.com/v2/locations', db)
    print("结束")
    return {'info': 200, 'message': '数据正在后台同步中.....'}
