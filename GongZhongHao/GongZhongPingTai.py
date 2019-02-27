# -*- coding: utf-8 -*-
# Author : ZSQ
# Time : 2019-01-25 10:49
import random

from fake_useragent import UserAgent
import time
import requests
from PIL import Image
from io import BytesIO

from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from send_email import Send_Email

class Gongzhongpingtai(object):
	def __init__(self):
		self.base_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&share=1&lang=zh_CN&token=1569823112'
		self.url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&share=1&lang=zh_CN&token=1106542388'
		self.lists = ['安徽']

	def handle_cookies(self):
		# self.username = '1875030315@qq.com'
		self.username = '2855139763@qq.com'
		# self.password = 'zsq987654321'
		self.password = 'zsq19940519zsq'
		self.chrom_options = Options()
		self.ua = UserAgent(verify_ssl=False)
		self.headers = {
			'User-Agent': self.ua.random
		}
		self.chrom_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
		self.chrom_options.add_argument('--headless')  # 设置是否提供可视化界面
		self.chrom_options.add_argument('--disable-infobars')  # 是否提示自动化测试浏览器
		# self.chrom_options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
		self.chrom_options.add_argument('--disable-gpu')  # 谷歌文档提示用来规避bug
		self.driver = webdriver.Firefox(firefox_options=self.chrom_options)
		self.driver.maximize_window()
		self.driver.get(self.url)
		login = self.driver.find_element_by_xpath('//*[@id="jumpUrl"]').is_displayed()
		if login:
			self.driver.find_element_by_xpath('//*[@id="jumpUrl"]').click()
			time.sleep(1)
			self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/form/div[1]/div[1]/div/span/input').send_keys(self.username)
			self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/form/div[1]/div[2]/div/span/input').send_keys(self.password)
			time.sleep(1)
			self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/form/div[4]/a').click()
			self.driver.implicitly_wait(10)
			qr_code = self.driver.find_element_by_xpath('//*[@id="app"]/div[3]/div/div[2]/div[2]/div/div/div/div/p[1]').is_displayed()
			cookies = self.driver.get_cookies()
			cookie = {}
			for cook in cookies:
				name = cook['name']
				value = cook['value']
				cookie[name] = value
			# print(cookie)
			if qr_code:
				image_url = self.driver.find_element_by_xpath('//*[@id="app"]/div[3]/div/div[2]/div[1]/div/img').get_attribute('src')
				# print(image_url)
				response = requests.get(image_url, cookies=cookie, headers=self.headers)

				Send_Email(response.content).send_email()
				# print(response.content)
				# image = Image.open(BytesIO(response.content))
				# w, h = image.size
				# image.thumbnail((w // 2, h // 2))
				# image.save('QR_code/1.jpg')
				# image.show() #扫码图片show
				code_times = 600
				while True:
					current_url = self.driver.current_url
					if 'home?t=home/index' in current_url:
						break
					time.sleep(5)
					code_times -= 5
					if code_times <= 5:
						self.driver.quit()
						Gongzhongpingtai().handle_cookies()
						code_times = 600
				current_url = self.driver.current_url
				token = current_url.split('token=')[1]
				cookies = self.driver.get_cookies()
				cook = {}
				for cookie in cookies:
					name = cookie['name']
					value = cookie['value']
					cook[name] = value
				result = [token, cook]
				# print(result)
				self.driver.quit()
				with open('login_info.txt', 'w+') as f:
					f.write(str(result))
				return result
		# self.driver.find_element_by_xpath('//*[@id="menuBar"]/li[4]/ul/li[3]/a/span/span').click()
		# self.driver.implicitly_wait(10)
		# handle = self.driver.current_window_handle
		# self.driver.find_element_by_xpath('//*[@id="js_main"]/div[3]/div[1]/div[2]/div[2]/div/button[1]').click()
		# all_windows = self.driver.window_handles
		# for window in all_windows:
		# 	if handle != window:
		# 		self.driver.switch_to_window(window)
		# 	else:
		# 		self.driver.close()
		# time.sleep(2)
		# self.driver.implicitly_wait(10)
		# self.driver.find_element_by_xpath('//*[@id="edui24_body"]').click()
		# self.driver.implicitly_wait(10)
		# try:
		# 	self.driver.find_element_by_xpath('//*[@id="myform"]/div[3]/div[1]/div/label[2]').click()
		# except:
		# 	self.driver.find_element_by_xpath(
		# 		'/html/body/div[13]/div/div[2]/form/div[3]/div[1]/div/label[2]/span').click()
		# time.sleep(1)
		# self.driver.implicitly_wait(10)
		# for list in self.lists:
		# 	try:
		# 		self.driver.find_element_by_xpath('//*[@id="myform"]/div[3]/div[3]/div[1]/div/span[1]/input').send_keys(list)
		# 	except Exception as f:
		# 		self.driver.find_element_by_xpath("//*[@class='frm_input js_acc_search_input valid']").send_keys(list)
		# 	# print(f)
		# 	self.driver.find_element_by_xpath('//*[@id="myform"]/div[3]/div[3]/div[1]/div/span[1]/a[2]').click()
		# 	before_num = int(self.driver.find_element_by_xpath('//*[@class="page_num"]/label[1]').text)
		# 	after_num = int(self.driver.find_element_by_xpath('//*[@class="page_num"]/label[2]').text)
		# 	for i in range(1, after_num):
		# 		self.driver.implicitly_wait(20)
		# 		wechat_names = self.driver.find_elements_by_xpath("//*[@class='search_biz_info']/p[1]")
		# 		wechat_ids = self.driver.find_elements_by_xpath("//*[@class='search_biz_info']/p[2]")
		# 		lens = len(wechat_names)
		# 		for j in range(lens):
		# 			wechat_name = str(wechat_names[j].text).strip()
		# 			wechat_id = str(wechat_ids[j].text).replace('微信号：', '')
		# 			print(wechat_name, wechat_id)
		# 			with open('GongZhongPingTai.csv','a+') as f:
		# 				f.write(str(wechat_name) + ',' + str(wechat_id) + '\n')
		# 		time.sleep(random.randint(2,8))
		#
		# 		if i == 2:
		# 			break
		# 		try:
		# 			self.driver.find_element_by_xpath("//*[@class='pagination']/span[1]/a[@class='btn page_next']").click()
		# 		except:
		# 			time.sleep(30)
		# 			self.driver.find_element_by_xpath("//*[@class='pagination']/span[1]/a[@class='btn page_next']").click()




		else:
			self.driver.refresh()
			self.handle_cookies()
		self.driver.quit()

	pass


if __name__ == '__main__':
	Gongzhongpingtai().handle_cookies()
