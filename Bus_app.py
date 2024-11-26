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

# Function to fetch bus details from the database based on route_name, seats, and price sort order
def fetch_bus_details(route_name, min_seats, price_sort_order):
    # SQL Query to select bus details with filtering based on seat availability
    price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
    
    # Correct query with price sorting applied properly
    query = f"""
        SELECT route_name, route_link, busname, bustype, departing_time, 
               duration, reaching_time, star_rating, price, seats_available 
        FROM bus_routes 
        WHERE LOWER(route_name) = LOWER(%s) 
        AND seats_available >= %s
        ORDER BY price {price_sort_order_sql}, star_rating DESC
    """
    
    connection = get_connection()
    cursor = connection.cursor()
    
    # Execute the query with the correct number of parameters
    cursor.execute(query, (route_name, min_seats))  
    
    # Fetch all rows of the result
    results = cursor.fetchall()  
    
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

    # Dropdown for sorting by price
    price_sort_order = st.selectbox('Sort by Price', ['Low to High', 'High to Low'])

    # Input fields for filtering by seat availability
    min_seats = st.number_input("Minimum Seats Available", min_value=1, step=1, value=1)
    
    # Button to fetch and display details
    if st.button('Show Bus Details'):
        if route_name:
            # Fetch bus details based on route_name, min_seats, and price_sort_order
            bus_details = fetch_bus_details(route_name, min_seats, price_sort_order)

            if not bus_details.empty:
                st.write(f"### Bus details for Route: {route_name}")
                st.dataframe(bus_details)  # Display the full DataFrame in a tabular format
            else:
                st.write("No buses found matching your criteria.")
        else:
            st.write("Please enter a route name.")

if __name__ == '__main__':
    main()
