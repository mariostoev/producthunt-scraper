import requests
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# Initialize the WebDriver

BASE_URL = 'https://www.producthunt.com'
TIME_TRAVEL_URL = 'https://www.producthunt.com/time-travel'


class Product:
    def __init__(self, ph_url, company_url, name, featured_date, tagline, ranking, upvotes,
                 product_category, comments, description, makers):
        self.ph_url = ph_url
        self.company_url = company_url
        self.name = name
        self.featured_date = featured_date
        self.tagline = tagline
        self.description = description
        self.ranking = ranking
        self.upvotes = upvotes
        self.product_category = product_category
        self.comments = comments
        self.makers = makers


def get_today_date():
    """ Returns the today's date at %Y/%m/%d format. """
    today = datetime.date.today()
    formatted_date = today.strftime("%Y/%m/%d")

    return formatted_date


def get_products_of_the_day_urls(date):
    driver = webdriver.Chrome(options=chrome_options)
    time_travel_url = f'{TIME_TRAVEL_URL}/{date}'
    driver.get(time_travel_url)

    for _ in range(5):
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for a brief period to allow content to load
        time.sleep(2)

    html_content = driver.execute_script("return document.documentElement.outerHTML;")
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.select('#__next > div.layoutContainer > div > div > div:nth-child(3)')

    product_urls = []
    for product in list(products[0].contents):
        product_url = product.find('a')['href']
        product_urls.append(f'{BASE_URL}{product_url}')

    return product_urls


def get_product_information(product_url):
    page = requests.get(product_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    res = soup.find('script', {'id': '__NEXT_DATA__'})
    json_object = json.loads(res.contents[0])

    try:
        id = product_ids = ' '.join(
             [x if x.startswith('Post') else '' for x in list(json_object['props']['apolloState'].keys())]).split()[-1]
        ph_url = product_url
        company_url = json_object['props']['apolloState'][' '.join(
                      [x if x.startswith('ProductLink') else '' for x in
                      list(json_object['props']['apolloState'].keys())]).split()[0]]['websiteName']
        name = json_object['props']['apolloState'][id]['name']
        featured_date = json_object['props']['apolloState'][id]['featuredAt'].split('T')[0].replace('-', '/')
        tagline = json_object['props']['apolloState'][id]['tagline']
        description = json_object['props']['apolloState'][id]['description']
        ranking = json_object['props']['apolloState'][id]['dailyRank']
        upvotes = json_object['props']['apolloState'][id]['votesCount']
        product_category = json_object['props']['apolloState'][id]['structuredData']['applicationCategory']
        comments = json_object['props']['apolloState'][id]['commentsCount']
        """
        reviews = json_object['props']['apolloState'][id]['reviewsCount']
        reviews_rating = json_object['props']['apolloState'][id]['reviewsRating']
        followers = json_object['props']['apolloState'][id]['followersCount']
        """

        makers = [author['name'] for author in json_object['props']['apolloState'][id]['structuredData']['author']]

        return Product(
            ph_url=ph_url,
            company_url=company_url,
            name=name,
            featured_date=featured_date,
            tagline=tagline,
            description=description,
            ranking=ranking,
            upvotes=upvotes,
            product_category=product_category,
            comments=comments,
            makers=makers
        )
    except KeyError:
        return 0


def get_products_of_the_day(date=False):

    if not date:
        today = datetime.date.today()
        date = today.strftime("%Y/%m/%d")

    product_data = []
    for product_url in get_products_of_the_day_urls(date):
        product_data.append(get_product_information(product_url))

    return product_data
