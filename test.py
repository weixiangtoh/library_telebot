import time
from selenium import webdriver

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')
# driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe", chrome_options=options)

# driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')  # Optional argument, if not specified will search path.
# driver.get('http://www.google.com/')
# time.sleep(5) # Let the user actually see something!
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!
# driver.quit()

# URL = "https://library.smu.edu.sg/"

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()