import streamlit as st
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt

# Define a function to scrape text data from the URL
def scrape_text_from_url(url):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Check if the request was successful
        html_content = r.content
        soup = BeautifulSoup(html_content, 'html.parser')
        paragraphs = soup.find_all('p')
        text_data = ' '.join([para.get_text() for para in paragraphs])
        text_data = ' '.join(text_data.split())  # Remove extra whitespace
        return text_data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return None

# Define a function to perform sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    sentiment_subjectivity = blob.sentiment.subjectivity
    sentences = [(sentence, sentence.sentiment.polarity, sentence.sentiment.subjectivity) for sentence in blob.sentences]
    return sentiment_polarity, sentiment_subjectivity, sentences

# Streamlit interface
st.title('Article Sentiment Analysis')

# URL input
url = st.text_input('Enter the URL of the article:', '')

if url:
    # Scrape and analyze the text
    text_data = scrape_text_from_url(url)
    if text_data:
        sentiment_polarity, sentiment_subjectivity, sentences = analyze_sentiment(text_data)
        
        # Display results
        st.write(f"**Article Sentiment Polarity:** {sentiment_polarity}")
        st.write(f"**Article Sentiment Subjectivity:** {sentiment_subjectivity}")
        
        if sentiment_polarity > 0:
            st.success("Positive sentiments")
        else:
            st.warning("Negative sentiments")
        
        # Visualize the sentiment data
        st.write("### Sentiment Polarity and Subjectivity Plot")
        
        # Extracting sentence data for plotting
        sentence_texts = [str(sentence) for sentence, _, _ in sentences]
        polarities = [polarity for _, polarity, _ in sentences]
        subjectivities = [subjectivity for _, _, subjectivity in sentences]
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Plot sentiment polarity
        ax.plot(range(len(sentences)), polarities, label='Polarity', color='blue', marker='o')
        ax.set_xlabel('Sentence Index')
        ax.set_ylabel('Sentiment Polarity', color='blue')
        ax.tick_params(axis='y', labelcolor='blue')
        
        # Create a second y-axis for sentiment subjectivity
        ax2 = ax.twinx()
        ax2.plot(range(len(sentences)), subjectivities, label='Subjectivity', color='red', marker='x')
        ax2.set_ylabel('Sentiment Subjectivity', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        
        fig.tight_layout()
        st.pyplot(fig)


        # Display sentence-wise sentiment analysis
        st.write("### Sentence-wise Sentiment Analysis")
        for sentence, polarity, subjectivity in sentences:
            st.write(f"**Sentence:** {sentence}")
            st.write(f"Sentiment Polarity: {polarity}")
            st.write(f"Sentiment Subjectivity: {subjectivity}")
            st.write("---")
        
#The url you can enter
#https://www.grammar-monster.com/glossary/articles.htm
        
