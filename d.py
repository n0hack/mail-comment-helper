# SMTP Library
import smtplib

# Mail Library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email import encoders

import os

SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 587

def send_mail( user_id, user_pw, msg):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        try:
            # TLS 보안 연결
            server.starttls()
            # SMTP 로그인 테스트 (성공)
            server.login(user_id, user_pw)
            # 메일 전송
            print('실제 sender: {0}'.format(msg['From']))
            res = server.sendmail(msg['From'], msg['To'], msg.as_string())
            if not res:
                print('완')
            else:
                print('실')
        except Exception as e:
            print(e)


subject = '메일 제목 (블로그 댓글은 설정 안 해도 됨)'
content = '''
안녕하세요^^

혹시 블로그를 통해 포스팅 해보실 의향 없으신가요?
준비된 원고를 보내드리면 블로그에 복붙해서 올려주시면 되고, 한 건 올리시는데 5분 이내로 소요됩니다.

저희는 업체 홍보 리뷰, 제품, 맛집, 뷰티, 홍보 리뷰를 주로 하는 업체입니다.

포스팅 비용은 건당 2~3만원 입니다!

저희 업체는 불법적인 키워드가 아닌 합법적인 키워드만 취급하고 있습니다.
원고는 일주일에 10~15건 정도 드리며, 하실 의향이나 궁금하신 점 있으시면 010-8733-7408로 연락주세요!

긴 글 읽어주셔서 감사합니다.
'''
msg = MIMEMultipart('SendMail')
msg['Subject'] = subject
msg['From'] = 'nohack-@naver.com'
msg['To'] = 'twenty--@naver.com'

img_data = open('./img/test.png', 'rb').read()
image = MIMEImage(img_data, name=os.path.basename('./img/test.png'))
msg.attach(image) 

# msg = MIMEText(_text=content, _charset='utf-8')
# msg['Subject'] = subject
# msg['From'] = 'nohack-@naver.com'
# msg['To'] = 'twenty--@naver.com'

print(msg)
# for i in range(0, 10):
send_mail('nohack-', 'wjswlehf2!N', msg)