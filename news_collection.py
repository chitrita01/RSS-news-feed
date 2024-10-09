import feedparser
import random
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from celery import Celery
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from celery import Celery
from Database import session

# Database connection
engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    publication_date = Column(Date)
    source_url = Column(String)
    category = Column(String)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class ArticleCategory(Base):
    __tablename__ = 'article_categories'
    article_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, primary_key=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Celery configuration
celery = Celery('tasks', broker='amqp://guest@localhost//')


# RSS feeds
feeds = [
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'http://qz.com/feed',
    'http://feeds.foxnews.com/foxnews/politics',
    'http://feeds.reuters.com/reuters/businessNews',
    'http://feeds.feedburner.com/NewshourWorld',
    'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
]
# Feed Parser
def parse_feed(feed_url):
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        title = entry.title
        content = entry.description
        publication_date = entry.published
        source_url = entry.link
        article = Article(title=title, content=content, publication_date=publication_date, source_url=source_url)
        session.add(article)
        session.commit()
        celery.send_task('process_article', args=[article.id])
def extract_data(feeds):
    articles = []
    for feed in feeds:
        articles.extend(parse_feed(feed))
    return articles
def process_article(article_id):
    article = session.query(Article).get(article_id)
    content = article.content
    tokens = word_tokenize(content)
    tokens = [token for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stopwords.words('english')]
    tokens = [WordNetLemmatizer().lemmatize(token) for token in tokens]
    category = classify(tokens)
    article.category = category
    session.commit()

def classify(tokens):
    # Implement your classification logic here
    # For demonstration purposes, we'll just assign a random category
    categories = ['Terrorism / protest / political unrest / riot', 'Positive/Uplifting', 'Natural Disasters', 'Others']
    return random.choice(categories)

if __name__ == '__main__':
    for feed in feeds:
        parse_feed(feed)


celery = Celery('tasks', broker='amqp://guest@localhost//')

@celery.task
def process_article(article_id):
    article = session.query(Article).get(article_id)
    # Implement your processing logic here
    print(f"Processing article {article_id}")      

#Data Extraction
articles = extract_data(feeds)
for article in articles:
    print(article)    