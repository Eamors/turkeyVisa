from flask import Flask
from Celery_spider.turkey_tasks import turkey_spider
from do_md5 import HandleCache
from Config import DevConfig
from flask import request
from retry_work import r_work,save_task
import json
import logging
import socket

app = Flask(__name__)
app.logger.name = 'flask_celery'
logging.basicConfig(filename='flask_celery.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
app.config.from_object(DevConfig)


# Ceche_db = HandleCache()


@app.route('/turkey/CheckVisaStatus', methods=['GET', 'POST'])
def CheckVisaStatus():
	"""
	目前的请求流程是：收到汪松发来的请求之后，将任务放进rabbitmq,立即返回当前是否接到请求
	然后消费者再处理任务，通过回调地址，消费者执行完成后，再将结果返回给汪松
	:return:
	"""
	if request.method == "POST":
		params = request.get_data().decode()
		app.logger.info('接受到来自{}的土耳其的visa查询请求。\n参数：{}'.format(request.remote_addr, params))
		try:
			para = json.loads(params)
		except:
			dicts = {
				"code": "1000",
				"message": "参数有误，请传json"
			}
			return json.dumps(dicts, ensure_ascii=False)

		account = para.get("visa_data").get("account")
		#新加查缓存
		Cache = HandleCache(account)
		data = Cache.get_data()
		if data:
			print('数据在缓存队列中，直接返回')
			app.logger.info('数据在缓存队列中，直接返回：{}'.format(params))
			return data
		else:
			print("不在队列")

		passportNumber = account.get("passportNumber")
		email = account.get("email")
		if passportNumber and email:
			Cache = HandleCache(params)
			url_name = 'checkVisaStatus'
			save_task(Cache, turkey_spider, url_name, params)
			dicts = {
				"code": "0",
				"message": "收到请求，任务已提交，待处理"
			}
			return json.dumps(dicts, ensure_ascii=False)
		else:
			dicts = {
				"code": "1000",
				"message": "护照号或者邮箱不能为空"
			}
			return json.dumps(dicts, ensure_ascii=False)
	else:
		dicts = {
			"code": "1000",
			"message": "请传post请求"
		}
		return json.dumps(dicts, ensure_ascii=False)


@app.route('/turkey/submit', methods=['GET', 'POST'])
def turkeyVisa():
	"""
	目前的请求流程是：收到汪松发来的请求之后，将任务放进rabbitmq,立即返回当前是否接到请求
	然后消费者再处理任务，通过回调地址，消费者执行完成后，再将结果返回给汪松
	:return:
	"""
	if request.method == "POST":
		params = request.get_data().decode()
		app.logger.info('接受到来自{}的土耳其的visa提交请求。\n参数：{}'.format(request.remote_addr, params))
		try:
			para = json.loads(params)
		except:
			dicts = {
				"code": "1000",
				"message": "参数有误，请传json"
			}
			return json.dumps(dicts, ensure_ascii=False)

		Cache = HandleCache(params)
		data = Cache.get_data()
		if data:
			print('数据在缓存队列中，直接返回')
			app.logger.info('数据在缓存队列中，直接返回：{}'.format(params))
			return data
		else:
			print("缓存里没有")
		url_name = 'submit'
		save_task(Cache, turkey_spider, url_name, params)
		# r_work(Cache, turkey_spider, url_name, params)
		print('111111111111111111111111')
		dicts = {
			"code": "0",
			"message": "收到请求，任务已提交，待处理"
		}
		return json.dumps(dicts, ensure_ascii=False)

	else:
		dicts = {
			"code": "1000",
			"message": "请传post请求"
		}
		return json.dumps(dicts, ensure_ascii=False)



