from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

page_start = 0
pages = 2

terms = ["software developer", "mechanical engineer"]
# initialize Selenium Web Driver

titles = []
companies = []
descriptions = []
for term in terms:
    num_start = 6 * page_start

    driver = webdriver.Chrome("chromedriver.exe")

    driver.get("https://www.linkedin.com/uas/login")

    username = driver.find_element_by_name('session_key')
    username.send_keys("tuckers@goldmedalfitness.com")

    password = driver.find_element_by_id("session_password-login")
    password.send_keys("krownetwork")

    driver.find_element_by_xpath('//*[@id="btn-primary"]').click()

    time.sleep(5)

    driver.find_element_by_xpath('//*[@id="jobs-nav-item"]/a/span[2]').click()

    driver.find_element_by_xpath('//*[starts-with(@id, "jobs-search-box-keyword")]').send_keys(term)
    driver.find_element_by_xpath('//*[starts-with(@id, "jobs-search-box-keyword")]').send_keys(Keys.ENTER)
    driver.find_element_by_xpath('//*[starts-with(@id, "jobs-search-box-location")]').send_keys(Keys.ENTER)

    if num_start != 0:
        driver.get(driver.current_url + "&start=%s" % num_start)
    list_jobs = []

    for i in range(pages):
        time.sleep(3)
        jobs = driver.find_element_by_xpath('//div[@class="ember-view"]/div[6]/div[4]/div[2]/div[3]/div[1]/div/div/div/div/ul')
        j = jobs.find_elements_by_tag_name("li")[:6]
        for x in j:
            list_jobs.append(x.find_element_by_tag_name("a").get_attribute('href'))
        num_start += 6
        driver.get(driver.current_url + "&start=%s" % num_start)
        print ("Number scraped: %s" % len(list_jobs))


    count = 1
    for i in list_jobs:
        driver.get(i)
        print (count)
        count += 1
        time.sleep(1)
        try:
            titles.append(driver.find_element_by_xpath('//div[@class="ember-view"]/div[5]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/h1').text)
            companies.append(driver.find_element_by_xpath('//div[@class="ember-view"]/div[5]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/h3/a').text)
            descriptions.append(driver.find_element_by_xpath('//*[@id="company-description-text"]').text)
        except:
            print ([len(titles), len(companies), len(descriptions)])
            if len(titles) != len(companies) or len(companies) != len(descriptions):
                min_l = min([len(titles), len(companies), len(descriptions)])
                print ([len(titles), len(companies), len(descriptions)])
                print (min_l)
                titles = titles[:min_l]
                companies = companies[:min_l]
                descriptions = descriptions[:min_l]
                print ([len(titles), len(companies), len(descriptions)])
            print ("Failed")
            continue

    driver.quit()

data = pd.DataFrame({
    "company": companies,
    "title": titles,
    "description": descriptions
})
data.to_csv('data.csv')
# for index in driver.find_element_by_css_selector(".card-list.card-list--column.jobs-search-results__list"):
#     print (index)
# //*[@id="ember1022"]/div[6]/div[4]/div[2]/div[3]/div[1]/div/div/div/div/ul
# //*[@id="ember1022"]/div[6]/div[4]/div[2]
