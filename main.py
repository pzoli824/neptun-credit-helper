from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#TODO: change namings later to camel case
#TODO: extract magic strings
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options)

driver.get("https://neptun.szte.hu/hallgato/login.aspx")

usernameInput = driver.find_element(By.ID, "user")
usernameInput.clear()
usernameInput.send_keys("username")

passwordInput = driver.find_element(By.ID, "pwd")
passwordInput.clear()
passwordInput.send_keys("password")

submitLogin = driver.find_element(By.ID, "btnSubmit")
submitLogin.click()

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
            print(rows[i])

    finally:
        # Logout
        print("should logout")
        driver.find_element(By.ID, "lbtnQuit").click()
        #driver.quit()

except TimeoutException:
    driver.quit()

#driver.quit()

