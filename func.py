import time
import pyautogui
import pyperclip
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtWidgets

# Selenium Library
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Auto Installer
import chromedriver_autoinstaller


class PosThread(QtCore.QThread):
    update_pos = QtCore.pyqtSignal(int, int)

    def __init__(self, parent, window):
        super().__init__(parent)
        self.window = window
        self.working = True

    def run(self):
        while(self.working):
            x, y = pyautogui.position()
            self.update_pos.emit(x, y)

    def stop(self):
        self.working = False
        self.quit()
        self.wait(1000)

class CommentThread(QtCore.QThread):
    update_comment = QtCore.pyqtSignal(int, str)
    update_end = QtCore.pyqtSignal(int, str)
    update_progress = QtCore.pyqtSignal(int)

    def __init__(self, parent, window):
        super().__init__(parent)
        self.window = window
        self.working = True

    def run(self):
        # Pos 계산
        mouse_x_1 = int(self.window.txtPOS_1_X.text())
        mouse_y_1 = int(self.window.txtPOS_1_Y.text())
        mouse_x_2 = int(self.window.txtPOS_2_X.text())
        mouse_y_2 = int(self.window.txtPOS_2_Y.text())

        # Selenium Driver 생성
        chromedriver_autoinstaller.install(cwd=True)
        time.sleep(1)
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--app=http://www.google.com')
        self.driver = webdriver.Chrome(chrome_options=options)

        # 네이버 로그인
        self.driver.get(url='https://www.naver.com/')
        self.driver.find_element_by_xpath('//*[@id="account"]/a').click()
        time.sleep(1)
        pyperclip.copy(self.window.txtID.text())
        self.driver.find_element_by_xpath('//*[@id="id"]').send_keys(Keys.CONTROL, 'v')
        time.sleep(1)
        pyperclip.copy(self.window.txtPW.text())
        self.driver.find_element_by_xpath('//*[@id="pw"]').send_keys(Keys.CONTROL, 'v')
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="log.login"]').click()
        time.sleep(2)

        # 블로거 인덱싱
        bg_idx = 0
        while bg_idx < self.window.num_of_row:
            blogger = self.window.tableWidget.item(bg_idx, 0).text()
            self.driver.get(url='https://blog.naver.com/PostList.nhn?blogId=' + blogger + '&skinType=&skinId=&from=menu')
            print('{0}: {1}'.format(bg_idx, blogger))

            if self.has_xpath('//*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div', self.driver):
                # 태그 추출
                bs = BeautifulSoup(self.driver.page_source, 'html.parser')
                try:
                    # 공감 버튼 유무 체크
                    if bs.select('.wrap_postcomment > div')[0]['class'][0] == 'area_comment':
                        self.update_comment.emit(bg_idx, 'O')
                        self.driver.find_element_by_xpath('//*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div').click()
                        try:
                            post_id = bs.select('.blog2_post_function > a')[0]['id'].replace('copyBtn_', '')
                        except:
                            post_id = bs.select('.post-top p')[2]['id'].replace('url_' + blogger + '_', '')

                        time.sleep(0.5)
                        self.driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '__write_textarea_secret_check"]').click()
                        time.sleep(0.2)
                        self.driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '"]/div/div[5]/div[1]/form/fieldset/div/div/div[6]/div/span[1]/span[1]').click()
                        time.sleep(1)
                        pyautogui.click(x=mouse_x_1, y=mouse_y_1, button='left', clicks=1)
                        time.sleep(1)
                        pyautogui.click(x=mouse_x_2, y=mouse_y_2, button='left', clicks=2)
                        time.sleep(2.5)
                        self.driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id +'"]/div/div[5]/div[1]/form/fieldset/div/div/div[6]/button').click()

                        self.update_end.emit(bg_idx, '작성 완료')
                    else:
                        self.update_comment.emit(bg_idx, 'O')
                        try:
                            self.driver.find_element_by_xpath('//*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div[2]').click()
                        except:
                            self.driver.find_element_by_xpath('//*[@id="printPost1"]/tbody/tr/td[2]/div[4]/div[1]/div[2]').click()
                        try:
                            post_id = bs.select('.blog2_post_function > a')[0]['id'].replace('copyBtn_', '')
                        except:
                            post_id = post_id = bs.select('.post-top p')[2]['id'].replace('url_' + blogger + '_', '')

                        time.sleep(0.5)
                        self.driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '__write_textarea_secret_check"]').click()
                        time.sleep(0.2)
                        self.driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '"]/div/div[5]/div[1]/form/fieldset/div/div/div[6]/div/span[1]/span[1]').click()
                        time.sleep(1)
                        pyautogui.click(x=mouse_x_1, y=mouse_y_1, button='left', clicks=1)
                        time.sleep(1)
                        pyautogui.click(x=mouse_x_2, y=mouse_y_2, button='left', clicks=2)
                        time.sleep(2.5)
                        self.driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id +'"]/div/div[5]/div[1]/form/fieldset/div/div/div[6]/button').click()

                        self.update_end.emit(bg_idx, '작성 완료')
                except:
                    print('예외 발생')
                    self.update_comment.emit(bg_idx, 'X') 
            else:
                print('예외 발생')
                self.update_comment.emit(bg_idx, 'X')

            bg_idx = bg_idx + 1
            self.update_progress.emit(int((bg_idx/self.window.num_of_row)*100))
            time.sleep(2)

        self.driver.close()

    def stop(self):
        self.working = False
        self.driver.close()
        self.quit()
        self.wait(1000)

    # xpath 유효성 검증 메소드
    def has_xpath(self, xpath, driver):
        try:
            driver.find_element_by_xpath(xpath)
            return True
        except:
            return False