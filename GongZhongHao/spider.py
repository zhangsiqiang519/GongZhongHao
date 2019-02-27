# -*- coding: utf-8 -*-
# Author : ZSQ
# Time : 2019-01-30 15:36
import datetime
import random
import time

import requests
from GongZhongPingTai import Gongzhongpingtai
from fake_useragent import UserAgent
from openpyxl import Workbook


class WeiXinPinTaiSpider(object):
	def __init__(self):
		self.lists = ['合肥', '芜湖']
		self.ua = UserAgent(verify_ssl=False)
		self.headers = {
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Cache-Control': 'no-cache',
			'Connection': 'keep-alive',
			'Host': 'mp.weixin.qq.com',
			'Pragma': 'no-cache',
			'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=1389721861&lang=zh_CN',
			'User-Agent': self.ua.random,
			'X-Requested-With': 'XMLHttpRequest'
		}
		self.wb = Workbook()
		self.ws = self.wb.active
		self.ws.append(['微信名', '微信ID'])

	def get_info(self):
		with open('login_info.txt', 'r+') as f:
			result = eval(f.readline())
		json = requests.get(url='https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={}&lang=zh_CN&f=json&ajax=1&random=0'
		                        '.5773776028057243&query=%E5%AE%89%E5%BE%BD&begin=0&count=5'.format(result[0]), cookies=result[1]).json()
		print(json)
		if json['base_resp']['ret'] == 200003:
			Gongzhongpingtai().handle_cookies()
			time.sleep(3)
			WeiXinPinTaiSpider().get_info()
		if json['base_resp']['ret'] == 200013:
			Gongzhongpingtai().handle_cookies()
			time.sleep(3)
			WeiXinPinTaiSpider().get_info()
		try:
			while True:
				to_day = datetime.datetime.now()
				for list in self.lists:
					if int(json['total']) > 0:
						page = int(json['total']) // 5 + 1
						for i in range(page):
							print('当前爬取第{}页'.format(i))
							# https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={
							# }&lang=zh_CN&f=json&ajax=1&random=0.5773776028057243&query=安徽&begin=1&count=5
							json1 = requests.get(
								url='https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={}'
								    '&lang=zh_CN&f=json&ajax=1&random=0.5773776028057243&query={}&begin={}&count=10'.format(result[0], list,
								                                                                                            i * 10),
								cookies=result[1]).json()
							if json1['base_resp']['ret'] == 200003:
								Gongzhongpingtai().handle_cookies()
								time.sleep(3)
								json1 = requests.get(
									url='https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={}'
									    '&lang=zh_CN&f=json&ajax=1&random=0.5773776028057243&query={}&begin={}&count=10'.format(result[0],
									                                                                                            list,
									                                                                                            i * 10),
									cookies=result[1]).json()
							if json1['base_resp']['ret'] == 200013:
								Gongzhongpingtai().handle_cookies()
								time.sleep(60 * 60 * 24)
								json1 = requests.get(
									url='https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={}'
									    '&lang=zh_CN&f=json&ajax=1&random=0.5773776028057243&query={}&begin={}&count=10'.format(result[0],
									                                                                                            list,
									                                                                                            i * 10),
									cookies=result[1]).json()

							if json1['base_resp']['err_msg'] == 'ok':
								for lis in json1['list']:
									wechat_name = lis['nickname']
									wechat_id = lis['alias']
									print(wechat_name, wechat_id)
									line = [wechat_name, wechat_id]
									self.ws.append(line)  # 将数据以行的形式添加到xlsx中
									try:
										self.wb.save('/Users/apple/XianMu/GongZhongHao/WeiXinPinTaiSpider_{}_{}_{}.xlsx'.format(to_day.year,
										                                                                                        to_day.month,
										                                                                                        to_day.day))  # 保存xlsx文件
									except:
										self.wb.save('C:\\Users\ZSQ\Desktop\GongZhongHao\WeiXinPinTaiSpider_{}_{}_{}.xlsx'.format(
											to_day.year, to_day.month, to_day.day))
								# 保存xlsx文件
								# with open('WeiXinPinTaiSpider7.csv', 'a+', encoding="utf8", newline='') as f:
								# 	f.write(wechat_name + ',' + wechat_id + '\n')
								time.sleep(random.randint(40, 61))
								# time.sleep(61)

								if i == page:
									break

		except:
			print(json)


if __name__ == '__main__':
	WeiXinPinTaiSpider().get_info()
