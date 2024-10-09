from celery import Celery
from Database import session
from news_collection import Article

celery = Celery('tasks', broker='amqp://guest@localhost//')

@celery.task
def process_article(article_id):
    article = session.query(Article).get(article_id)
    # Implement your processing logic here
    print(f"Processing article {article_id}")