from turtle import title
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import googlemaps
import json


def switch_iframe(browser, iframe_xpath):
    browser.switch_to.default_content()  # iframe end
    iframe = browser.find_element(By.XPATH, iframe_xpath)
    browser.switch_to.frame(iframe)
    time.sleep(1.0)


def switch_to_iframe(browser):
    iframe = browser.find_element(By.XPATH, '//*[@id="searchIframe"]')
    browser.switch_to.frame(iframe)


def find_element_by_css_selector(browser, selector):
    try:
        result = browser.find_element(By.CSS_SELECTOR, selector).text
    except:
        result = ""
    return result


def get_browser():
    browser = webdriver.Chrome('C:\chromedriver.exe')
    return browser


def move_to_url(browser):
    url = "https://map.naver.com/v5/search/%ED%99%8D%EB%8C%80%20%EC%B9%B4%ED%8E%98%20%EC%B6%94%EC%B2%9C?c=14128354.8486428,4516221.3776633,14,0,0,0,dh"
    browser.get(url)
    browser.implicitly_wait(5)


def open_load_frame(browser):
    load_frame = browser.find_element(
        By.CSS_SELECTOR, '#container > shrinkable-layout > div > app-base > search-layout > div.main.-top_space.ng-star-inserted > combined-search-list > salt-search-list')
    load_frame.click()


def click_detail_page(link, browser):
    # 기존에 받았던 링크는 DOM이 변해서 사용할 수 없으므로 frame을 바꿀 때마다 새로 가져온다.
    sel_link = f"#_pcmap_list_scroll_container > ul > li:nth-child({link + 1}) > div._3hn9q > a > div.O9Z-o > div > span"
    link_obj = browser.find_element(By.CSS_SELECTOR, sel_link)
    link_obj.click()
    time.sleep(1.0)


def get_detail_page(link, browser):
    click_detail_page(link, browser)
    switch_iframe(browser, '//*[@id="entryIframe"]')


def click_open_time_list(browser):
    try:
        link_obj = browser.find_element(
            By.CSS_SELECTOR, "#app-root > div > div > div.place_detail_wrapper > div:nth-child(4) > div > div.place_section.no_margin > div > ul > li.Cqsis._1X-CS > div > a")
        link_obj.click()
        time.sleep(1.0)
    except:
        time.sleep(0)


def click_menu_container(browser):
    try:
        click_spans = browser.find_elements(
            By.CSS_SELECTOR, '#app-root > div > div > div.place_detail_wrapper > div.place_fixed_maintab > div > div > div > div > a')
    except:
        click_spans = browser.find_elements(
            By.CSS_SELECTOR, '#app-root > div > div > div.place_detail_wrapper > div.place_fixed_maintab > div > div > div > div > div > div:nth-child(2) > div > div > a')

    if len(click_spans) == 4:
        click_spans[1].click()
    else:
        click_spans[2].click()


def get_menu(browser):
    click_menu_container(browser)

    menu_list = []
    dic = {}

    menus = browser.find_elements(
        By.CSS_SELECTOR, '#app-root > div > div > div.place_detail_wrapper > div:nth-child(5) > div > div.place_section.no_margin > div.place_section_content > ul > li')

    for selector in menu_css_selectors:
        for menu in menus:
            menu_list.append(find_element_by_css_selector(menu, selector))

    length = (len(menu_list)+1) // 2
    for i in range(length):
        dic[menu_list[i]] = menu_list[i + length]

    return dic


def get_image(link, browser):
    image_link = f"#_pcmap_list_scroll_container > ul > li:nth-child({link + 1}) > div.zZGuI > div > a:nth-child(1) > div > div"

    try:
        image_obj = browser.find_element(
            By.CSS_SELECTOR, image_link).get_attribute('style')
        image_obj = image_obj.replace(
            'width: 100%; height: 112px; background-image: url("', '')
        image_obj = image_obj.replace('");', '')
    except:
        image_obj = ""

    return image_obj


def get_data_pack(browser, data_dic):
    data_dic["title"] = find_element_by_css_selector(
        browser, '#_title > span._3XamX')
    data_dic["rating"] = find_element_by_css_selector(
        browser, '#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR._2z4r0 > div._1kUrA > span._1Y6hi._1A8_M > em')
    data_dic["address"] = find_element_by_css_selector(
        browser, '#app-root > div > div > div.place_detail_wrapper > div:nth-child(4) > div > div.place_section.no_margin > div > ul > li._1M_Iz._1aj6- > div > a > span._2yqUQ')
    data_dic["telephone"] = find_element_by_css_selector(
        browser, 'div._1h3B_ > span._3ZA0S')


def get_open_time_list(browser):
    open_time_list = {}

    for i in range(2, 9):
        day = find_element_by_css_selector(
            browser, f'#app-root > div > div > div.place_detail_wrapper > div:nth-child(4) > div > div.place_section.no_margin > div > ul > li.Cqsis._1X-CS > div > a > div:nth-child({i}) > div > span > span')
        time = find_element_by_css_selector(
            browser, f'#app-root > div > div > div.place_detail_wrapper > div:nth-child(4) > div > div.place_section.no_margin > div > ul > li.Cqsis._1X-CS > div > a > div:nth-child({i}) > div > span > div')

        open_time_list[day] = time

    return open_time_list


def scroll_to_page_end(browser):
    for i in range(5):
        body_key = browser.find_element(By.CSS_SELECTOR, "body")
        body_key.send_keys(Keys.END)
        time.sleep(2.5)


def get_coordinates(name):
    gmaps = googlemaps.Client("AIzaSyC3bsg4iFMpI5OTgj2mGowB3IM3AWHp_II")

    try:

        geocode_result = gmaps.geocode("홍대 " + name, language='ko')

        latitude = geocode_result[0]["geometry"]["location"]["lat"]
        longitude = geocode_result[0]["geometry"]["location"]["lng"]

        return [latitude, longitude]
    except:
        return [0, 0]


def main():
    browser = get_browser()
    move_to_url(browser)

    open_load_frame(browser)
    switch_iframe(browser, '//*[@id="searchIframe"]')

    scroll_to_page_end(browser)

    columnList = browser.find_elements_by_css_selector("div._2ky45 > a")
    columnList.pop(0)

    total_data = []
    total_marker = []

    # for column in columnList:
    #     column.click()
    columnList[1].click()

    item_count = len(browser.find_elements(
        By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li'))

    for index in range(item_count):
        data_dic = {}
        marker_dic = {}

        data_dic["images"] = get_image(index, browser)
        get_detail_page(index, browser)
        click_open_time_list(browser)
        get_data_pack(browser, data_dic)
        data_dic["open_time"] = get_open_time_list(browser)
        data_dic["menus"] = get_menu(browser)
        data_dic["location"] = get_coordinates(data_dic["title"])

        print(data_dic)  # 확인용
        total_data.append(data_dic)

        marker_dic[data_dic["title"]] = data_dic["location"]
        total_marker.append(marker_dic)
        print(marker_dic)

        switch_iframe(browser, '//*[@id="searchIframe"]')

    with open(r"C:\Users\danha\Documents\GitHub\naver_search_crawling\crawling.py\1.py", 'w', encoding='utf-8') as combine_file:
        json.dump(total_data, combine_file, indent="\t", ensure_ascii=False)

if __name__ == '__main__':
    menu_css_selectors = [
        'a > div > div._25ryC > div > span',
        'a > div > div._3qFuX'
    ]

    main()
