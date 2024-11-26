import streamlit as st
import mysql.connector
import pandas as pd

# Function to get connection to the database
def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",  # Replace with your actual password
        database="busdetails"  # Replace with your actual database name
    )
    return connection

# Function to fetch all bus details from the database based on route_name
def fetch_all_bus_details(route_name):
    # SQL Query to select all columns for the given route_name
    query = """
        SELECT route_name, route_link, busname, bustype, departing_time, 
               duration, reaching_time, star_rating, price, seats_available
        FROM bus_routes
        WHERE LOWER(route_name) = LOWER(%s)  # Case-insensitive matching
    """
    
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, (route_name,))  # Execute the query with the route name as a parameter
    results = cursor.fetchall()  # Fetch all rows of the result
    # Get column names from cursor description (the names of the selected fields)
    columns = [desc[0] for desc in cursor.description]

    # Convert the result into a DataFrame for easier display in Streamlit
    df = pd.DataFrame(results, columns=columns)

    cursor.close()
    connection.close()

    return df

# Main Streamlit app
def main():
    st.header('Bus Details')

    # Sidebar input for route name
    route_name = st.text_input("Enter Route Name", "")

    if route_name:
        # Fetch bus details based on route_name
        bus_details = fetch_all_bus_details(route_name)

        if not bus_details.empty:
            st.write(f"### Bus details for Route: {route_name}")
            st.table(bus_details)  # Display the full DataFrame in a tabular format
        else:
            st.write("No buses found for this route.")

if __name__ == '__main__':
    main()
