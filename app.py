import streamlit as st
import json

def fetch_news(tags):
    # Function to fetch news articles based on selected tags
    with open("data/confidencial.json", "r") as f:
        articles = json.load(f)
    
    return list(articles.values())

def main():
    st.title("Newsies")

    # Define available tags (news sites)
    tags = ["Confidencial", "Mundo", "Pais", "ABC", "Razon"]

    # Sidebar for tag selection
    selected_tags = st.sidebar.multiselect("Select Tags", tags, default=tags)

    # "All" option to select all tags
    if "All" in selected_tags:
        selected_tags = tags

    # Fetch news articles for selected tags
    news_articles = fetch_news(selected_tags)

    # Calculate the number of rows needed to ensure an even grid
    num_columns = 3  # Number of columns in the grid
    num_articles = len(news_articles)
    num_rows = -(-num_articles // num_columns)  # Ceiling division to ensure the grid is even

    # Display news articles in a grid with cards
    for i in range(num_rows):
        row = st.columns(num_columns)
        for j in range(num_columns):
            index = i * num_columns + j
            if index < num_articles:
                with row[j]:
                    article = news_articles[index]
                    st.write(f"## {article['title']}")
                    st.write(article['text'])
                    st.write(f"[Read more]({article['link']})")
                    st.markdown("---", unsafe_allow_html=True)  # Add border between cards

if __name__ == "__main__":
    main()
