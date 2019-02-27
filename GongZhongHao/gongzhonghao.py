# -*- coding: utf-8 -*-
# Author : ZSQ
# Time : 2019-01-16 09:13
from openpyxl import Workbook
import time

from fake_useragent import UserAgent

import wechatsogou


class GongZhongHao(object):
	def __init__(self):
		self.ua = UserAgent(verify_ssl=False)
		self.ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3, timeout=1)
		# self.search_lists = [] #搜索入口
		# self.search_lists =  #搜索入口
		self.search_lists = [] #搜索入口
		self.page_num = 10 # 爬取页数
		self.wb = Workbook()
		self.ws = self.wb.active
		self.ws.append(['微信号唯一ID', '名称', '微信id', '介绍', '认证', '最近的一篇文章', '最近一月群发数'])
		pass

	def gongzhonghao(self):
		for search_list in self.search_lists:
			time.sleep(2)
			for page in range(1, self.page_num + 1):
				print('正在保存 {} 第 {} 页内容！'.format(search_list, page))
				time.sleep(3)
				infos_list = self.ws_api.search_gzh(search_list, page=page)
				# print(infos_list)
				for info_dicts in infos_list:
					# 'open_id': '', # 微信号唯一ID
					# 'profile_url': '',  # 最近的一篇文章
					# 'headimage': '',  # 头像
					# 'wechat_name': '',  # 名称
					# 'wechat_id': '',  # 微信id
					# 'post_perm': '',  # 最近一月群发数
					# 'qrcode': '',  # 二维码
					# 'introduction': '',  # 介绍
					# 'authentication': ''  # 认证
					# print(info_dicts['profile_url'])
					line = [info_dicts['open_id'], info_dicts['wechat_name'], info_dicts['wechat_id'],
					        info_dicts['introduction'], info_dicts['authentication'], info_dicts['profile_url'],
					        info_dicts['post_perm']]
					self.ws.append(line)
					try:
						self.wb.save('./gongzhonghao.xlsx')

					except:
						pass
				print('{} 第 {} 页内容收集完成！'.format(search_list, page))

if __name__ == '__main__':
	GongZhongHao().gongzhonghao()
