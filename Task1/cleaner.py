import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('data/ba_reviews.csv')

# Data cleaning
data.dropna(inplace=True)

# Sentiment analysis
data['Sentiment'] = data['Review'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Visualizing sentiment distribution
plt.hist(data['Sentiment'], bins=30, edgecolor='k')
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Frequency')
plt.show()

# Generate word cloud (Fig1)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(data['Review']))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('data/Figure 1.png')

#Generate Fig2
data = {'Category A': 40, 'Category B': 70, 'Category C': 30}
categories = list(data.keys())
values = list(data.values())

plt.figure(figsize=(10, 6))
plt.bar(categories, values, color=['blue', 'orange', 'green'])
plt.xlabel('Categories')
plt.ylabel('Values')
plt.title('Sample Bar Chart')
plt.savefig('data/Figure 2.png')
plt.close()
