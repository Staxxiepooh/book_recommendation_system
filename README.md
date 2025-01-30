# Book Recommendation System

## Overview
This project is a Book Recommendation System that provides personalized book suggestions based on user preferences and historical data. The system uses collaborative filtering and content-based filtering techniques to recommend books that match users' reading tastes.

## Features
- Personalized book recommendations
- Uses collaborative and content-based filtering
- Interactive web application for user interaction
- Efficient data processing and recommendation logic
- Genre-based filtering with minimum data threshold
- Displays book covers along with recommendations

## Project Structure
```
├── RecSystem.ipynb      # Jupyter Notebook for recommendation logic
├── app.py               # Main application script
├── requirements.txt     # Required dependencies
├── setup.py             # Installation script
├── src/                 # Source code for the recommendation engine
├── data2/               # Dataset containing book information
├── Recmodel/            # Trained models for recommendations
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
1. **Select a Genre**: Choose a book genre from the dropdown.
2. **Pick Liked Books**: Select books you enjoyed from the given list.
3. **Get Recommendations**: Click the "Show Recommendation" button to generate a list of suggested books based on your preferences.
4. **View Book Covers**: The system displays book covers when available; otherwise, a placeholder image is shown.

## Contribution
Feel free to contribute to the project by submitting issues or pull requests. Ensure your contributions follow the project's coding standards and include proper documentation.

## License
This project is licensed under the MIT License.

## Contact
For any questions or contributions, contact the repository owner via GitHub.

