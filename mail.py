# SMTP Library
import smtplib

# Mail Library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email import encoders


# Const Value
SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 587

# SMTP Authentication
def auth_mail(user_id, user_pw):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        try:
            # TLS 보안 연결
            server.starttls()
            # SMTP 로그인 테스트 (성공)
            server.login(user_id, user_pw)

            print('SMTP 사용 가능')
        except:
            print('SMTP 사용 불가')

# Send Mail
def send_mail(user_id, user_pw, msg):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        try:
            # TLS 보안 연결
            server.starttls()
            # SMTP 로그인 테스트 (성공)
            server.login(user_id, user_pw)

            # 메일 전송
            res = server.sendmail(msg['from'], msg['to'], msg.as_string())
            if not res:
                print('메일 전송 성공')
            else:
                print('메일 전송 실패')
        except:
            print('메일 전송 실패')



idx = 0

# ID/PW 로드 (테스트)
with open('test.txt', mode='rt', encoding='utf-8') as f:
    for i in f.readlines():
        if idx == 1:
            break
        temp = i.splitlines()[0].split(' ') 
        print('ID: {0}, PW: {1}'.format(temp[0], temp[1]))

        # smtp_test
        smtp_info = dict({'smtp_server':'smtp.naver.com', 'smtp_port':587})
        smtp_info['smtp_user_id'] = temp[0]
        smtp_info['smtp_user_pw'] = temp[1]

        print(smtp_info)

        title = '기본 이메일입니다.'
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
        sender = temp[0] + '@naver.com'
        receiver = 'twenty--@naver.com'

        msg = MIMEText(_text=content, _charset='utf-8')
        msg['Subject'] = title
        msg['From'] = sender
        msg['To'] = receiver

        print(content)

        # # 딜레이를 줘야할 듯?
        # for i in range(0, 10):
        auth_mail(temp[0] ,temp[1])
        # send_mail(smtp_info, msg)

        # 임시
        idx = idx + 1