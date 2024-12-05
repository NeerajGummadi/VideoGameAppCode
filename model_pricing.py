import sqlite3
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

# Path to the SQLite database
DATABASE = '/Users/neeraj_gummadi/Documents/project/games.db'

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
    X = df.drop(columns=['price'])  # Features excluding 'price'
    y = df['price']                # Target is 'price'

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Decision Tree Regressor
    model_pricing = DecisionTreeRegressor(random_state=42)
    model_pricing.fit(X_train, y_train)

    # Save the model
    with open('model_pricing.pkl', 'wb') as file:
        pickle.dump(model_pricing, file)

    print("model_pricing.pkl saved successfully!")
else:
    print("Failed to load data from the database. Exiting.")