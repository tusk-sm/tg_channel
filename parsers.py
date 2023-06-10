import requests
import re
from already_sent import get_already_sent

def hn_parser():
    HN_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    ARTICLE_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'
    article_ids = requests.get(HN_URL).json()
    messages = []
    for article_id in article_ids:
        if str(article_id) in get_already_sent():
            continue
        
        article_data = requests.get(ARTICLE_URL.format(article_id)).json()
        
        if article_data.get('score', 0) >= 1000:
            

            article_url = article_data.get('url', '') 
            if not article_data.get('url'):
                article_url = f'https://news.ycombinator.com/item?id={article_id}'
            
            message = '{}\n{}'.format(article_data.get('title', ''), article_url)

            messages.append({
                "id":article_id,
                "text": message
            })            
    return messages

def gh_parser():
    gh_trending_url = 'https://github.com/trending'
    html = requests.get(gh_trending_url).text
    
    arcicle_pattern = r'<article.*?</article>'  
    title_pattern = r'<h2.*?</h2>'
    link_pattern = r'href=".*?"'
    description_pattern = r'<p .*?</p>'
    stars_pattern = r'>[\s\d,.]*?stars.*?<'
    digits_pattern = r'\d{1,3}(?:,\d{3})*'

    articles = re.findall(arcicle_pattern, html, re.DOTALL)
    messages = []
    for article in articles:        
        stars = re.findall(stars_pattern, article, re.DOTALL)
        if stars:
            stars = stars[0]
            stars_count = re.findall(digits_pattern, stars, re.DOTALL)[0]
            stars_count = int(stars_count.replace(',','').replace('.', ''))

            if stars_count > 1000:
                h2 = re.findall(title_pattern, article, re.DOTALL)[0]
                h2_tags = re.findall(r'<.*?</.*?>', h2,  re.DOTALL)                
                title = h2
                for tag in h2_tags:             
                    title = title.replace(tag, "")           

                title = title.strip()

                link = re.findall(link_pattern, h2)[0]
                link = link.replace('"', "").replace('href=', "")

                if link in get_already_sent():                    
                    continue

                description = re.findall(description_pattern, article, re.DOTALL)
                if description:
                    description = description[0]
                    d_tags = re.findall(r'<.*?>', description,  re.DOTALL)
                    for tag in d_tags:
                        description = description.replace(tag, "")
                    description = description.strip()
                else:
                    description =""

                message = f"{title}\nhttps://github.com{link}\n{description}"

                messages.append({
                    "id": link ,
                    "text": message
                }) 
    return messages 
