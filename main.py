from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from pkg.providers.browser import BrowserFactory, BrowserType
from pkg.providers.neptun import Neptun, University

browser = BrowserFactory.create_browser(BrowserType.CHROME)
driver = browser.driver

neptun = Neptun(browser, University.SZTE)
neptun.login("username", "password")

try:
    #TODO: probably not needed to store in a variable, check when refactoring
    authPage = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "function_tableheader"))
    )
    driver.get("https://neptun.szte.hu/hallgato/main.aspx?ismenuclick=true&ctrl=02101")
    # click to set query for all subjects
    driver.find_element(By.ID, "upFilter_rbtnCompleted_0").click()
    # start the query
    driver.find_element(By.ID, "upFilter_expandedsearchbutton").click()

    try:
        # wait for results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "head_Code"))
        )
        rows = driver.find_elements(By.XPATH, "//*[contains(@id, 'tr__')]")
        print(len(rows))
        for i in range(len(rows)):
            #magic happens here
            #datas.append(rows[i].text)
            print(rows[i].text)
            tds = rows[i].find_elements(By.XPATH, ".//td")
            print(len(tds))
            for j in range(len(tds)):
                print(j, ' ' + tds[j].text)
            #print(tds[6].text)


    finally:
        # Logout and close chrome
        driver.find_element(By.ID, "lbtnQuit").click()
        driver.quit()

except TimeoutException:
    driver.quit()

#driver.quit()
