# # coding=utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class Send_Email(object):
	def __init__(self, byteio):
		self.receiver = "51952561@qq.com"
		self.sender = "51952561@qq.com"
		self.pwd = "hydtrpeghgzgcaad"  # 这里是64xxxxx71@qq.com邮箱的授权码

		self.msg = MIMEMultipart()
		self.msg["Subject"] = "Python微信扫码通知"  # 邮件的主题
		self.msg["From"] = self.sender
		self.msg["To"] = self.receiver

		self.part = MIMEText("请查看邮件附件扫码：请注意使用手机摄像头扫码登录验证。无法使用相册截图扫码登录。")  # 邮件的正文
		self.msg.attach(self.part)

		# jpg类型附件
		# self.part = MIMEApplication(open('apple.png', 'rb').read())  # 'apple.jpg'和该.py文件在同一个文件夹下
		self.part = MIMEApplication(byteio)  # 'apple.jpg'和该.py文件在同一个文件夹下
		self.part.add_header('Content-Disposition', 'attachment', filename="weixin.png")
		self.msg.attach(self.part)
		pass

	def send_email(self):

		try:
			s = smtplib.SMTP("smtp.qq.com", timeout=30)  # 连接smtp邮件服务器,端口默认是25
			s.ehlo()
			s.starttls()
			s.login(self.sender, self.pwd)  # 登陆服务器
			s.sendmail(self.sender, self.receiver, self.msg.as_string())  # 发送邮件
			s.close()
			print('邮件发送成功！')
		except smtplib.SMTPException:
			print('邮件发送失败！')


if __name__ == '__main__':
	# Send_Email().send_email()
	pass
