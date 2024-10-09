RSS News Feed Categorization Application

This application collects news articles from multiple RSS feeds, stores them in a relational database, and categorizes them into predefined categories using Natural Language Processing (NLP) techniques.

Features:

Fetches news articles from multiple RSS feeds
Stores articles in a PostgreSQL database
Classifies articles into categories using NLP (Terrorism/Protest/Political Unrest/Riot, Positive/Uplifting, Natural Disasters, Others)
Uses Celery for asynchronous processing and task management
Implements logging and error handling for smooth operation
Technologies Used:

Python
Feedparser
SQLAlchemy
Celery
NLTK
PostgreSQL
Flask (optional)
Future Improvements:

Implement more sophisticated classification models (e.g., machine learning classifiers)
Add support for real-time news feed updates using webhooks or data streaming
Incorporate additional error handling mechanisms for more robust performance
This project demonstrates a systematic approach to building an automated news article categorization system using Python and NLP techniques.
