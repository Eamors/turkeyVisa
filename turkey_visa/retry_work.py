from retry import retry

@retry(exceptions=RuntimeError,tries=5)
def r_work(c_obj,func_name,url_name,params):
	func_name.delay(url_name, params)

	print('2222')
	# data = c_obj.get_backend(timeout=7)
	# if data and 'errMsg' in data:
	# 	raise
	# else:
	# 	return data

@retry(exceptions=RuntimeError,tries=5)
def save_task(c_obj,func_name,url_name,params):
	print('到这了')
	# func_name.delay(url_name, params)
	func_name.apply_async(args=[url_name, params])
	print("过去了")



