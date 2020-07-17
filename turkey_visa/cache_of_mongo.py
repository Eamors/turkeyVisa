import pymongo
import Config
import json
import hashlib
import time
from datetime import datetime

class HandleCache():
	def __init__(self, params):
		self.params = params
		# self.db = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PROT, db=Config.CACHE_DB)
		self.client = pymongo.MongoClient(host=Config.MONGO_HOST, port=Config.MONGO_PORT)
		self.mongo_db = self.client[Config.MONGO_DB]
		self.cache_col = self.mongo_db[Config.MONGO_CAHCE]
		self.cache_col.create_index([("cache_time", 1)], expireAfterSeconds=3)
		self.cache_col.create_index([('_id',2)])
	
	def encode_params(self):
		if isinstance(self.params, str):
			params_dict = json.loads(self.params)
			return params_dict
	
	def get_md5(self):
		m = hashlib.md5()
		params_dict = self.encode_params()
		# if 'ceche' in data:
		# 	# print("缓存需求")
		# 	data = data.replace(""","ceche":""}""", "}")
		# print(data)
		if 'cache' in params_dict:
			del params_dict['cache']
		data = json.dumps(params_dict)
		# print(data)
		m.update(data.encode("utf8"))
		return m.hexdigest()
	
	def get_data(self):
		params_dict = self.encode_params()
		if params_dict.get('cache'):
			md_key = self.get_md5()
			data = self.cache_col.find_one({"_id":md_key})
			if data:
				del data['_id']
			else:
				data = None
		else:
			data = None
		# self.cache_col.remove({'_id':"5b8b7e1fa094c8cf6d2b00e1e36de1d3"})
		self.client.close()
		return data
	
	def set_data(self, data):
		# md_key = self.get_md5(params)
		md_key = self.get_md5()
		data['_id'] = md_key
		data['cache_time'] = datetime.utcnow()
		self.cache_col.insert_one(data)
		self.client.close()
		# print(md_key),
		# print(data)
	
	
if __name__ == '__main__':
	a = """{"oragin": "CK", "dest": "SZX", "fromDate": "20190506", "appName": "xcyx", "tripType": "1", "retDate":"","cache":1}"""
	data = {"name":"gao","age":24}
	Cache = HandleCache(a)
	# Cache.set_data(data)
	x = Cache.get_data()
	print(x)
	# start_time = time.time()
	# while Cache.get_data():
	# 	pass
	# end_time = time.time()
	# print(end_time-start_time)
	
	
	
	
	
	
	
	
	
	
	
	
	
	