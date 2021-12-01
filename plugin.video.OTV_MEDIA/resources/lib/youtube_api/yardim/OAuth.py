# -*- coding: UTF-8 -*-
from __future__ import print_function

from json import loads
from os import path

from .compat import compat_urlencode
from .compat import compat_urlopen
from .compat import compat_Request
import os
import xbmc, xbmcaddon, xbmcplugin
import xbmcgui
import sys
import time
import re


def GetKey(x):
	p = 3
	while True:
		if p > len(x):
			break
		pl = len(str(p))
		x = x[:p] + x[p + pl:]
		p += 12 - pl
	x = x.replace('w_OizD', 'a')
	x = x.replace('Xhi_Lo', 'A')
	return x
import os
import xbmc, xbmcaddon, xbmcplugin
import xbmcgui
import sys
import time
import re
addonId = "plugin.video.OTV_MEDIA"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
API_KEY = GetKey('Xhi3_LoIzw_OizD15SyCNReMvKL27nw_OizDWRR395T5uGWpvn451I2VYc78Gy463')
CLIENT_ID = GetKey('4113447027255-v15bgs05u1o3m278mpjs2vcd0394w_OizDfrg5160drbw_Oiz63D.w_OizDpp75s.googleus87ercontent.99com')
CLIENT_SECRET = GetKey('Zf93pqd2rxgY2ro159rK20BMxif27')

if os.path.join(os.path.join(dataPath), 'YouTube.key' ):
	try:
		for line in open(os.path.join(os.path.join(dataPath), 'YouTube.key' )).readlines():
			line = line.strip().replace(' ', '')
			if len(line) < 30 or line[0] == '#' or '=' not in line:
				continue
			line = line.split('=', 1)
			if line[1][:1] == '"' or line[1][:1] == "'":
				line[1] = line[1][1:]
			if line[1][-1:] == '"' or line[1][-1:] == "'":
				line[1] = line[1][:-1]
			if line[1][:4] == 'GET_':
				line[1] = GetKey(line[1][4:])
			if 'API_KEY' in line[0]:
				API_KEY = line[1]
			elif 'CLIENT_ID' in line[0]:
				CLIENT_ID = line[1]
			elif 'CLIENT_SECRET' in line[0]:
				CLIENT_SECRET = line[1]
	except Exception as e:
		print('[OAuth] Error in read YouTube.key:', e)


class OAuth:
	def __init__(self):
		self.device_code = ''
		self.retry_interval = 2

	def get_oauth_response(self, url, data):
		headers = {'Content-type': 'application/x-www-form-urlencoded'}
		try:
			request = compat_Request(url, data=data, headers=headers)
			request.get_method = lambda: 'POST'
			response = compat_urlopen(request)
			status_code = response.getcode()
			if status_code == 200:
				return loads(response.read())
			else:
				print('[OAuth] Error in auth response, errorcode', status_code)
				print(response.read())
		except Exception as e:
			print('[OAuth] Error in auth response', e)
		return {}

	def get_user_code(self):
		url = 'https://accounts.google.com/o/oauth2/device/code'
		data = compat_urlencode({
				'client_id': CLIENT_ID,
				'scope'	: 'https://www.googleapis.com/auth/youtube'}).encode()
		data = self.get_oauth_response(url, data)
		self.device_code = data.get('device_code', '')
		self.retry_interval = data.get('interval', 2)
		return str(data.get('verification_url', '')), str(data.get('user_code', ''))

	def get_new_token(self):
		url = 'https://accounts.google.com/o/oauth2/token'
		data = compat_urlencode({
				'client_id': CLIENT_ID,
				'client_secret': CLIENT_SECRET,
				'code': self.device_code,
				'grant_type': 'http://oauth.net/grant_type/device/1.0'}).encode()
		data = self.get_oauth_response(url, data)
		if 'access_token' in data and 'refresh_token' in data:
			return data['refresh_token'], 1
		return None, self.retry_interval + 2

	def get_access_token(self, refresh_token):
		url = 'https://accounts.google.com/o/oauth2/token'
		data = compat_urlencode({
				'client_id': CLIENT_ID,
				'client_secret': CLIENT_SECRET,
				'refresh_token': refresh_token,
				'grant_type': 'refresh_token'}).encode()
		data = self.get_oauth_response(url, data)
		if 'access_token' in data:
			return data['access_token']
		print('[OAuth] Error in get access token')
		return None
