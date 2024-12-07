import sqlite3
import pandas as pd
import pickle
import streamlit as st
import joblib

# Database connection
DATABASE = "games.db"

def connect_db():
    return sqlite3.connect(DATABASE)

# Load models

with open('model_playtime.pkl', 'rb') as file:
    model_playtime = pickle.load(file)

with open('model_ratings.pkl', 'rb') as file:
    model_ratings = pickle.load(file)

with open('model_pricing.pkl', 'rb') as file:
    model_pricing = pickle.load(file)

with open('model_game_score.pkl', 'rb') as file:
    model_game_score = pickle.load(file)

# Function to fetch games
def fetch_games():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM SteamData", conn)
    conn.close()
    return df

# Function to add a game
def add_game_to_db(inputs):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO SteamData (
                appid, name, release_date, english, developer, publisher,
                platforms, required_age, categories, genres, steamspy_tags,
                achievements, positive_ratings, negative_ratings, average_playtime,
                median_playtime, owners, price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(inputs.values()))
        conn.commit()
        conn.close()
        return True, "Game added successfully!"
    except Exception as e:
        return False, f"Error adding game: {e}"

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Manage Steam Games", "View Games", "Predict Playtime", "Predict Ratings", "Predict Pricing", "Predict Game Score"])

# Home
if page == "Home":
    st.title("Video Game Reception Prediction")
    st.write("Welcome to the Video Game Reception Prediction Dashboard! Use the navigation menu to explore features.")

# Manage Steam Games
elif page == "Manage Steam Games":
    st.title("Manage Steam Games")

    # Fetch games from the database
    def fetch_games():
        conn = connect_db()
        df = pd.read_sql_query("SELECT rowid, * FROM SteamData", conn)
        conn.close()
        return df

    df = fetch_games()

    if not df.empty:
        # Display the games in a table
        st.dataframe(df)

        # Select a game by name to Edit or Delete
        st.subheader("Edit or Delete Game")
        selected_game_name = st.selectbox("Select a Game Name to Edit/Delete", df["name"].values)

        # Fetch selected row data by name
        selected_row = df[df["name"] == selected_game_name].iloc[0]

        # Display Edit form with populated values
        # Display Edit form with populated values
        st.subheader("Edit Game")
        with st.form("edit_game_form"):
            updated_data = {
                "appid": st.text_input("App ID", value=str(selected_row["appid"])),
                "name": st.text_input("Name", value=str(selected_row["name"])),
                "release_date": st.text_input("Release Date", value=str(selected_row["release_date"])),
                "english": st.text_input("English", value=str(selected_row["english"])),
                "developer": st.text_input("Developer", value=str(selected_row["developer"])),
                "publisher": st.text_input("Publisher", value=str(selected_row["publisher"])),
                "platforms": st.text_input("Platforms", value=str(selected_row["platforms"])),
                "required_age": st.text_input("Required Age", value=str(selected_row["required_age"])),
                "categories": st.text_input("Categories", value=str(selected_row["categories"])),
                "genres": st.text_input("Genres", value=str(selected_row["genres"])),
                "steamspy_tags": st.text_input("SteamSpy Tags", value=str(selected_row["steamspy_tags"])),
                "achievements": st.text_input("Achievements", value=str(selected_row["achievements"])),
                "positive_ratings": st.text_input("Positive Ratings", value=str(selected_row["positive_ratings"])),
                "negative_ratings": st.text_input("Negative Ratings", value=str(selected_row["negative_ratings"])),
                "average_playtime": st.text_input("Average Playtime", value=str(selected_row["average_playtime"])),
                "median_playtime": st.text_input("Median Playtime", value=str(selected_row["median_playtime"])),
                "owners": st.text_input("Owners", value=str(selected_row["owners"])),
                "price": st.text_input("Price", value=str(selected_row["price"])),
            }
            if st.form_submit_button("Update Game"):
                try:

                    # Display the app ID being updated for debugging
                    st.write(f"Updating Game with App ID: {updated_data['appid']}")
                    print(f"Updating Game with App ID: {updated_data['appid']}")  # Print to terminal for debugging

                    # Connect to the database
                    conn = connect_db()
                    cursor = conn.cursor()

                    # Update the record in the database
                    query = """
                        UPDATE SteamData
                        SET appid = ?, name = ?, release_date = ?, english = ?, developer = ?, publisher = ?,
                            platforms = ?, required_age = ?, categories = ?, genres = ?, steamspy_tags = ?,
                            achievements = ?, positive_ratings = ?, negative_ratings = ?, average_playtime = ?,
                            median_playtime = ?, owners = ?, price = ?
                        WHERE appid = ?
                    """
                    cursor.execute(query, (*updated_data.values(), updated_data["appid"]))

                    conn.commit()
                    conn.close()

                    st.success("Game updated successfully!")
                    # Refresh the table
                    df = fetch_games()
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"Error updating game: {e}")

        
        # Delete functionality
        st.subheader("Delete Game")
        
        if st.button("Delete Game"):
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM SteamData WHERE name = ?", (selected_game_name,))  # Updated to use 'name' for targeting
                conn.commit()
                conn.close()
                st.success("Game deleted successfully!")
                # Refresh the table
                df = fetch_games()
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error deleting game: {e}")

    else:
        st.warning("No games found in the database.")

    # Add a new game
    st.subheader("Add a New Game")
    with st.form("add_game_form"):
        inputs = {
            "appid": st.text_input("App ID"),
            "name": st.text_input("Name"),
            "release_date": st.text_input("Release Date"),
            "english": st.text_input("English"),
            "developer": st.text_input("Developer"),
            "publisher": st.text_input("Publisher"),
            "platforms": st.text_input("Platforms"),
            "required_age": st.text_input("Required Age"),
            "categories": st.text_input("Categories"),
            "genres": st.text_input("Genres"),
            "steamspy_tags": st.text_input("SteamSpy Tags"),
            "achievements": st.text_input("Achievements"),
            "positive_ratings": st.text_input("Positive Ratings"),
            "negative_ratings": st.text_input("Negative Ratings"),
            "average_playtime": st.text_input("Average Playtime"),
            "median_playtime": st.text_input("Median Playtime"),
            "owners": st.text_input("Owners"),
            "price": st.text_input("Price"),
        }
        if st.form_submit_button("Add Game"):
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO SteamData (
                        appid, name, release_date, english, developer, publisher,
                        platforms, required_age, categories, genres, steamspy_tags,
                        achievements, positive_ratings, negative_ratings, average_playtime,
                        median_playtime, owners, price
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tuple(inputs.values()))
                conn.commit()
                conn.close()
                st.success("Game added successfully!")
                # Refresh the table
                df = fetch_games()
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error adding game: {e}")
                
# View Games
elif page == "View Games":
    st.title("View Games")
    df = fetch_games()
    st.dataframe(df)

# Prediction Pages
elif page == "Predict Playtime":
    st.title("Predict Average Playtime")
    st.write("Enter game details for prediction:")
    with st.form("playtime_form"):
        inputs = {
            "positive_ratings": st.number_input("Positive Ratings"),
            "negative_ratings": st.number_input("Negative Ratings"),
            "price": st.number_input("Price"),
            "achievements": st.number_input("Achievements"),
        }
        if st.form_submit_button("Predict Playtime"):
            input_df = pd.DataFrame([inputs])
            prediction = model_playtime.predict(input_df)[0]
            st.success(f"Predicted Average Playtime: {prediction:.2f}")

elif page == "Predict Ratings":
    st.title("Predict Positive Ratings")
    st.write("Enter game details for prediction:")
    with st.form("ratings_form"):
        inputs = {
            "negative_ratings": st.number_input("Negative Ratings"),
            "price": st.number_input("Price"),
            "achievements": st.number_input("Achievements"),
            "average_playtime": st.number_input("Average Playtime"),
        }
        if st.form_submit_button("Predict Ratings"):
            input_df = pd.DataFrame([inputs])
            prediction = model_ratings.predict(input_df)[0]
            st.success(f"Predicted Positive Ratings: {prediction:.2f}")

elif page == "Predict Pricing":
    st.title("Predict Game Pricing")
    st.write("Enter game details for prediction:")
    with st.form("pricing_form"):
        inputs = {
            "positive_ratings": st.number_input("Positive Ratings"),
            "negative_ratings": st.number_input("Negative Ratings"),
            "achievements": st.number_input("Achievements"),
            "average_playtime": st.number_input("Average Playtime"),
        }
        if st.form_submit_button("Predict Pricing"):
            input_df = pd.DataFrame([inputs])
            prediction = model_pricing.predict(input_df)[0]
            st.success(f"Predicted Price: ${prediction:.2f}")

elif page == "Predict Game Score":
    st.title("Predict Game Score")
    st.write("Enter game details for prediction:")
    with st.form("score_form"):
        inputs = {
            "is_action": st.number_input("Is Action"),
            "is_indie": st.number_input("Is Indie"),
            "is_casual": st.number_input("Is Casual"),
            "is_strat": st.number_input("Is Strategy"),
            "is_adv": st.number_input("Is Adventure"),
            "is_f2p": st.number_input("Is Free to Play"),
            "is_sim": st.number_input("Is Simulation"),
            "is_windows": st.number_input("Is Windows"),
            "is_mac": st.number_input("Is Mac"),
            "is_linux": st.number_input("Is Linux"),
        }
        if st.form_submit_button("Predict Score"):
            input_df = pd.DataFrame([inputs])
            prediction = model_game_score.predict(input_df)[0]
            st.success(f"Predicted Game Score: {prediction:.2f}")
