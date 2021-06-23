"""
项目入口
"""
from fastapi import FastAPI
import uvicorn
from fastapi_tutorial import app_03, app_04, app_05

app_main = FastAPI()

# 将子应用加入主应用中
app_main.include_router(app_03, prefix='/chapter_03', tags=['第三章，请求参数和验证'])
app_main.include_router(app_04, prefix='/chapter_04', tags=['第四章，相应处理处理和fastapi配置'])
app_main.include_router(app_05, prefix='/chapter_05', tags=['第五章，fastapi的依赖注入系统'])


if __name__ == '__main__':
	uvicorn.run(
		'run:app_main',
		host='127.0.0.1',
		port=7000,
		reload=True,
		debug=True,
		workers=4  # 进程数量
	)