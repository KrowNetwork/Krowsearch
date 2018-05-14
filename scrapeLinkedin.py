from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

page_start = 0
pages = 11

terms = ["computer science", "software developer", "mechanical engineer", "marketing", "business", "financial analyst", "insurance", "engineer", "machine learning", "data science", "civil engineer", "artist", "graphic designer", "business analyst", "recruiter", "chef"]
# initialize Selenium Web Driver
print ("Expected docs: %s" % (pages * len(terms) * 6))
titles = []
companies = []
descriptions = []
# data = pd.read_csv('data.csv')
data = pd.DataFrame({
    "company": companies,
    "title": titles,
    "description": descriptions
})
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

    try:
        driver.find_element_by_xpath('//*[@id="jobs-nav-item"]/a/span[2]').click()
    except:
        _ = input("Press any key after proving youre not a robot to linkedin")
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
    titles = []
    companies = []
    descriptions = []
    for i in list_jobs:
        driver.get(i)
        print (count)
        count += 1
        time.sleep(1)
        try:
            titles.append(driver.find_element_by_xpath('//div[@class="ember-view"]/div[5]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/h1').text)
            companies.append(driver.find_element_by_xpath('//div[@class="ember-view"]/div[5]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/h3/a').text)
            driver.find_element_by_xpath('//*[@aria-controls="job-details"]').click()
            descriptions.append(driver.find_element_by_xpath('//*[@id="job-details"]').text)
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

    d2 = pd.DataFrame({
        "company": companies,
        "title": titles,
        "description": descriptions
    })
    data = pd.concat([data, d2])
    data.to_csv('data.csv')
    driver.quit()


data.to_csv('data.csv')
# for index in driver.find_element_by_css_selector(".card-list.card-list--column.jobs-search-results__list"):
#     print (index)
# //*[@id="ember1022"]/div[6]/div[4]/div[2]/div[3]/div[1]/div/div/div/div/ul
# //*[@id="ember1022"]/div[6]/div[4]/div[2]
