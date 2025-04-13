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
	echo = True  # 表示引擎将用repr()函数 记录操作日志
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
Base = declarative_base()

# 绑定引擎到元数据
Base.metadata.bind = database_engine


