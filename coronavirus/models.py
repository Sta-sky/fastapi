"""
	数据库模型
"""
from sqlalchemy import Column, String, Integer, BigInteger, Date, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

# 导入数据库模型
from coronavirus.database import Base

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
	__mapper_args__ = {'order_by': country_code.desc()} # 默认是正序的  想要倒叙的时候 添加  country_code.desc()
	
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