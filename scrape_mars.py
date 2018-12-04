from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def mars_news():
    
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the article
    article = soup.find('div', class_='list_text')

    # Get the article title
    title = article.find('a').text
    print(f"Title: {title}")
    print("-------------------------------------------------")
    # Get the article content
    content = article.find('div', class_='article_teaser_body').text
    print(f"Content: {content}")

    # Store data in a dictionary
    article_data = {
        "article_title": title,
        "article_content": content
    }
    browser.quit()
    return article_data


def mars_space_images():
    #(https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    #* Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
    #* Make sure to find the image url to the full size `.jpg` image.
    #* Make sure to save a complete url string for this image.

    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser") 

    article = soup.find('div', class_='carousel_items')
    getting_image1 = article.find('article', class_='carousel_item')['style']
    featured_image_url = "https://www.jpl.nasa.gov" + getting_image1.split("'")[1]
    browser.quit()
    return featured_image_url

def mars_weather():
    
    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser") 
    mars_weather = soup.find('div', class_='js-tweet-text-container').text
    browser.quit()
    return mars_weather

def mars_facts():
    url = "http://space-facts.com/mars/"
    browser = init_browser()
    browser.visit(url)

    time.sleep(1)

        # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser") 

    table = soup.find('table', class_='tablepress tablepress-id-mars')
    td1 = table.find_all('td', class_="column-1")
    td2 = table.find_all('td', class_="column-2")
    col1 = [x.text for x in td1]
    col2 = [x.text for x in td2]
    browser.quit()
    d = {" ": col1, "Value": col2}
    df = pd.DataFrame(d)
    html_table = df.to_html(index=False)
    browser.quit()
    return html_table


def mars_hemispheres():

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser = init_browser()
    browser.visit(url)
    time.sleep(1)

    #Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser") 

    image = soup.find('div', class_='collapsible results')
    p1 = image.find_all('div', class_='description')

    titles = image.find_all('h3')
    titles_list = [x.text for x in titles]

    links = []
    for x in p1:
        links.append("https://astrogeology.usgs.gov" +  x.find('a', class_='itemLink product-item')['href'])

    image_links = []

    for x in links:
        browser = init_browser()
        browser.visit(x)
        time.sleep(1)
        html = browser.html
        soup1 = bs(html, "html.parser") 
        pic = soup1.find('div', class_='downloads')
        imageurl = pic.find('a')['href']
        image_links.append(imageurl)
        
        browser.quit()
    
    #make the dictionaries
    image1 = {"title":titles_list[0], "url": image_links[0]}
    image2 = {"title":titles_list[1], "url": image_links[1]}
    image3 = {"title":titles_list[2], "url": image_links[2]}
    image4 = {"title":titles_list[3], "url": image_links[3]}
    hemisphere_image_urls = [image1, image2, image3, image4]

    return hemisphere_image_urls


def scrape():
    news_dict = mars_news()
    image_url = mars_space_images()
    weather_tweet = mars_weather()
    facts_table = mars_facts()
    image_urls_dict = mars_hemispheres()
    complete_dict = {"Mars_News": news_dict, 
                     "Space_Images": image_url,
                     "Mars_Weather": weather_tweet,
                     "Mars_Facts": facts_table,
                     "Mars_Hemispheres": image_urls_dict}
    return complete_dict


