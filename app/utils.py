import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

def gui_email(email_nguoi_dung):
    email_he_thong = "2251052134tuan@ou.edu.vn"
    password_he_thong = "testathttt"
    noi_dung = str(random.randint(10000, 99999))

    smtp_session = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_session.starttls()
    smtp_session.login(email_he_thong, password_he_thong)

    message = MIMEMultipart()
    message['From'] = email_he_thong
    message['To'] = email_nguoi_dung
    message['Subject'] = "mã xác nhận"
    message.attach(MIMEText(noi_dung, 'plain'))

    smtp_session.sendmail(from_addr=email_he_thong, to_addrs=email_nguoi_dung, msg=message.as_string())

    smtp_session.quit()
    return noi_dung