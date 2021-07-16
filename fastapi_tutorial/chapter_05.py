from fastapi import APIRouter, Depends, Header, HTTPException
from typing import Optional

app_05 = APIRouter()

def comment_parse(q: Optional[str] = None, page: int = 1, limit: int = 100):
	return {'page': page, 'limit': limit, 'parse': q}


@app_05.get('/def_dependence_01', summary='01')
async def dependency01(comments: dict = Depends(comment_parse)):
	return comments


@app_05.get('/def_dependence_02', summary='02')
def dependency02(comments: dict = Depends(comment_parse)):
	return comments

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

# 子依赖

def quer(q: Optional[str] = None):
	return q

def sub_query(q: str = Depends(quer), last_q: str = 'test last q'):
	if not q:
		return last_q
	return q

@app_05.get('/sub_dependency')
async def sub_dependency(query_parse: str = Depends(sub_query, use_cache=True)):
	""" use_cache 表示当多个依赖有同一个子依赖时， 每次request请求只会调用一次子依赖 提升性能"""
	return {'quesy_parse': query_parse}
	


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