import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

address_info = ['szuhaien@163.com'] #  接受者的邮箱列表

def send_message(headers,s,target_addr):
    #邮件发送
    # from_addr = 'szuhaien@sina.com'  # 发件邮箱
    from_addr = '1102485579@qq.com'  # 发件邮箱  (此处填你的邮箱（放松邮件的邮箱）)
    password = 'qqoyzfmmytchbadh'  # 邮箱密码            （邮箱的登陆密码）
    to_addr = target_addr  # 收件邮箱
    # smtp_server = 'smtp.sina.com'  # SMTP服务器，以新浪为例
    smtp_server = 'smtp.qq.com'  # SMTP服务器
      
    try:
        msg = MIMEText(s, 'plain', 'utf-8')
        # msg['Content-Type'] = 'Text/HTML';
        msg['From'] = formataddr([headers["sender_name"], from_addr])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        # msg['To'] = formataddr(["hai", 'you'])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = headers["title"]          # 邮件的主题，也可以说是标题
        # server = smtplib.SMTP(smtp_server)  # 第二个参数为默认端口为25，有些邮件有特殊端口
        server = smtplib.SMTP_SSL(smtp_server,465)  # 第二个参数为默认端口为25，有些邮件有特殊端口
        print('开始登录')
        server.login(from_addr, password)  # 登录邮箱
        print('登录成功')
        print("邮件开始发送")
        for item in to_addr:
            msg['To'] = formataddr([item, item])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            server.sendmail(from_addr, item, msg.as_string())  # 将msg转化成string发出
        server.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("邮件发送失败", e)

headers = {}
headers["sender_name"] = "zyy"    # sender name
headers["title"] = "title"     #   设置标题

mes_content = "十九分十九覅士大夫\n"+"ljljkjlk就立刻\n" # 内容

send_message(headers,mes_content,address_info)

print("ok!")