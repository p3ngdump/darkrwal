import os
import socket
from logger import logger

import requests

from torpy import TorClient
from torpy.stream import TorStream
from torpy.utils import AuthType, recv_all, retry
from torpy.http.adapter import TorHttpAdapter
from torpy.hiddenservice import HiddenService
from torpy.http.requests import TorRequests, tor_requests_session, do_request as requests_request
from torpy.http.urlopener import do_request as urllib_request

import store_web

RETRIES = 3

def front():
	print("               .__                                  __          ")
	print("__  _  __ ____ |  |   ____  ____   _____   ____   _/  |_  ____  ")
	print("\ \/ \/ // __ \|  | _/ ___\/  _ \ /     \_/ __ \  \   __\/  _ \ ")
	print(" \     /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/   |  | (  <_> )")
	print("  \/\_/  \___  >____/\___  >____/|__|_|  /\___  >  |__|  \____/ ")
	print("             \/          \/            \/     \/                ")
	print("    .___             __                         .__   ")
	print("  __| _/____ _______|  | ______________ __  _  _|  |  ")
	print(" / __ |\__  \\_  __ \  |/ /\_  __ \__  \\ \/ \/ /  |  ")
	print("/ /_/ | / __ \|  | \/    <  |  | \// __ \\     /|  |__")
	print("\____ |(____  /__|  |__|_ \ |__|  (____  /\/\_/ |____/")
	print("     \/     \/           \/            \/             ")

def onion_online(address):
	data = requests_request(address, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'}, retries=RETRIES)
	if('200' in data or '201' in data or '202' in data):
		return True
	else:
		return False

def onion_connect(address):
	with TorClient() as tor:
		tor.create_circuit(3)
		with tor.get_guard() as guard:
			adapter = TorHttpAdapter(guard, 3, retries=RETRIES)

			with requests.Session() as s:
				s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'})
				s.mount('http://', adapter)
				s.mount('https://', adapter)

				r = s.get(address, timeout=30)
				#logger.warning(r)
				#logger.warning(r.text)
				return r.text.rstrip()
 
def parse_data_ahmia(data):
	url_list = list()
	tmp = ""
	data = data.split("&redirect_url=")
	for i in data:
		if('http://' in i or 'https://' in i):
			tmp = i.split("\">")
			url_list.append(tmp[0])

	return url_list

def web_content(address):
	try:
		online = onion_online(address)
	except:
		return
	if(online):
		print('[+] onion site is online now!!')
		print('[+] we will connect now.. wait a minute please..')
		data = onion_connect(address)
		print(data)
		store_web.store(data)

if(__name__=="__main__"):
	front()
	keyword = ['sex', 'ransom', 'virus', 'worm', 'apt', 'hack', 'drug', 'cocaine', 'addict', 'backdoor', 'trojan', 'bypass', 'vulnerabl', 'attack', 'ransomware', 'hacker', 'rape', 'violate', 'vulnerable', 'vulnerability']
	before_address = "http://msydqstlz2kzerdg.onion/search/?q="
	url_list = list()
	#count = 1

	for i in keyword:
		online = onion_online(before_address + i)
		online = 1
		if(online):
			print('[+] onion site is online now!!')
			print('[+] we will connect now.. wait a minute please..')
			#data = onion_connect(before_address + i)
			data = onion_connect(before_address + i)
			url_list = parse_data_ahmia(data)
			for i in url_list:
				web_content(i)
		else:
			print('[+] onion site is not online now..!')