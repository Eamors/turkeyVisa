import hashlib
import redis
import json
import Config
import time

pool = redis.ConnectionPool(host=Config.REDIS_HOST, port=Config.REDIS_PROT, db=Config.CACHE_DB)


class HandleCache():
	def __init__(self, params):
		self.params = params
		self.db = redis.StrictRedis(connection_pool=pool)
	
	def encode_params(self):
		if isinstance(self.params, str):
			params_dict = json.loads(self.params)
			return params_dict
	def del_data(self):
		md_key = self.get_md5()
		self.db.delete(md_key)
	
	def get_md5(self):
		m = hashlib.md5()
		params_dict = self.encode_params()
		data = json.dumps(params_dict)
		m.update(data.encode("utf8"))
		return m.hexdigest()
	
	def get_data(self):
		params_dict = self.encode_params()
		md_key = self.get_md5()
		data = self.db.get(md_key)
		if data:
			data = data.decode()
		else:
			self.db.delete(md_key)
			data = None
		return data

	def get_datas(self):
		params_dict = self.encode_params()
		md_key = self.get_md5()
		if params_dict.get('cache') != 2 or 'cache' not in params_dict:
			data = self.db.get(md_key)
			if data:
				data = data.decode()
				if 'errMsg' in data:
					data = None
				else:
					data = data
		else:
			self.db.delete(md_key)
			data = None
		return data


	def get_backend(self, timeout):
		md_key = self.get_md5()
		# data = self.db.get(md_key)
		i = 0
		start_time = time.time()
		while i < timeout:
			data = self.db.get(md_key)
			# print(data)
			if data:
				return data.decode()
			i = time.time() - start_time
	
	def set_data(self, data):
		md_key = self.get_md5()
		self.db.set(md_key, data)
		self.db.expire(md_key, 600)


if __name__ == '__main__':
	response = {
		"loginAccount":"18067986193",
		"password":"123456",
		"json":{
			"message":"请求首页失败",
			"code":"53100",
			"data":{
				"extra":{

				}
			}
		},
		"taskId":"",
		"callbackType":"TURKEY_SUBMIT_TASK_CALLBACK_QUEUE"
	}


	para = {
      "company_type": 1,
      "company_code": "260b7b37dd4de97b9f762825ad82823a",
      "secret_key": "6f04aa1004e7dffbe632615539887f86",
      "user_code": "c4ca4238a0b923820dcc509a6f75849b",
      "spdier_name": "turkey_visa",
      "visa_data": {
        "option": "submit",
        "country":"1",
        "travel_date":"2020-09-11",
        "certificateType":"1",
    "personals": [
      {
        "firstname": "mingming",
        "familyname": "wang",
        "birthdate": "1992-10-12",
        "place_of_birth": "hangzhou",
        "mother_name": "monther",
        "father_name": "father",
        "travel_no": "EA888855",
        "travel_issue_date":"2016-10-14",
        "travel_expiry_date": "2026-10-15",
        "email":"lc2224268262@163.com",
        "phoneNumber": "15855558888",
        "contact_address": "hangzhoushi"
      },
        {
            "firstname": "mingtian",
            "familyname": "wang",
            "birthdate": "1991-10-12",
            "place_of_birth": "hangzhou",
            "mother_name": "assdasdf",
            "father_name": "fatsdgfdgher",
            "travel_no": "EA884455",
            "travel_issue_date": "2017-10-14",
            "travel_expiry_date": "2027-10-15",
            "email": "lc2224268262@163.com",
            "phoneNumber": "15855558888",
            "contact_address": "hangzhoushi"
        }
    ],
    "extra": {}
  }
}
	R_db = HandleCache(para)
	data = R_db.get_data()
	print(data)

	RedisHandle = HandleCache(para)
	RedisHandle.set_data(json.dumps(response))

	R_db = HandleCache(para)
	data = R_db.get_data()
	print(data)



# print(type(json.loads(a)))
# print()
