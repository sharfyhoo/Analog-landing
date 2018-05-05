#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import time
import copy
import hmac
import hashlib
import base64
import json
from orc import *
from requests_toolbelt.multipart.encoder import MultipartEncoder

import sys   #引用sys模块进来，并不是进行sys的第一次加载  
reload(sys)  #重新加载sys  
sys.setdefaultencoding('utf8')  ##调用setdefaultencoding函数



class ZhiHu(object):
	u"""知乎类"""

	def __init__(self):
		u"""初始化"""
		self.headers = {
			'Host': 'www.zhihu.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
			'Referer': 'https://www.zhihu.com/signup?next=%2F',
			'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
			'X-Xsrftoken': 'adea40fb-0956-4019-98f3-d4411ccce8ed',
			'Content-Length': '0',
			'Origin': 'https://www.zhihu.com',

		}
		self.requests = requests.session()
		self.proxies = { "http": "http://192.168.199.228:8888", "https": "http://192.168.199.228:8888", }
		self.timestamp = str(int(float(time.time())*1000))

	def _get(self, url, param=None, headers=None):
		u"""构造get请求"""
		old_headers = copy.deepcopy(self.headers)
		if headers:
			old_headers.update(headers)

		if param:
			response = self.requests.get(url, param=param, headers=old_headers, verify=False, proxies=self.proxies)
		else:
			response = self.requests.get(url, headers=old_headers, verify=False, proxies=self.proxies)
		return response
	
	def _post(self, url, data=None, headers=None):
		u"""构造post请求"""
		old_headers = copy.deepcopy(self.headers)
		if headers:
			old_headers.update(headers)

		if data:
			response = self.requests.post(url, data=data, headers=old_headers, verify=False, proxies=self.proxies)
		else:
			response = self.requests.post(url, headers=old_headers, verify=False, proxies=self.proxies)
		return response

	def _put(self, url, data=None, headers=None):
		old_headers = copy.deepcopy(self.headers)
		if headers:
			old_headers.update(headers)
		if data:
			response = self.requests.put(url, data=data, headers=old_headers, verify=False, proxies=self.proxies)
		else:
			response = self.requests.put(url, headers=old_headers, verify=False, proxies=self.proxies)
		return response

	def login(self):
		u"""登录操作"""
		files = {
			'client_id': "c3cef7c66a1843f8b3a9e6a1e3160e20",      # 固定值  js里有
			'grant_type': 'password',
			'timestamp': self.timestamp,
			'source': 'com.zhihu.web',
			'signature': self.get_signature(),
			'username': '+8617601016701',
			'password': 'hu123456',
			'captcha': self.get_captcha(),
			'lang': 'en',
			'ref_source': 'homepage',
			'utm_source': '',
		}

		boundary = '------WebKitFormBoundaryUO9iTB26wze2OcCK'
		headers = {
			'Content-Type': 'multipart/form-data; boundary={}'.format(boundary)
		}
		data = MultipartEncoder(files, boundary).to_string()
		url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
		response = self._post(url, data=data, headers=headers)
		if 'user_id' in response.text:
			print u'登陆成功---'
			return
		else:
			print response.text

	def get_signature(self):
		u"""对digestmod进行hmac sha1加密"""
		myhmac = hmac.new('d1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
		e = b'password'         # 固定值
		u = b'c3cef7c66a1843f8b3a9e6a1e3160e20'   #固定值
		s = b'com.zhihu.web'    # 固定值
		n = bytes(self.timestamp)
		myhmac.update(e)
		myhmac.update(u)
		myhmac.update(s)
		myhmac.update(n)
		signature = myhmac.hexdigest()
		print signature
		return signature

	def get_captcha(self):
		u"""获取验证码"""

		url = "https://www.zhihu.com/api/v3/oauth/captcha?lang=en"
		response = self._get(url)
		response = self._put(url)
		if 'img_base64' in response.text:
			img_base64 = json.loads(response.text)['img_base64']
			img = base64.b64decode(img_base64)
			img_name = 'zhihu_captcha.jpg'
			with open('img/{}'.format(img_name), 'wb') as f:
				f.write(img)
				f.close()
			captcha = raw_input(u'请输入验证码:')
			return captcha

if __name__ == "__main__":
	zhihu = ZhiHu()
	# zhihu.get_captcha()
	zhihu.login()


