

## fastai

1、asgi：

2、wsgi：



##### ASGI服务：

###### 三种ASGI服务：

**1、Uvicorn**

**2、Hypercorn**

**3、Daphne**

----------



## 1、请求参数和验证

**所在文件路径  ../chapter_03.py**

####  1、参数解析

```python

注意：
	"""
        路径参数校验，使用 Path 类
        查询参数校验，使用 Query 类
        pydantic 参数校验，使用 Field 类
        
        Path(...,), Path(default='test')
        Query(...,), Query(default='test')
        Field(...,), Field(default='test')
        注：
        	...      表示 此字段必填
        	default  表示 此字段有默认值， 非必填字段
    """
```

###### 1、基础路径

###### 2、枚举类型参数传递

###### 3、文件路径 验证

###### 4、数字参数的验证

###### 5、查询参数选填

###### 6、bool参数验证

######  7、字符串的验证

###### 8、请求体和字段

###### 9、多种请求混合解析  路径参数  请求体参数  查询参数

######  10、数据格式嵌套的请求体

###### 11 获取Cookie 跟 Header参数

--------------



## 2、响应处理处理和fastapi配置

**所在文件路径  ../chapter_04.py**

#### 1、响应模型

~~~python
所在文件路径  ../chapter_04.py

@app_04.post('/union_response_model',
             # response_model=Union[UserIn, UserOut],
             response_model = List[UserOut],
             response_model_include = ['username', 'email'],
			 response_model_exclude = ['password']
             )
async def union_response(user: UserIn):
    
	"""
		response_model_exclude_unset:   设置有默认值，或可选参数  用户未传进来时 不返回
		response_model: 				设置响应体模型
		Union: 							取响应模型的并集
		List:  							可响应多个 符合 UserOut 模型的 数据
		response_model_include：		   包含那些响应字段
		response_model_exclude： 	   排除那些响应字段
	:param user:  						请求体验证模型
	:return:
	"""

~~~



#### 2、状态码定义

~~~python
from fastapi import status

# 3、状态码的调用
@app_04.get('/status')
async def status_code():
	return {'status code': 200}

@app_04.get('status_attribute')
async def status_attribute():
	return {'status code': status.HTTP_200_OK}

~~~



#### 3、表单数据处理

~~~python
# 4、表单数据处理
@app_04.post('/login')
async def login(username:str = Form(..., min_length=5), password: str = Form(..., max_length=10)):
	return {'username': username, 'password': password}


# 5、body 数据处理
@app_04.post('/body_handle')
async def body_handle(
		username: str = Body(..., title='用户名'),
		password: str = Body(...,),
		body_info: str = Body(...)
):
	return {
		'body_info': body_info,
		'user_name': username,
		'password': password,
		'status code': status.HTTP_200_OK
	}

~~~



#### 4、单文件、多文件上传、及参数处理



~~~python
 
# 上传单个文件 、小文件
file: bytes = File(...)

# 上传多个文件
files: List[bytes] = File(...,)

# 上传视频、大文件  UploadFile
files: List[UploadFile] = File(...)
    

~~~

#### 5、静态文件的配置

~~~python
app_main.mount(path='/static', app=StaticFiles(directory='./static'))
~~~



#### 6、自定义应用配置

~~~python
 app_main = FastAPI(
	title='my_fastapi',
	description='first fastapi app - 我的第一个fastapi应用',
	version='1.0.1',
	docs_url='/docs'
)

~~~



#### 7、框架错误处理

~~~python
# 7、框架错误处理
@app_04.get('/http_exception')
async def http_exception(city: str):
	if city != 'beijing':
		raise HTTPException(status_code=status.HTTP_200_OK,
		                    detail='city error',
		                    headers={'X-Error': 'Error'})
	return {'city': city}

~~~



----





## 3、fastapi的依赖注入系统

**所在文件路径  ../chapter_05.py**

#### 1、什么是依赖注入：

~~~python
依赖注入，是为了实现类似于django框架的类视图的功能，
作用：
	1、为了提高代码的复用率
    2、共享数据库连接
    3、增强安全、认证、角色管理 
~~~

#### 2、兼容性

~~~python
1、支持所有的关系型数据库，支持Nosql数据库
2、第三方的包和api
3、认证和授权系统
4、响应数据注入系统	
~~~



#### 3、创建声明导入依赖

##### 1、将函数作为依赖项

###### 1、可在异步的函数中调用  同步的依赖

~~~python
    # 同步函数
    def comment_parse(q: Optional[str] = None, page: int = 1, limit: int = 100):
        return {'page': page, 'limit': limit, 'parse': q}

    # 异步函数
    @app_05.get('/dependence_01', summary='01')
    async def dependency01(comments: dict = Depends(comment_parse)):
        return comments

~~~

###### 2、也可在同步的函数中调用  异步的依赖

~~~python
 	# 异步函数
    async def comment_parse(q: Optional[str] = None, page: int = 1, limit: int = 100):
        return {'page': page, 'limit': limit, 'parse': q}
	
    # 同步函数
    @app_05.get('/dependence_02', summary='02')
    def dependency02(comments: dict = Depends(comment_parse)):
        return comments

~~~

##### 2、将类作为依赖项

~~~python

fake_data_sql = [{'name_item': 'Bar'}, {'name_item': 'Lienda'}, {'name_item': 'Loc'}]


class DependencyClass:
	def __init__(self, q: Optional[str] = None, page: int = 1, limit: int = 100):
		self.q = q
		self.page = page
		self.limit = limit


@app_05.get('/class_dependency')
async def class_dependency(comment=Depends(DependencyClass)):
	response = {}
	if comment.q:
		response.update({'q': comment.q})
	items = fake_data_sql[comment.page: comment.page + comment.limit]
	response.update({'name item': items})
	return response


~~~

##### 3、子依赖

~~~python
def query(q: Optional[str] = None):
	return q

def sub_query(q: str = Depends(quer), last_q: str = 'test last q'):
	if not q:
		return last_q
	return q

@app_05.get('/sub_dependency')
async def sub_dependency(query_parse: str = Depends(sub_query, use_cache=True)):
	""" use_cache 表示当多个依赖有同一个子依赖时， 每次request请求只会调用一次子依赖 提升性能"""
	return {'quesy_parse': query_parse}
	

~~~



##### 4、路径操作中装饰器的多依赖  

**作用**：

​	**在进入视图函数之前可进行参数验证**

~~~python
# 路径操作中的 多依赖
async def verify_token(x_token: str = Header(...)):
	if x_token != 'user-agent-token':
		raise HTTPException(status_code=400, detail='X-Token is valid')
	return x_token

async def verify_key(x_key: str = Header(...)):
	if x_key != 'user-agent-key':
		raise HTTPException(status_code=400, detail='X-Key is valid')
	return x_key

@app_05.get('/many_dependency', dependencies=[Depends(verify_token), Depends(verify_key)])
async def many_dependency():
	return {'status': 200}
~~~



##### 5、全局依赖

###### 1、主程序设置依赖： 所有应用都可使用

~~~python
app_main = FastAPI(
	dependencies=dependencies=[Depends(verify_token), Depends(verify_key)]
)

~~~

###### 2、单个应用设置依赖：

~~~python
app_05 = APIRouter(dependencies=dependencies=[Depends(verify_token), Depends(verify_key)])

~~~

----------



### 4、安全、认证、授权



##### 1、授权码授权模式

##### 2、隐式授权模式

##### 3、密码授权模式

~~~python
1、指定token请求的地址:
    
     # 请求token的url 127.0.0.1:7000/chapter_06/token
    oauth2_schema = OAuth2PasswordBearer('/chapter_06/token') 

2、登录验证 签发token ：

	@app_06.post('/token')
    async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
        username = form_data.username
        password = form_data.password
        user = get_user(fake_user_db, username)
        if not user or fask_password(password) != user.hash_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='username == or password is wrong'
            )
        token = make_token(user.username)
        response = {
            'access_token': token.decode(),
            'token_type': 'bearer'
        }
        return response

3、使用 token 获取数据，获取数据前验证token是否有效：
	@app_06.get('/get_current_user')
    async def get_current_user(
        request: Request,
        token: str = Depends(oauth2_schema)
    ):
        user = fake_decode_token(token)
        dic = user.dict()
        dic.update({'header': request.headers.get('authorization')})
        dic.update({'token': token})
        if user:
            return dic
        else:
            return {'statuc': 400}

   
~~~



##### 4、客户端凭证授权模式



### 5、fastapi的数据库操作和多应用的目录结构设计

##### 1、配置数据库

**database.py**

~~~python
"""
	数据库配置
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库连接
# 1、配置数据库，
#   连接mysql/postgresql的格式  mysql://username:password@ip:port/database_name
#   sqlite3的格式  sqllite:///./database_name.sqllite3
DATABASE_URL = 'mysql+pymysql://root:123456@127.0.0.1:3306/coronavirus'


database_engine = create_engine(
	DATABASE_URL, # 数据库连接地址
	encoding = 'utf-8',
	# echo = True  # 表示引擎将用repr()函数 记录操作日志
)

# 在sqlalchemy中  数据库操作crud 是通过session会话进行的， 每一个session就是一个数据库连接
# 创建会话
SessionLocal = sessionmaker(
	bind=database_engine, # 绑定引擎
	autoflush=False,
	autocommit=False,
	expire_on_commit=True
)


# 创建基本的映射类
Base = declarative_base(bind=database_engine, name='Base')
~~~

##### 2、创建数据库连接对象，及创建返回数据库操作对象

**main.py**

~~~python
from coro_navirus_app.database import database_engine, Base, SessionLocal

app_coronavirus = FastAPI(
	title='Coronavirus Project'
)

# 创建数据库
Base.metadata.create_all(bind=database_engine)

# 创建会话
async def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
~~~



##### 3、创建数据库模型

**models.py**

~~~python
"""
	数据库模型
"""
from sqlalchemy import Column, String, Integer, BigInteger, Date, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

# 导入数据库模型
from .database import Base

# 构建模型

class City(Base):
	__tablename__ = 'city' # 表名
	id = Column(
		Integer, # 整数类型
		primary_key=True, # 设为主键
		index=True, # 设置索引
		autoincrement=True) # 设置自增长
	province = Column(
		String(100), # 字符串类型  设置长度100
		unique=True, # 省份唯一
		nullable=False, # 不能为空
		comment='省份或者直辖市', # 注解
	)
	country = Column(String(100), nullable=False, comment='国家')
	country_code = Column(String(100), nullable=False, comment='国家代码')
	country_population = Column(BigInteger, nullable=False, comment='国家人口')
	
	# Data是指关联的类名， back_populates 来指定反向访问的属性名。
	data = relationship('Data', back_populates = 'city')
	create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
	update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
	
	# 排序
	__mapper_args__ = {'order_by': country_code} # 默认是正序的  想要倒叙的时候 添加  country_code.desc()
	
	def __repr__(self):
		return f'{self.country}_{self.province}'
	
class Data(Base):
	__tablename__ = 'data'
	id = Column(Integer, primary_key=True, index=True, autoincrement=True) # 设置自增长
	# 设置外键  ForeignKey中 不是 类名.属性名  而是 表名.字段名
	city_id = Column(Integer, ForeignKey('city.id'), comment='所属省/直辖市')
	data_date = Column(Date, nullable=False, comment='数据的日期')
	confirmed = Column(BigInteger, default=0, nullable=False, comment='确诊数量')
	deathed = Column(BigInteger, default=0, nullable=False, comment='死亡数量')
	recovered = Column(BigInteger, default=0, nullable=False, comment='痊愈数量')
	city = relationship('City', back_populates='data')
	create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
	update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
	
	# 排序
	__mapper_args__ = {'order_by': data_date.desc()}  # 默认是正序的  想要倒叙的时候 添加  country_code.desc()
	
	def __repr__(self):
		return f'{repr(self.data_date)} 确诊: {self.confirmed} 例'
~~~



##### 4、pydantic数据响应模型 

**schemas.py**

~~~python
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

~~~

##### 5、数据库增删改查操作

**crud.py**



##### 6、jinjia2模板渲染前端

###### 1、jinja2模板配置

~~~python
from fastapi.templating import Jinja2Templates

# 1、配置
# templates = Jinja2Templates(directory='模板相对于run.py的相对位置')
templates = Jinja2Templates(directory='./templates')

# 2、静态文件配置    directory='模板相对于run.py的相对位置'
    app_main.mount(path='/static', app=StaticFiles(directory='./coronavirus/static'), name='static')
    app_coronavirus.mount(path='/static', app=StaticFiles(directory='./coronavirus/static'), name='static')


# 2、使用

return templates.TemplateResponse(
    'home.html',   ---------------------------- 固定写法  返回的html
    {
        'request': request,	------------------  固定写法 返回 request						
        'data': data,       ------------------  定义返回数据
        'sycn_data_url': '/coronavirus/sync_coronavirus_data/jhu'
    }
)
~~~



###### 2、前端加载数据

~~~html
home.html
~~~



##### 7、多应用的目录结构设计

###### 1、目录结构

~~~python
fastapi:.								----------------主应用
        │  .gitignore
        │  README.md
        │  run.py						----------------主应用入口
        |
        ├─coronavirus					----------------分应用 coronavirus
        │  │  city_details.py			----------------分应用 逻辑操作
        │  │  crud.py					----------------分应用 数据库增删改查
        │  │  database.py				----------------分应用 数据库配置
        │  │  main.py					----------------分应用 初始化
        │  │  models.py					----------------分应用 数据库模型
        │  │  schemas.py				----------------分应用 数据响应格式
        │  │  __init__.py
        │  │
        │  ├─static						----------------分应用 静态文件
        │  │  │
        │  │  └─jquery-3.5.1		
        │  ├─templates					----------------分应用 模板
        │  │      home.html
        ├─doc
        │      fastapi_noet.md
        │
        ├─fastapi_tutorial
        │  │  chapter_03.py				----------------分应用3 初始化
        │  │  chapter_04.py				----------------分应用4 初始化
        │  │  chapter_05.py				----------------分应用5 初始化
        │  │  chapter_06.py				----------------分应用6 初始化
        │  │  chapter_07.py				----------------分应用7 初始化
        │  │  chapter_08.py				----------------分应用8 初始化
        │  │  __init__.py

~~~

###### 2、为分应用添加依赖

~~~python
async def get_user_agent(reqest: Request):
	print({'user-agent': reqest.headers['User-Agent']})
	

app_coronavirus = APIRouter(
	# prefix='/big_application',       #为子应用 app_coronavirus 所有接口路径添加前缀
	dependencies=[Depends(get_user_agent)]  # 为子应用所有接口添加 依赖，进入试图前处理
)

~~~



