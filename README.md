# Book Recommendation System

## Overview
This project is a Personalized Book Recommendation System that dynamically adjusts suggestions based on user preferences, historical data, and real-time feedback. The system employs collaborative filtering and cosine similarity to refine recommendations, incorporating user input for better personalization.

## Features
- Personalized book recommendations based on user ratings and preferences.
- Collaborative filtering for finding similar users and recommendations.
- Cosine similarity-based model for content-based recommendations.
- Dynamic feedback mechanism to refine suggestions over time.
- Genre-based and page-length filtering for fine-tuned recommendations.
- Interactive web application using Streamlit.
- User rating storage in SQLite for tracking preferences.
- Pre-trained model integration for efficient recommendation retrieval.

## Project Structure
```
├── RecSystem.ipynb      # Jupyter Notebook for model development
├── app.py               # Streamlit application script
├── requirements.txt     # Required dependencies
├── setup.py             # Installation script
├── src/                 # Source code for the recommendation engine
├── data/                # Dataset containing book information
├── Recmodel/            # Pre-trained models for recommendations
│   ├── cosine_sim.pkl   # Cosine similarity matrix
│   ├── book_pivot.pkl   # Processed pivot table for ratings
│   ├── books.pkl        # Book metadata
├── user_ratings.csv     # Storage for user feedback and ratings
├── .gitignore           # Files and directories to be ignored by Git
├── README.md            # Project documentation
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Staxxiepooh/book_recommendation_system.git
   ```
2. Navigate to the project directory:
   ```bash
   cd book_recommendation_system
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application using:
```bash
streamlit run app.py
```
Then, open your browser and navigate to the provided local server URL to interact with the recommendation system.

## How It Works
1. Select a Genre: Choose a book genre from the dropdown.
2. Pick Liked Book: Select books you enjoyed from the given list.
3. Rate Books: Provide feedback on recommendations.
4. Get Recommendations: Click the "Show Recommendation" button to generate a list of suggested books.
5. View Book Covers: Displays book covers when available; otherwise, a placeholder image is shown.
6. Dynamic Updates: As you rate more books, future recommendations improve based on your inputs.

## Contribution
Contributions are welcome! Submit issues or pull requests following the project's coding standards and documentation guidelines.

## License
This project is licensed under the MIT License.

## Contact
For any questions or contributions, contact the repository owner via GitHub.
