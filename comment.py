import time
import pyperclip

# Selenium Library
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Auto Installer
import chromedriver_autoinstaller

# Beautiful Soup
from bs4 import BeautifulSoup

# PyQt Library
from PyQt5 import QtCore, QtWidgets


class CommentThread(QtCore.QThread):
    add_log = QtCore.pyqtSignal(str)

    def __init__(self, parent, window):
        super().__init__(parent)
        self.window = window
        self.working = True

    # xpath 유효성 검증 메소드
    def has_xpath(self, xpath, driver):
        try:
            driver.find_element_by_xpath(xpath)
            return True
        except:
            return False

    def run(self):
        self.add_log.emit('댓글 작성 시작')

        # Selenium Driver 생성
        chromedriver_autoinstaller.install(cwd=True)
        time.sleep(1)
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--app=http://www.google.com')
        driver = webdriver.Chrome(chrome_options=options)

        # 네이버 로그인
        driver.get(url='https://www.naver.com/')
        driver.find_element_by_xpath('//*[@id="account"]/a').click()
        time.sleep(1)
        pyperclip.copy(self.window.tableAccount.item(0, 0).text())
        driver.find_element_by_xpath('//*[@id="id"]').send_keys(Keys.CONTROL, 'v')
        time.sleep(1)
        pyperclip.copy(self.window.tableAccount.item(0, 1).text())
        driver.find_element_by_xpath('//*[@id="pw"]').send_keys(Keys.CONTROL, 'v')
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="log.login"]').click()
        time.sleep(2)

        # 블로그 메인 페이지 진입
        bg_idx = 0
        while self.working and bg_idx < self.window.num_of_row_blogger:
            blogger = self.window.tableBlogger.item(bg_idx, 0).text()
            driver.get(url='https://blog.naver.com/PostList.nhn?blogId=' + blogger + '&skinType=&skinId=&from=menu')
            # 컨텐츠 및 댓글 조작
            content = self.window.txtContent.toPlainText()

            # # 1개 댓글 = //*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div
            if self.has_xpath('//*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div', driver):
                # Extract Tags using BeautifulSoup
                bs = BeautifulSoup(driver.page_source, 'html.parser')
                try:
                    if bs.select('.wrap_postcomment > div')[0]['class'][0] == 'area_comment':
                        driver.find_element_by_xpath('//*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div').click()
                        post_id = bs.select('.blog2_post_function > a')[0]['id'].replace('copyBtn_', '')
                        pyperclip.copy(content)

                        # Comment + Secret Click
                        time.sleep(0.5)
                        driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '__write_textarea"]').send_keys(' ')
                        driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '__write_textarea"]').send_keys(Keys.CONTROL, 'v')
                        time.sleep(0.5)
                        driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '__write_textarea_secret_check"]').click()
                        time.sleep(0.5)
                        driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '"]/div/div[5]/div[1]/form/fieldset/div/div/div[6]/button').click()
                        
                        self.add_log.emit('{0} 블로그 댓글 달기 성공'.format(blogger))
                    else:
                        driver.find_element_by_xpath('//*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div[2]').click()
                        post_id = bs.select('.blog2_post_function > a')[0]['id'].replace('copyBtn_', '')
                        pyperclip.copy(content)

                        # Comment + Secret Click
                        time.sleep(0.5)
                        driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '__write_textarea"]').send_keys(' ')
                        driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '__write_textarea"]').send_keys(Keys.CONTROL, 'v')
                        time.sleep(0.5)
                        driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '__write_textarea_secret_check"]').click()    
                        time.sleep(0.5)
                        driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '"]/div/div[5]/div[1]/form/fieldset/div/div/div[6]/button').click()

                        self.add_log.emit('{0} 블로그 댓글 달기 성공'.format(blogger))
                except:
                    # 댓글/공감 기능을 막아놓음
                    self.add_log.emit('{0} 블로그는 댓글을 달 수 없습니다.'.format(blogger))
            else:
                # 글이 아예 없는 경우 + 댓글/공감 기능을 막아놓음
                self.add_log.emit('{0} 블로그는 댓글을 달 수 없습니다.'.format(blogger))

            bg_idx = bg_idx + 1
            time.sleep(2)

        driver.close()
        self.add_log.emit('댓글 작성 완료')

    def stop(self):
        self.add_log.emit('댓글 작성 중단 요청 - 1초 딜레이')
        self.working = False
        self.quit()
        self.wait(1000)