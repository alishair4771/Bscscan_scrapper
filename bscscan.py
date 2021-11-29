from selenium import webdriver
from shutil import which
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from datetime import datetime




options = Options()
chrome_path = which("chromedriver")
driver = webdriver.Chrome(executable_path=chrome_path, options=options)

def scrape_bsc_reserves(url):
    driver.get(url)
    url = driver.current_url
    while (True):
        if url == driver.current_url:
            driver.switch_to.frame("readcontractiframe")
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#readCollapse8 > div > form > div > span:nth-child(7)")))
            div = driver.find_element_by_xpath("//*[@id='readCollapse8']/div/form/div").get_attribute("innerText")

            row1 = div.strip('reserve0 uint112, _reserve1 uint112, _blockTimestampLast uint32 _reserve0|uint112').strip()

            row2 = row1.replace(":","").strip("_reserve0|uint112")

            row3 = row2.replace(" _reserve1|uint112","")

            final = row3.replace("_blockTimestampLast|uint32", "")

            a = final.split("\xa0")
            t = ''.join(a)
            f = t.split("\n")


            date_data = datetime.now()
            output = {
                'date': date_data.strftime("%m/%d/%Y, %H:%M:%S"),
                'reserve0': f[0],
                'reserve1' : f[1]
            }
            print(output)
            driver.refresh()
        time.sleep(2)

scrape_bsc_reserves(url= "https://bscscan.com/address/0x7213a321F1855CF1779f42c0CD85d3D95291D34C#readContract")