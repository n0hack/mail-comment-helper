import time

# SMTP Library
import smtplib

# Mail Library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email import encoders

# PyQt Library
from PyQt5 import QtCore, QtWidgets


# Const Value
SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 587

class AuthThread(QtCore.QThread):
    table_changed = QtCore.pyqtSignal(str, int, int)
    add_log = QtCore.pyqtSignal(str)

    def __init__(self, parent, window):
        super().__init__(parent)
        self.window = window

    # SMTP Authentication
    def auth_mail(self, user_id, user_pw):
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            try:
                # TLS 보안 연결
                server.starttls()
                # SMTP 로그인 테스트 (성공)
                server.login(user_id, user_pw)

                return True
            except:
                return False

    def run(self):
        self.add_log.emit('계정 사용가능 여부 체크 시작')
        idx = 0
        
        while idx < self.window.num_of_row_account:
            user_id = self.window.tableAccount.item(idx, 0).text()
            user_pw = self.window.tableAccount.item(idx, 1).text()
            ret = self.auth_mail(user_id, user_pw)

            # 시그널
            if ret:
                self.table_changed.emit('Account', idx, 1)
            else:
                self.table_changed.emit('Account', idx, 0)

            # 인덱스
            idx = idx + 1
            time.sleep(0.5)

        self.add_log.emit('계정 사용가능 여부 체크 완료')

class MailThread(QtCore.QThread):
    add_log = QtCore.pyqtSignal(str)

    def __init__(self, parent, window):
        super().__init__(parent)
        self.window = window
        self.working = True

    # Send Mail
    def send_mail(self, user_id, user_pw, msg):
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            try:
                # TLS 보안 연결
                server.starttls()
                # SMTP 로그인 테스트 (성공)
                server.login(user_id, user_pw)

                # 메일 전송
                res = server.sendmail(msg['From'], msg['To'], msg.as_string())
                if not res:
                    self.add_log.emit('{0} → {1} 전송 완료'.format(user_id, msg['To'].split('@')[0]))
                else:
                    self.add_log.emit('{0} → {1} 전송 실패'.format(user_id, msg['To'].split('@')[0]))
            except:
                self.add_log.emit('{0} → {1} 전송 실패'.format(user_id, msg['To'].split('@')[0]))

    def run(self):
        self.add_log.emit('메일 발송 시작')

        # 종료 플래그
        is_finish = False

        id_idx = 0  # 계정 인덱스
        bg_idx = 0  # 블로거 인덱스
        num_combobox = int(self.window.comboBox.currentText())

        while id_idx < self.window.num_of_row_account and self.working:
            # 모두 완료했으면 반복문 빠져 나옴
            if is_finish:
                break
            # 사용가능 여부가 O인 경우
            if self.window.tableAccount.item(id_idx, 2).text() == 'O':
                cb_idx = 0
                # 계정마다 초기 정한 횟수만큼 반복
                while cb_idx < num_combobox and self.working:
                    if bg_idx < self.window.num_of_row_blogger:
                        # Message 생성
                        subject = self.window.txtSubject.text()
                        content = self.window.txtContent.toPlainText()
                        msg = MIMEText(_text=content, _charset='utf-8')
                        msg['Subject'] = subject
                        sender = self.window.tableAccount.item(id_idx, 0).text() + '@naver.com'
                        receiver = self.window.tableBlogger.item(bg_idx, 0).text() + '@naver.com'
                        msg['From'] = sender
                        msg['To'] = receiver
                        # Message 보내기
                        naver_id = self.window.tableAccount.item(id_idx, 0).text()
                        naver_pw = self.window.tableAccount.item(id_idx, 1).text()
                        self.send_mail(naver_id, naver_pw, msg)
                        # Index 증가
                        cb_idx = cb_idx + 1
                        bg_idx = bg_idx + 1
                        time.sleep(0.2)
                    else:
                        is_finish = True
                        break

            # 네이버 계정 인덱스 증가
            id_idx = id_idx + 1

        self.add_log.emit('메일 발송 완료')

    def stop(self):
        self.add_log.emit('메일 발송 중단 요청 - 1초 딜레이')
        self.working = False
        self.quit()
        self.wait(1000)