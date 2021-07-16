"""
	项目入口
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from coronavirus import app_coronavirus
from fastapi_tutorial import app_03, app_04, app_05, app_06, app_07, app_08

app_main = FastAPI(
	title='my_fastapi',
	description='first fastapi app - 我的第一个fastapi应用',
	version='1.0.1',
	docs_url='/docs'
)

# 静态文件配置
app_main.mount(path='/static', app=StaticFiles(directory='./coronavirus/static'), name='static')
app_coronavirus.mount(path='/static', app=StaticFiles(directory='./coronavirus/static'), name='static')

# 重写异常处理器


# 将子应用加入主应用中
app_main.include_router(app_03, prefix='/chapter_03', tags=['第三章，请求参数和验证'])
app_main.include_router(app_04, prefix='/chapter_04', tags=['第四章，响应处理处理和fastapi配置'])
app_main.include_router(app_05, prefix='/chapter_05', tags=['第五章，依赖注入系统'])
app_main.include_router(app_06, prefix='/chapter_06', tags=['第六章，安全、认证、授权'])
app_main.include_router(app_07, prefix='/chapter_07', tags=['第七章，数据库操作，项目目录结构设计'])
app_main.include_router(app_08, prefix='/chapter_08', tags=['第八章，第八章 中间件、CORS、后台任务、测试用例'])
app_main.include_router(app_coronavirus, prefix='/coronavirus', tags=['新冠病毒疫情跟踪器API'])

if __name__ == '__main__':
	uvicorn.run(
		'run:app_main',
		host='127.0.0.1',
		port=7001,
		reload=True,
		debug=True,
		workers=4  # 进程数量
	)