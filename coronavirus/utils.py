import requests


def return_requests_data(param_url):
	retry_times = 20
	retry_count = 0
	for i in range(retry_times):
		retry_count += 1
		try:
			if retry_count > 1:
				print(f'重试第{retry_count - 1}次请求，当前请求地址为: [ {param_url} ] 请等待...')
			http_res = requests.get(url=param_url, verify=False, timeout=5)
			http_res.close()
			return http_res
		except Exception as e:
			if retry_count >= retry_times:
				print(f'{param_url},请求失败，原因{e}')
				return False
			else:
				continue