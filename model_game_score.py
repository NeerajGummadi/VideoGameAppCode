import sqlite3
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
import lightgbm as lgb

# Connect to the database and load the data from the OutputData table
DATABASE = '/Users/neeraj_gummadi/Documents/project/games.db'

def load_data_from_db():
    """
    Load data from the OutputData table in the database.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        query = "SELECT is_action, is_indie, is_casual, is_strat, is_adv, is_f2p, is_sim, is_windows, is_mac, is_linux, rval FROM OutputData"
        df = pd.read_sql_query(query, conn)
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
    X = df.drop(columns=['rval'])
    y = df['rval']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train LightGBM model
    train_set = lgb.Dataset(X_train, label=y_train)
    params = {'objective': 'regression', 'metric': 'rmse', 'learning_rate': 0.1, 'num_leaves': 31}
    model_game_score = lgb.train(params, train_set, num_boost_round=200)

    # Save the model
    with open('model_game_score.pkl', 'wb') as file:
        pickle.dump(model_game_score, file)

    print("model_game_score.pkl saved successfully!")
else:
    print("Failed to load data from the database. Exiting.")