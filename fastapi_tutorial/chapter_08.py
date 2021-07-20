import time
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends

app_08 = APIRouter()



"""
	中间件、CORS 代码参见run.py中
"""

# 1、	中间件 代码参见run.py中
# 2、	CORS 代码参见run.py中

# 3、后台任务

async def task_back(parse):
	with open('readmes.md', 'w+', encoding='utf-8') as fp:
		fp.write(parse)
	
# 单个函数的异步任务
@app_08.post('/task')
async def backend_task(framework: str, backend_task: BackgroundTasks):
	"""
		后台任务
	:param framework: 被调用的后台任务传入的参数
	:param backend_task:  后台任务对象
	:return:
	"""
	backend_task.add_task(task_back, framework)
	return {'info': 200}

# 依赖注入异步任务

async def write_readme(bacend_task: BackgroundTasks, parse_q: Optional[str] = None):
	if parse_q:
		bacend_task.add_task(task_back, parse_q)
		return parse_q

@app_08.post('/dependency')
async def dependency_task(parse: str = Depends(write_readme)):
	if parse:
		return {'info': '文件正在写入'}
	else:
		return {'info': '啥也不是'}