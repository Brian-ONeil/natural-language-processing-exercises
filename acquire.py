###imports

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

import re
import os
import json
from pprint import pprint 

###functions

def scrape_codeup_blog():
    # Define headers
    headers = {'User-Agent': 'Codeup Data Science'}

    # Scrape blog homepage for links
    url = "https://codeup.com/blog/"
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    more_links = soup.find_all('a', class_='more-link')
    
    # Extract the links into a list
    links_list = [link['href'] for link in more_links]
    
    # Loop through the links to collect all of the articles' info
    article_info = []
    for link in links_list:
        response = get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        info_dict = {
            "title": soup.find("h1").text,
            "link": link,
            "date_published": soup.find('span', class_="published").text,
            "content": soup.find('div', class_="entry-content").text
        }
        article_info.append(info_dict)
    
    return links_list, article_info

def get_blog_articles(article_list):
    """brings in CodeUp blog posts to get title, date, and content. Runs a 'for' loop to get each article, loads into dictionary, appends and creates json file.
    To call: article_info = get_blog_articles(links_list)
            article_info
    """
    file = "blog_posts.json"
    
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
        
    
    headers = {'User-Agent': 'Codeup Data Science'}
    article_info = []

    for article in article_list:
        response = get(article, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        info_dict = {"title":soup.find("h1").text,
                    "link": article,
                    "date_published":soup.find('span', class_="published").text,
                    "content": soup.find('div', class_="entry-content").text}
        article_info.append(info_dict)
    
    with open(file, "w") as f:
        json.dump(article_info, f)
        
    return article_info

def scrape_one_page(topic):
#topic = "business"
    '''call function: 
    business_test = scrape_one_page("business")
    business_test[0]
    '''
    base_url = "https://inshorts.com/en/read/"

    response = get(base_url + topic)

    soup = BeautifulSoup(response.content, 'html.parser')

    titles = soup.find_all('span', itemprop="headline")

    summaries = soup.find_all('div', itemprop="articleBody")

    summary_list = []

    for i in range(len(titles)):
        temp_dict = {"category": topic,
                    "title": titles[i].text,
                    "content": summaries[i].text}

        summary_list.append(temp_dict)

    return summary_list

def get_news_articles(topic_list):
    """
    call function: topics = ['business', 'sports', 'technology', 'entertainment']

    final_list = get_news_articles(topics)
    final_list[50]
    
    """
    file = "news_articles.json"
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)

    final_list = []

    for topic in topic_list:
        final_list.extend(scrape_one_page(topic))
    
    with open(file, "w") as f:
        json.dump(final_list, f)
        
    return final_list

