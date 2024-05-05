import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load background image style
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://img.freepik.com/free-photo/lightbox-still-life-arrangement_23-2149198407.jpg?t=st=1714885995~exp=1714889595~hmac=2074c0155cb59115af991d3abc9ae22ef12e92c257195421fc4b2105f598f800&w=740");
background-size: cover;
}
[data-testid="stHeader"]{
background-color: rgba(0,0,0,0);
}
</style>
'''

# Display background image
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title of the Streamlit app
st.title('Book Recommendation System')

# Function to recommend similar books
def recommend(book_name):
    # Load necessary data
    pt = pd.read_pickle('pivot.pkl')
    finalbooks = pd.read_pickle('finalbooks.pkl')
    similarity_score = cosine_similarity(pt)
    
    # Find similar books
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:7]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = finalbooks[finalbooks['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    
    return data

# Load popular books data
popular_df = pd.read_pickle('popular.pkl')

# Get the current page query parameter
page = st.query_params.get("page", "popular_books")

# Define page content based on the current page
if page == "popular_books":
    # Popular Books Section
    st.header('Popular Books')

    # Display top 50 popular books in a grid layout
    num_cols = 4  # Number of columns in the grid layout
    num_books = 50  # Number of books to display
    for i in range(0, num_books, num_cols):
        book_subset = popular_df.iloc[i:i+num_cols]
        cols = st.columns(num_cols)
        for j, (_, row) in enumerate(book_subset.iterrows()):
            with cols[j]:
                st.subheader(row['Book-Title'])
                st.write('Author:', row['Book-Author'])
                st.image(row['Image-URL-M'], use_column_width=True)
                st.write('Number of Ratings:', row['num_rating'])
                st.write('Average Rating:', row['avg_rating'])

elif page == "recommend_books":
    # Recommend Books Section
    st.header('Recommend Similar Books')

    # User input for book name
    input_book = st.selectbox("Enter or select the name of a book", popular_df['Book-Title'].unique())

    # Button to trigger recommendation
    if st.button('Recommend similar Books'):
        # Get recommendations based on user input
        recommended_books = recommend(input_book)
        
        # Display recommended books
        for book in recommended_books:
            st.subheader(book[0])
            st.write('Author:', book[1])
            st.image(book[2])
            st.write("**________________________________________________________________________________**")

# Add navigation buttons to switch between pages
if page == "popular_books":
    st.write("Click here for the book recommendation")
    if st.button("Recommend Books"):
        st.query_params["page"] = "recommend_books"
else:
    st.write("Click here to see the popular books ")
    if st.button("Popular Books"):
        st.query_params["page"] = "popular_books"
