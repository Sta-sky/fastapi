from fastapi import APIRouter
app_07 = APIRouter()

@app_07.get('/city/info')
def get_city_info(city_id: int):
	return