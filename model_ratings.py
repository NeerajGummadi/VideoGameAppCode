import sqlite3
import pickle
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


# Dynamically set the database path relative to the script's location
DATABASE = os.path.join(os.path.dirname(__file__), 'games.db')

def load_data_from_db():
    """
    Load data from the SteamData table in the database.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        
        # Query to retrieve the required columns
        query = """
        SELECT positive_ratings, negative_ratings, price, achievements, average_playtime
        FROM SteamData
        """
        
        # Load the data into a pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Close the database connection
        conn.close()
        
        return df
    except Exception as e:
        print(f"Error loading data from the database: {e}")
        return None

# Load and preprocess the dataset from the database
df = load_data_from_db()

if df is not None:
    # Drop any rows with missing data
    df = df.dropna()

    # Define features and target
    X = df.drop(columns=['positive_ratings'])
    y = df['positive_ratings']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest Regressor with reduced size
    model_ratings = RandomForestRegressor(
        n_estimators=50,        # Reduced number of trees
        max_depth=10,           # Limit tree depth
        max_features='sqrt',    # Limit the number of features used in splits
        random_state=42
    )
    model_ratings.fit(X_train, y_train)

    # Save the model with pickle
    with open('model_ratings.pkl', 'wb') as file:
        pickle.dump(model_ratings, file)

    print("model_ratings.pkl saved successfully!")
else:
    print("Failed to load data from the database. Exiting.")
