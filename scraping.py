# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = mars_hemispheres(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        'news_title':news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'hemispheres': hemisphere_image_urls,
        'last_modified': dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)


    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Convert the browser to a soup object and then quit the browser
    html = browser.html
    news_soup = soup (html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent elemet to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
         return None, None  
    

    return news_title, news_p

# ## Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full iumage button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url    


# ## Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        #use 'read_html' to scrape the facts into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign the columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrip
    return df.to_html(classes="table table-striped")


# ## Scrape High-Resolution Mars' Hemisphere Images and Titles

def mars_hemispheres(browser):

    # ### Hemispheres


    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []


    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_soup


    # results returned as an interable list
    img_link=img_soup.find_all('div', class_="item")
    img_link


    # Create for loop to iterate through list
    for img in img_link:
        ref=img.find('a', class_="result-title")
        hem_link=img.a['href']
        img_url = f'https://marshemispheres.com/{hem_link}'
        browser.visit(img_url)
        html = browser.html
        img_soup2 = soup(html, 'html.parser')
        hem_title = img_soup2.find("h2", class_="title").get_text()
        hem_full_img = img_soup2.find("img", class_="wide-image").get("src")
        hem_img_url = f'https://marshemispheres.com/{hem_full_img}'
        hemispheres={"img_url":hem_img_url, "title":hem_title}
        hemisphere_image_urls.append(hemispheres)
        browser.back()


    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())
