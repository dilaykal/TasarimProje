import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MultiLabelBinarizer
import re

class DepremTweetClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.classifier = OneVsRestClassifier(LinearSVC())
        self.mlb = MultiLabelBinarizer()
        self.categories = ['acil', 'cok_acil', 'yardim', 'erzak_yardimi', 'su_yardimi', 'afad_yardimi']
        
    def preprocess_text(self, text):
        # Basit önişleme
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def determine_urgency(self, text):
        urgent_words = ['acil', 'yardım', 'enkaz', 'mahsur', 'yaralı']
        very_urgent_words = ['ölüm', 'kan', 'kritik', 'ağır yaralı']
        
        text_lower = text.lower()
        urgency_score = sum(word in text_lower for word in urgent_words)
        very_urgent_score = sum(word in text_lower for word in very_urgent_words)
        
        if very_urgent_score > 0:
            return 'cok_acil'
        elif urgency_score > 0:
            return 'acil'
        return 'yardim'

    def determine_aid_type(self, text):
        aid_types = []
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['yiyecek', 'gıda', 'erzak']):
            aid_types.append('erzak_yardimi')
        if any(word in text_lower for word in ['su', 'içme suyu']):
            aid_types.append('su_yardimi')
        if 'afad' in text_lower:
            aid_types.append('afad_yardimi')
            
        return aid_types

    def process_tweets(self, tweet_file):
        with open(tweet_file, 'r', encoding='utf-8') as f:
            tweets = f.readlines()
        
        processed_data = []
        for tweet in tweets:
            processed_text = self.preprocess_text(tweet)
            urgency = self.determine_urgency(tweet)
            aid_types = self.determine_aid_type(tweet)
            categories = [urgency] + aid_types
            
            processed_data.append({
                'tweet': tweet.strip(),
                'processed_text': processed_text,
                'categories': categories
            })
            
        return pd.DataFrame(processed_data)

    def categorize_tweets(self, tweet_file):
        df = self.process_tweets(tweet_file)
        results = {category: [] for category in self.categories}
        
        for _, row in df.iterrows():
            for category in row['categories']:
                results[category].append(row['tweet'])
        
        return results

def write_results(results, output_prefix='kategori'):
    for category, tweets in results.items():
        filename = f'{output_prefix}_{category}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            for tweet in tweets:
                f.write(tweet + '\n')

classifier = DepremTweetClassifier()
results = classifier.categorize_tweets('tweets.txt')
write_results(results)