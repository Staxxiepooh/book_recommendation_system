import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sqlite3

# Load pre-trained model and datasets
cosine_sim = pickle.load(open('Recmodel/cosine_sim.pkl', 'rb'))
table_pivot = pickle.load(open('Recmodel/book_pivot.pkl', 'rb'))
books = pickle.load(open('Recmodel/books.pkl', 'rb'))

# SQLite Database for user ratings
USER_RATINGS_FILE = 'user_ratings.db'

# Apply genre threshold
GENRE_THRESHOLD = 10
genre_counts = books['categories'].value_counts()
popular_genres = genre_counts[genre_counts >= GENRE_THRESHOLD].index
books = books[books['categories'].isin(popular_genres)]

# Ensure thumbnails are valid URLs
books['thumbnail'] = books['thumbnail'].astype(str)
books['thumbnail'] = books['thumbnail'].apply(
    lambda x: x if x.startswith('http') else 'https://via.placeholder.com/120'
)

# Load user ratings
def load_user_ratings():
    conn = sqlite3.connect(USER_RATINGS_FILE)
    query = "SELECT user_id, book_title, rating FROM ratings"
    
    try:
        df = pd.read_sql(query, conn)
    except:
        df = pd.DataFrame(columns=['user_id', 'book_title', 'rating'])
    
    conn.close()
    return df

# Save user ratings
def save_user_rating(user_id, book_title, rating):
    conn = sqlite3.connect(USER_RATINGS_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings 
                      (user_id TEXT, book_title TEXT, rating INTEGER)''')

    cursor.execute("SELECT * FROM ratings WHERE user_id=? AND book_title=?", (user_id, book_title))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("UPDATE ratings SET rating=? WHERE user_id=? AND book_title=?", (rating, user_id, book_title))
    else:
        cursor.execute("INSERT INTO ratings (user_id, book_title, rating) VALUES (?, ?, ?)", (user_id, book_title, rating))
    
    conn.commit()
    conn.close()

# Function to recommend books
def recommend_books(book_title, user_id, selected_genre):
    """Recommend books based on the selected book, user's ratings, and genre."""
    if book_title not in table_pivot.index:
        return pd.DataFrame(columns=['title', 'thumbnail'])

    book_index = np.where(table_pivot.index == book_title)[0][0]
    similarities = cosine_sim[book_index]
    suggestions = np.argsort(similarities)[::-1][1:15]
    recommended_books = [table_pivot.index[i] for i in suggestions]

    # Filter by genre
    genre_books = books[books['categories'] == selected_genre]
    filtered_books = genre_books[genre_books['title'].isin(recommended_books)]

    if filtered_books.empty:
        filtered_books = books[books['title'].isin(recommended_books)]

    # Load user ratings and adjust recommendations
    user_ratings = load_user_ratings()
    user_ratings = user_ratings[user_ratings['user_id'] == user_id]

    if not user_ratings.empty:
        rated_books_list = user_ratings['book_title'].tolist()

        # Remove books with low ratings (1 or 2)
        low_rated_books = user_ratings[user_ratings['rating'] <= 2]['book_title'].tolist()
        filtered_books = filtered_books[~filtered_books['title'].isin(low_rated_books)]

        # Prioritize books with high ratings (4 or 5)
        high_rated_books = user_ratings[user_ratings['rating'] >= 4]['book_title'].tolist()

        # Combine high-rated books and new recommendations (without duplicates)
        high_rated_books_df = books[books['title'].isin(high_rated_books)]
        combined_books = pd.concat([high_rated_books_df, filtered_books]).drop_duplicates().reset_index(drop=True)

        # Ensure diverse recommendations
        filtered_books = combined_books.sample(frac=1).head(6)

    # If still empty, suggest random books from the same genre
    if filtered_books.empty:
        st.warning("No more personalized recommendations! Showing random books from the same genre.")
        filtered_books = genre_books.sample(n=min(6, len(genre_books)))

    return filtered_books[['title', 'thumbnail']]

# Streamlit UI
st.title("📚 Personalized Book Recommendation System")

user_id = st.text_input("Enter your User ID:", value="User1")
selected_genre = st.selectbox("Select a genre:", books['categories'].unique())
selected_book = st.selectbox("Select a book you liked:", books[books['categories'] == selected_genre]['title'].unique())

if "recommended_books" not in st.session_state:
    st.session_state.recommended_books = pd.DataFrame(columns=['title', 'thumbnail'])

if st.button("Get Recommendations"):
    st.session_state.recommended_books = recommend_books(selected_book, user_id, selected_genre)

if not st.session_state.recommended_books.empty:
    st.subheader("📌 Recommended Books for You:")

    num_books = len(st.session_state.recommended_books)
    num_cols = min(6, num_books)  
    cols = st.columns(num_cols)

    for idx, (col, (_, row)) in enumerate(zip(cols, st.session_state.recommended_books.iterrows())):
        with col:
            st.image(row['thumbnail'], caption=row['title'], width=120)

st.subheader("⭐ Rate Your Recommended Books")
if not st.session_state.recommended_books.empty:
    selected_rated_book = st.selectbox("Select a book to rate:", st.session_state.recommended_books['title'])
    rating = st.slider("Rate this book (1-5):", 1, 5, 3)
    
    if st.button("Submit Rating"):
        save_user_rating(user_id, selected_rated_book, rating)
        st.success(f"Your rating for '{selected_rated_book}' has been saved! 🎉")

        # Refresh recommendations after rating
        st.session_state.recommended_books = recommend_books(selected_book, user_id, selected_genre)
        
        if not st.session_state.recommended_books.empty:
            st.subheader("🔄 Updated Recommendations:")
            num_books = len(st.session_state.recommended_books)
            num_cols = min(6, num_books)
            cols = st.columns(num_cols)

            for idx, (col, (_, row)) in enumerate(zip(cols, st.session_state.recommended_books.iterrows())):
                with col:
                    st.image(row['thumbnail'], caption=row['title'], width=120)
        else:
            st.warning("No more books to recommend based on your preferences and ratings.")
