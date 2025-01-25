import pickle
import streamlit as st
import numpy as np

# Load the pre-trained model, book names, pivot table, and books DataFrame
st.header('Book Recommendation System')
model = pickle.load(open('Recmodel/model.pkl', 'rb'))
book_names = pickle.load(open('Recmodel/book_names.pkl', 'rb'))
table_pivot = pickle.load(open('Recmodel/book_pivot.pkl', 'rb'))
books = pickle.load(open('Recmodel/books.pkl', 'rb'))  # Assuming books DataFrame is available

def recommend_books(user_genre, liked_books):
    books_list = []
    
    # Filter the books based on the selected genre from the original books DataFrame
    filtered_books = books[books['categories'].str.contains(user_genre, case=False, na=False)]
    
    # Ensure filtered_books is not empty
    if filtered_books.empty:
        return f"No books found for the genre '{user_genre}'."
    
    # Get book IDs of the liked books from the table_pivot index
    liked_books_ids = [np.where(table_pivot.index == book)[0][0] for book in liked_books if book in table_pivot.index]
    
    # Handle the case where no liked books are found
    if not liked_books_ids:
        return "None of the liked books are found in the dataset."
    
    # Calculate the mean vector of the liked books from the table_pivot
    liked_books_vector = table_pivot.iloc[liked_books_ids].mean(axis=0).values.reshape(1, -1)
    
    # Find the nearest neighbors based on the mean vector of liked books
    distance, suggestion = model.kneighbors(liked_books_vector, n_neighbors=6)

    # Get the recommended books from the table_pivot index
    for i in range(len(suggestion[0])):
        books_list.append(table_pivot.index[suggestion[0][i]])

    return books_list

# Streamlit select box to choose a genre
selected_genre = st.selectbox("Select a genre", books['categories'].unique())

# Streamlit multiselect box to select books
selected_books = st.multiselect("Select books you liked", book_names)

# Button to trigger recommendation
if st.button('Show Recommendation'):
    if not selected_books:
        st.warning("Please select at least one book you liked.")
    else:
        recommended_books = recommend_books(selected_genre, selected_books)
        
        # Display the recommendations in columns
        if isinstance(recommended_books, str):
            st.write(recommended_books)  # Display the message if no recommendations are found
        else:
            col1, col2, col3, col4, col5 = st.columns(5)
            for i, col in enumerate([col1, col2, col3, col4, col5]):
                if i < len(recommended_books):
                    with col:
                        book_title = recommended_books[i]
                        st.text(book_title)
                        
                        # Get the thumbnail URL for the recommended book from the original 'books' DataFrame
                        book_thumbnail_url = books[books['title'] == book_title]['thumbnail']
                        
                        # Check if the thumbnail URL is valid (not NaN or empty)
                        if not book_thumbnail_url.empty and isinstance(book_thumbnail_url.iloc[0], str):
                            st.image(book_thumbnail_url.iloc[0])  # Display the actual image
                        else:
                            # Display a placeholder image if the thumbnail URL is invalid or missing
                            st.image("https://via.placeholder.com/150?text=Book+Cover")
