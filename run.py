"""
    项目入口
"""
import time

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from flask import Request

from coronavirus import app_coronavirus
from fastapi_tutorial import app_03, app_04, app_05, app_06, app_07, app_08

app_main = FastAPI(
    title='my_fastapi',
    description='first fastapi app - fastapi TEST',
    version='1.0.1',
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

""" 中 间 件 """


@app_main.middleware('http')
async def process_tiem_add_header(request: Request, call_next_def):
    # 在此可加请求日志系统
    # call_next_def(request) 接收request参数,  为回调函数
    print(request.__dict__)
    start_time = time.time()
    response = await call_next_def(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    print(response.__dict__, '----------')
    return response


""" 加载中间件 """
app_main.add_middleware(
    CORSMiddleware,
    # 允许的源，   协议 + ip + 端口 == 源，
    allow_origins=[
        'http://127.0.0.1',  # 没有端口默认为80
        'http://127.0.0.1:8080',
        'http://127.0.0.1:7000',
    ],  # ['*'] 表示所有

    # 允许使用证书
    allow_credentials=True,
    allow_methods=[
        'get',
        'post',
        'put',
        'delete',
        'options',
        'patch'
    ],  # ['*'] 表示所有

    allow_headers=[
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
        'token',
    ]
)

if __name__ == '__main__':
    uvicorn.run(
        'run:app_main',
        host='127.0.0.1',
        port=7001,
        reload=True,
        workers=4  # 进程数量
    )
