from dataclasses import dataclass
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        # 'mars_news': mars_news(browser),
        'featured_image': featured_image(browser),
        'mars_facts': mars_facts(),
        'hemispheres': hemispheres(browser)
    }
    browser.quit()
    return data
# def mars_news(browser):
#     url = "https://redplanetscience.com"
#     browser.visit(url)
#     html = browser.html
#     soup = bs(html, "html.parser")
#     elements = soup.find_all('div', class_="list_text")
#     news = []
#     for item in elements:
#         title = item.find("div", class_="content_title").text
#         preview = item.find("div", class_="article_teaser_body").text
#         news_dict = {}
#         news_dict["title"] = title
#         news_dict["preview"] = preview
#         news.append(news_dict)
#     return news

def mars_news(browser):
    
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = bs(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    url = "https://spaceimages-mars.com"
    browser.visit(url)
    button = browser.find_by_tag("button")[1]
    button.click()
    img_soup = bs(browser.html, "html.parser")
    try:
        img_url = img_soup.find('img', class_="fancybox-image").get("src")
    except AttributeError:
        return None
    src_url = f'https://spaceimages-mars.com/{img_url}'
    return src_url
def mars_facts():
    try:
        mars_df = pd.read_html("https://galaxyfacts-mars.com/")[0]
    except BaseException:
        return None
    mars_df.columns = ["description", "mars", "earth"]
    mars_df.set_index("description", inplace=True)
    mars_df.to_html()
    return mars_df.to_html(classes='table table-striped')
def hemispheres(browser):
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)
    hemispheres = []
    for item in range(4):
        #Click into image
        browser.find_by_css("a.product-item img")[item].click()
        #Get title
        title = browser.find_by_css('h2.title').text
        #Get image url
        element= browser.links.find_by_text("Sample").first
        img_url = element["href"]
        #Adding to dictionary
        hemisphere_dict = {}
        hemisphere_dict["title"] = title
        hemisphere_dict["img_url"] = img_url
        hemispheres.append(hemisphere_dict)
        browser.back()
    return hemispheres
if __name__ == '__main__':
    print(scrape_all())
