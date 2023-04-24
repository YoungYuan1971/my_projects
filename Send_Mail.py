import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from SecretData import EMAIL_INFO

EmailInfo = EMAIL_INFO()
# 邮箱基本信息
smtp_host = 'smtp.qq.com'
ssl_port = '465'
username = EmailInfo.USER_NAME
password = EmailInfo.AUTH_CODE  # 授权码，并非登录密码


# 用户基本信息
from_addr = username
sender_name = 'YoungYuan'
to_addrs = ['541518439@qq.com', 'young_yuan@hotmail.com']  # 群发邮件使用列表

# 设置邮件主题，内容
encoding = 'utf-8'  # 编码
subject = '这是一封来自Python的邮件'  # 邮件主题

text_content = f'{sender_name}通过Python自动给你发送了一份邮件，请查收！'
txt_part = MIMEText(text_content, 'plain', encoding)  # 邮件主体内容

with open('Stock.csv', 'rb') as f:
    att_content = f.read()
att_part = MIMEText(att_content, 'base64', encoding)  # 邮件附件内容
att_part["Content-Type"] = 'application/octet-stream'  # 对邮件附件的声明
att_part['Content-Disposition'] = 'attachment; filename="Stock.csv"'  # 对邮件附件的声明

# 初始化邮件
mail = MIMEMultipart()  # 多个MIME对象的集合；MIMEAudio音频；MIMEImage图像；MIMEText文本
mail['Subject'] = subject  # 设置邮件主题
mail['From'] = from_addr  # 设置显示发件人邮箱
mail['To'] = ','.join(to_addrs)  # 设置显示收件人邮箱（将列表转换成字符串）
mail.attach(txt_part)  # 加载文字部分
mail.attach(att_part)  # 加载附件部分

# 连接并登录邮箱服务器
smtp = smtplib.SMTP_SSL(smtp_host, ssl_port)  # 连接邮箱
smtp.login(username, password)  # 登录邮箱

# 发送邮件，断开连接
smtp.sendmail(from_addr, to_addrs, mail.as_string())
smtp.quit()
