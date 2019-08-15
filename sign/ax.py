import unittest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
d = webdriver.Chrome()
d.implicitly_wait(30)
d.get('http://opc-staging.ehsy.com/admin/index.php?route=sale/order')
d.maximize_window()
d.find_element_by_name('username').send_keys('admin')
d.find_element_by_name('password').send_keys('Ehsy2019')
d.find_element_by_xpath('//form/div[4]/button').submit()
d.find_element_by_xpath('//div[1]/div/div/a[3]').click()
d.find_element_by_xpath('//*[@id="images_order"]/div[2]/button').click()
s = """var el=document.getElementsByClassName('btn-opc-file'); el.before('<input data-upload-type="file" data-upload-model="oc" style="cursor:pointer;" class="btn-opc-file">')"""
d.execute_script(s)
d.find_element_by_xpath('//*[@id="image-new-order-row0"]/div/a[1]').send_keys(r'C:\Users\rick_zhang\Desktop\www.png')
# ActionChains(d).send_keys(r'C:\Users\rick_zhang\Desktop\www.png')
# ActionChains(d).send_keys(Keys.ENTER)
