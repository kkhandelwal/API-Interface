#!/usr/bin/python
# __author__ = 'Kuldeep'


import urllib
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urlparse import parse_qsl

# Parameters of your app and the id of the profile you want to mess with.
FACEBOOK_APP_ID     = '000000027567380'
FACEBOOK_APP_SECRET = '000000000000000041ed597711efe65'
FACEBOOK_PROFILE_ID = '000000411674490'
REDIRECT_URL        = 'http://www.yourapp.com'
CHROME_DRIVER_LOC   = 'C://Python27/Scripts/chromedriver.exe'
oauth_args = dict(client_id     = FACEBOOK_APP_ID,
                  response_type    = 'token')

class FacebookInterface:
    """ Class provides various methods for interaction with Facebook   """
    
    def __init__(self):
        """
        | Library | FacebookInterface | 
        """

    def get_fb_user_access_token(self, username, password):
        oauth_access_token_cmd = 'https://www.facebook.com/dialog/oauth?redirect_uri=%s&' %REDIRECT_URL + urllib.urlencode(oauth_args)
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_LOC)
        driver.get(oauth_access_token_cmd)
        driver.find_element_by_id('email').send_keys(username)
        driver.find_element_by_id('pass').send_keys(password)
        driver.find_element_by_name('login').click()

        wait = WebDriverWait(driver, 50)
        element = wait.until(EC.title_contains(u'YouAppName'))
        return parse_qsl(driver.current_url)[0][1]
        driver.quit()

if __name__=='__main__':
    FB = FacebookInterface()
    token = FB.get_fb_user_access_token('testuser6534vcasgfsa@gmail.com', 'mychagepadssghsugeh')
    print token
