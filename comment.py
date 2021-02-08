import time
import pyperclip

# Selenium Library
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Auto Installer
import chromedriver_autoinstaller

# Beautiful Soup
from bs4 import BeautifulSoup



path = chromedriver_autoinstaller.install()
driver = webdriver.Chrome(executable_path=path)

# ID/PW 로드 (테스트)
idx = 0
id = ''
pw = ''
with open('test.txt', mode='rt', encoding='utf-8') as f:
    for i in f.readlines():
        if idx == 1:
            break
        temp = i.splitlines()[0].split(' ') 
        id = temp[0]
        pw = temp[1]

        idx = idx + 1


# 네이버 로그인
driver.get(url='https://www.naver.com/')
driver.find_element_by_xpath('//*[@id="account"]/a').click()
time.sleep(1)
pyperclip.copy(id)
driver.find_element_by_xpath('//*[@id="id"]').send_keys(Keys.CONTROL, 'v')
time.sleep(1)
pyperclip.copy(pw)
driver.find_element_by_xpath('//*[@id="pw"]').send_keys(Keys.CONTROL, 'v')
time.sleep(1)
driver.find_element_by_xpath('//*[@id="log.login"]').click()
time.sleep(2)

# xpath 유효성 검증 메소드
def has_xpath(xpath, driver):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False

# 블로그 메인 페이지 진입
blogger = 'nohack-'
driver.get(url='https://blog.naver.com/PostList.nhn?blogId=' + blogger + '&skinType=&skinId=&from=menu')

# 글 여부 확인, 댓글 작성 가능성 체크, 댓글 작성, 확인
# 글이 없는 경우, 글은 있지만 댓글버튼 없는 경우, 글이 있고 댓글 버튼 있는 경우
# 본문 진입 했는데 한 페이지에 글이 여러 개 띄워져 있는 경우 << 가장 최신 글에 작성
# xpath 검증 필요해 보임

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
# 1개 댓글 = //*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div
if has_xpath('//*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div', driver):
    # Extract Tags using BeautifulSoup
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        # True = Only Comment, False = Sympathy and Comment
        if bs.select('.wrap_postcomment > div')[0]['class'][0] == 'area_comment':
            print('댓글 O')
        else:
            print('댓글 공감 O')
    except:
        # 댓글, 공감 기능을 막아놓음
        print('기능 막아둠')
    
    # driver.find_element_by_xpath('//*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div').click()
    

    # tag = bs.select('.blog2_post_function > a')[0]['id'] # 이 본문 ID를 가지고 댓글 태그를 동적으로 열 수 있을듯?
    # post_id = tag.replace('copyBtn_', '')
    # time.sleep(1)
    # pyperclip.copy(content)
    # driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '__write_textarea"]').send_keys(Keys.CONTROL, 'v')
    # time.sleep(0.5)
    # driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '__write_textarea_secret_check"]').click()
    # time.sleep(0.5)
    # driver.find_element_by_xpath('//*[@id="naverComment_201_' + post_id + '"]/div/div[5]/div[1]/form/fieldset/div/div/div[6]/button').click()
else:
    # 둘다 없는 경우 걍 거름 (막아둔 것임)
    print('글이 아예 없음')

time.sleep(500)
driver.close()