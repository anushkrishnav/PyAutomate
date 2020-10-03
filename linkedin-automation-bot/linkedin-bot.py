# importing necessary libraries
import random
import time
from selenium import webdriver
from bs4 import BeautifulSoup

# creating browser window
browser = webdriver.Chrome('driver/chromedriver.exe')

# opening linkedin login page
browser.get('https://www.linkedin.com/uas/login')

# opening config.txt with email, password and number of profiles to visit
file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]
user_profile_link = lines[2]

# filling username and password
elementID = browser.find_element_by_id('username')
elementID.send_keys(username)
elementID = browser.find_element_by_id('password')
elementID.send_keys(password)

# visiting user profile
profile_to_visit = user_profile_link
full_link = 'https://www.linkedin.com/' + profile_to_visit
browser.get(full_link)

# initializing profiles_visited and profiles_to_visit
profiles_visited = []
profiles_to_visit = []


def getProfilesToVisit(soup, profiles_to_visit):
    """
     Gets list of profiles also viewed section and stores the link
    in a list.

    soup: The source code of the page.

    profile_to_visit: list of profiles to visit.
    """
    profileIDS = []
    people_also_viewed = soup.find('div', {'class': 'pv-browsemap-section'})
    all_links = people_also_viewed.findAll(
        'a', {'class': 'pv-browsemap-section__member ember-view'})

    for link in all_links:
        userID = link.get('href')
        if ((userID not in profiles_to_visit) and userID not in profiles_visited):
            profileIDS.append(userID)
    return profileIDS


def getUserName(soup):
    """
    Gets username of the pesron you want to connect to.

    soup: The source code of the page.
    """
    name_soup = soup
    name_div = name_soup.find('div', {'class': 'flex-1 mr5'})
    name_loc = name_div.find_all('ul')
    name = name_loc[0].find('li').get_text().strip()
    return name


# passing links to profiles_to_visit
profiles_to_visit = getProfilesToVisit(
    BeautifulSoup(browser.page_source, 'lxml'), profiles_to_visit)

# initializing the count of profiles visited
profile_visited_count = 0

# start loop for connecting
while profiles_to_visit:
    try:
        profile_to_visit = profiles_to_visit.pop()
        profiles_visited.append(profile_to_visit)
        full_link = 'https://www.linkedin.com' + profile_to_visit
        browser.get(full_link)



        browser.find_element_by_class_name('pv-s-profile-actions').click()

        browser.find_element_by_xpath(
            "//button[@class='mr1 artdeco-button artdeco-button--muted artdeco-button--3 artdeco-button--secondary ember-view']").click()

        connection_name = getUserName(
            BeautifulSoup(browser.page_source, 'lxml'))

        custom_message = "Hey! " + connection_name + \
                         ", I see we have mutual interest and I would be really happy to connect with you. So it would be great if you accept my connection. Thanks!!"

        elementID = browser.find_element_by_id('custom-message')
        elementID.send_keys(custom_message)

        browser.find_element_by_xpath(
            "//button[@class='ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view']").click()

        with open('profiles_visited.txt', 'a') as profiles_visited_file:
            profiles_visited_file.write(str(profile_to_visit) + '\n')
        profiles_visited_file.close()

        time.sleep(random.uniform(3, 10))

    except:
        continue
