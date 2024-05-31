

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

async def get_keywords(urls,comment):
    """
    Extracts keywords from the meta tags of given URLs. If no keywords are found,
    saves keywords using the domain name and title of the webpage.

    """
    keywords = []

    for url_info in urls:
        url = url_info.get('url')
        section = url_info.get('sec')

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            html_content = response.content
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
            continue

        soup = BeautifulSoup(html_content, 'html.parser')

        meta_keywords = None
        meta_tags = [
            soup.find("meta", {"name": "keywords"}),
            soup.find("meta", {"name": "Keywords"})
        ]

        for tag in meta_tags:
            if tag and 'content' in tag.attrs:
                meta_keywords = tag.attrs['content']
                break
        if len(comment)>10:
            if meta_keywords:
                cleaned_keywords = meta_keywords.replace(" ", "").split(',')
                for keyword in cleaned_keywords:
                    keywords.append({'keyword': keyword, 'sec': section, 'url': url, 'comment': comment})
            else:
            
                domain_name = urlparse(url).netloc
                page_title = soup.title.string.strip() if soup.title else ""
                keywords.append({'keyword': domain_name, 'sec': section, 'url': url, 'comment': comment})
                keywords.append({'keyword': page_title, 'sec': section, 'url': url, 'comment': comment})
        else:
            if meta_keywords:
                cleaned_keywords = meta_keywords.replace(" ", "").split(',')
                for keyword in cleaned_keywords:
                    keywords.append({'keyword': keyword, 'sec': section, 'url': url, })
            else:
            
                domain_name = urlparse(url).netloc
                page_title = soup.title.string.strip() if soup.title else ""
                keywords.append({'keyword': domain_name, 'sec': section, 'url': url, })
                keywords.append({'keyword': page_title, 'sec': section, 'url': url, })
            

    return keywords


def filter_keywords(keywords, max_keyword_length=12):
    """
    Filters keywords based on length less than a specified value.

    """
    filtered_keywords = [keyword for keyword in keywords if len(keyword['keyword']) < max_keyword_length]
    return filtered_keywords
