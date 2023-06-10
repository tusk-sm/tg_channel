import csv
import os

dir_path  = os.path.dirname(os.path.realpath(__file__))
SENT_ARTICLES_FILE = f'{dir_path}/already_sent.csv'

def get_already_sent():
    with open(SENT_ARTICLES_FILE, 'r') as f:
        sent_article_ids  = []
        for row in csv.reader(f):
            if row:
                sent_article_ids.append(row[0])        
        return sent_article_ids
    
def add_already_sent(article_id):    
    with open(SENT_ARTICLES_FILE,'a') as f:
        csv.writer(f).writerow([article_id])