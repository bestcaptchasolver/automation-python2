#!/usr/bin/python2.7

# Automation examples for bestcaptchasolver.com
# with browser and requests

from bestcaptchasolverapi2.bestcaptchasolverapi import *
from selenium import webdriver
import requests as req
from lxml import html
from time import sleep

# settings
ACCESS_TOKEN = 'BAC21DFA5FE5415CA9608BED45F8D703'
SLEEP = 10

# init bestcaptchasolverAPI object with access_token
bcs = BestCaptchaSolverAPI(ACCESS_TOKEN)

PAGES = {
    'image': 'https://bestcaptchasolver.com/automation/image',
    'recaptcha-v2': 'https://bestcaptchasolver.com/automation/recaptcha-v2',
    'recaptcha-invisible': 'https://bestcaptchasolver.com/automation/recaptcha-invisible'
}

# Image captcha automation with browser
def browser_image():
    print '[+] Image (classic) captcha automation with browser'
    print '---------------------------------'
    print '[+] Starting browser'
    url = PAGES['image']
    b = webdriver.Chrome()
    try:
        print '[+] Navigating to image captcha page'
        b.get(url)
        print '[+] Completing fields of form'
        b.find_element_by_id('username').send_keys('image-browser-user-123')
        captcha_image_b64 = b.find_element_by_id('automation-container').find_element_by_class_name('img-responsive').get_attribute('src')
        print '[+] Submitting image to bestcaptchasolver'

        # solve image captcha with bcs
        id = bcs.submit_image_captcha({     # submit image to bcs
            'image': captcha_image_b64
        })     # submit image captcha
        print '[+] Got ID {}, waiting for completion...'.format(id)
        text = None
        while text == None:
            text = bcs.retrieve(id)['text']
            if text != None: break      # don't even wait if completed
            sleep(10)
        print '[+] Typing response text from bcs: {}'.format(text)
        b.find_element_by_id('captcha-text').send_keys(text)    # write text received from bcs
        print '[+] Submitting form'
        b.find_element_by_id('automation_submit').click()       # submit form
        print '[+] Form submitted !'
        sleep(SLEEP)
    finally:
        b.quit()
        print '---------------------------------'

# Image captcha automation with requests
def requests_image():
    print '[+] Image (classic) captcha automation with requests'
    print '---------------------------------'
    try:
        s = req.session()
        url = PAGES['image']
        print '[+] Making request to get image captcha and set the cookie'
        resp = s.get(url).text
        # get image from response
        tree = html.fromstring(resp)        # use lxml to parse html, easier
        img = tree.xpath('//img')[1]        # get image we're interested in
        b64image = img.attrib['src']        # get b64/src from it
        print '[+] Got data needed from page, submitting captcha to bestcaptchasolver'
        # solve image captcha with BCS
        id = bcs.submit_image_captcha({  # submit image to bcs
            'image': b64image
        })  # submit image captcha
        print '[+] Got ID {}, waiting for completion...'.format(id)
        text = None
        while text == None:
            text = bcs.retrieve(id)['text']
            if text != None: break  # don't even wait if completed
            sleep(10)
        print '[+] Got captcha response from bcs: {}, submitting data to page'.format(text)

        # link gathered from page source
        resp = s.put('https://bestcaptchasolver.com/automation/image/verify', data={
            'username': 'image-requests-user-123',
            'text': text
        }).text
        print '[+] Response from site: ', resp
    finally:
        print '---------------------------------'

# reCAPTCHA v2 automation with browser
def browser_recaptchav2():
    print '[+] reCAPTCHA v2 automation with browser'
    print '---------------------------------'
    print '[+] Starting browser'
    url = PAGES['recaptcha-v2']
    b = webdriver.Chrome()
    try:
        print '[+] Navigating to reCAPTCHA v2 page'
        b.get(url)
        print '[+] Completing fields of form'
        b.find_element_by_id('username').send_keys('v2-browser-user-123')
        site_key = b.find_element_by_class_name('g-recaptcha').get_attribute('data-sitekey')
        print '[+] Submitting page_url with site_key to bestcaptchasolver'

        # solve image captcha with bcs
        id = bcs.submit_recaptcha({     # submit image to bcs
            'page_url': url,
            'site_key': site_key
        })     # submit image captcha
        print '[+] Got ID {}, waiting for completion...'.format(id)
        gresponse = None
        while gresponse == None:
            gresponse = bcs.retrieve(id)['gresponse']
            if gresponse != None: break      # don't even wait if completed
            sleep(10)
        print '[+] Setting gresponse from bcs: {}'.format(gresponse)
        b.execute_script('$("#g-recaptcha-response").val("{}")'.format(gresponse))        # set it through JS
        print '[+] Submitting form'
        b.find_element_by_id('automation_submit').click()       # submit form
        print '[+] Form submitted !'
        sleep(SLEEP)
    finally:
        b.quit()
        print '---------------------------------'

# reCAPTCHA v2 automation with requests
def requests_recaptchav2():
    print '[+] reCAPTCHA v2 automation with requests'
    print '---------------------------------'
    try:
        s = req.session()
        url = PAGES['recaptcha-v2']
        print '[+] Making request to get sitekey'
        resp = s.get(url).text
        # get image from response
        tree = html.fromstring(resp)        # use lxml to parse html, easier
        site_key = tree.xpath('//div[@class="g-recaptcha"]')[0].attrib['data-sitekey']        # get image we're interested in
        print '[+] Got site_key from page: {}, submitting captcha to bestcaptchasolver'.format(site_key)
        # solve image captcha with BCS
        id = bcs.submit_recaptcha({  # submit image to bcs
            'page_url': url,
            'site_key': site_key
        })  # submit image captcha
        print '[+] Got ID {}, waiting for completion...'.format(id)
        gresponse = None
        while gresponse == None:
            gresponse = bcs.retrieve(id)['gresponse']
            if gresponse != None: break  # don't even wait if completed
            sleep(10)
        print '[+] Got gresponse from bcs: {}, submitting data to page'.format(gresponse)

        # link gathered from page source
        resp = s.put('https://bestcaptchasolver.com/automation/recaptcha/verify', data={
            'username': 'v2-requests-user-123',
            'token': gresponse,
            'site_key': site_key
        }).text
        print '[+] Response from site: ', resp
    finally:
        print '---------------------------------'

# invisible reCAPTCHA automation with browser
def browser_invisible():
    print '[+] Invisible reCAPTCHA automation with browser'
    print '---------------------------------'
    print '[+] Starting browser'
    url = PAGES['recaptcha-invisible']
    b = webdriver.Chrome()
    try:
        print '[+] Navigating to invisible reCAPTCHA page'
        b.get(url)
        print '[+] Completing fields of form'
        b.find_element_by_id('username').send_keys('invisible-browser-user-123')
        site_key = b.find_element_by_class_name('g-recaptcha').get_attribute('data-sitekey')
        print '[+] Submitting page_url with site_key to bestcaptchasolver'

        # solve image captcha with bcs
        id = bcs.submit_recaptcha({     # submit image to bcs
            'page_url': url,
            'site_key': site_key,
            'type': '2'                 # set type to invisible
        })     # submit image captcha
        print '[+] Got ID {}, waiting for completion...'.format(id)
        gresponse = None
        while gresponse == None:
            gresponse = bcs.retrieve(id)['gresponse']
            if gresponse != None: break      # don't even wait if completed
            sleep(10)
        print '[+] Setting gresponse from bcs: {}'.format(gresponse)
        b.execute_script('check("{}")'.format(gresponse))        # execute callback method with token
        print '[+] Callback method executed / form submitted'
        sleep(SLEEP)
    finally:
        print '---------------------------------'
        b.quit()

# invisible reCAPTCHA automation with requests
def requests_invisible():
    print '[+] Invisible reCAPTCHA automation with requests'
    print '---------------------------------'
    try:
        s = req.session()
        url = PAGES['recaptcha-invisible']
        print '[+] Making request to get sitekey'
        resp = s.get(url).text
        # get image from response
        tree = html.fromstring(resp)        # use lxml to parse html, easier
        site_key = tree.xpath('//button[@class="g-recaptcha btn btn-primary btn-link btn-wd btn-lg"]')[0].attrib['data-sitekey']        # get image we're interested in
        print '[+] Got site_key from page: {}, submitting captcha to bestcaptchasolver'.format(site_key)
        # solve image captcha with BCS
        id = bcs.submit_recaptcha({  # submit image to bcs
            'page_url': url,
            'site_key': site_key,
            'type': '2'
        })  # submit image captcha
        print '[+] Got ID {}, waiting for completion...'.format(id)
        gresponse = None
        while gresponse == None:
            gresponse = bcs.retrieve(id)['gresponse']
            if gresponse != None: break  # don't even wait if completed
            sleep(10)
        print '[+] Got gresponse from bcs: {}, submitting data to page'.format(gresponse)

        # link gathered from page source
        resp = s.put('https://bestcaptchasolver.com/automation/recaptcha/verify', data={
            'username': 'invisible-requests-user-123',
            'token': gresponse,
            'site_key': site_key
        }).text
        print '[+] Response from site: ', resp
    finally:
        print '---------------------------------'


# Automate main method
def automate():
    try:
        print '[+] Automation started'
        browser_image()
        requests_image()

        browser_recaptchav2()
        requests_recaptchav2()

        browser_invisible()
        requests_invisible()
    except Exception, ex:
        print '[!] Error: {}'.format(ex)
    finally:
        print '[+] Automation finished !'

if __name__ == "__main__":
    automate()