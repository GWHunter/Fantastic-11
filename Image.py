# -*- coding: utf-8 -*-
import os
import cv2
import pandas as pd
import requests
from bs4 import BeautifulSoup
import shutil

base = '/home/soumitra/Webscraping-Fifa-Ratings/Pictures/'
a = os.listdir(base)
incorrect = [];


df = pd.read_csv("PlayerNames.csv")

print("Read complete")


url = "https://www.fifaindex.com"
proxies = {
  'http': 'http://10.4.22.5:3128',
  'https': 'https://10.4.22.5:3128',
}
for i in range(len(a)):
    im = cv2.imread(base+a[i])
    if(im is None):
    	p = a[i].split('.')
    	incorrect.append(p[0])

row = [];
for element in incorrect:
	row.append(df[df['Name']==element]['url'])
	print(element)

print(len(incorrect))
for i in range(len(row)):
	for parts in row[i]:
		url_temp = url+parts
		while(True):
			print("Getting page "+url_temp)
			try:
				page = requests.get(url_temp,proxies=proxies)
			except requests.exceptions.RequestException as e:  # This is the correct syntax
				print(e)
				continue
			break

		html = page.content
		soup = BeautifulSoup(html,'lxml')
		
		Nat = soup.find('img')
		while(True):
			try:
				response = requests.get(url+Nat['src'], stream=True,proxies=proxies)
			except requests.exceptions.RequestException as e:  # This is the correct syntax
				print(e)
				continue
			break
		with open('Pictures/'+incorrect[i]+'.png', 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response