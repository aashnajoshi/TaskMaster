import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the reviews page
url = 'https://www.airlinequality.com/airline-reviews/british-airways/'

# Sending a request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Successfully fetched the webpage")
    
    reviews = soup.find_all('article', class_='comp_media-review-rated')

    # Check if any reviews were found
    if reviews:
        print(f"Found {len(reviews)} reviews")
        
        # Lists to store data
        review_titles = []
        review_texts = []
        review_ratings = []

        # Loop through reviews and extract data
        for review in reviews:
            title = review.find('h2', class_='text_header')
            review_text = review.find('div', class_='text_content')
            rating = review.find('div', class_='rating-10')  # Updated the class for rating

            if title and review_text and rating:
                review_titles.append(title.text.strip())
                review_texts.append(review_text.text.strip())
                rating_value = rating.text.strip()  # Extracting the text inside the rating span
                review_ratings.append(rating_value)
            else:
                print("Incomplete review data found, skipping this entry")
                print(f"Title: {title}, Review Text: {review_text}, Rating: {rating}")

        # Creating a DataFrame
        data = pd.DataFrame({
            'Title': review_titles,
            'Review': review_texts,
            'Rating': review_ratings
        })

        # Save to CSV
        data.to_csv('data/ba_reviews.csv', index=False)
        print("Data successfully saved to 'data/ba_reviews.csv'")
    else:
        print("No reviews found on the webpage")
else:
    print(f"Failed to fetch the webpage, status code: {response.status_code}")
