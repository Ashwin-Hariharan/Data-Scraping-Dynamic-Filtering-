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
    price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
    
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
    cursor.execute(query, (route_name, min_seats))  
    results = cursor.fetchall()  
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(results, columns=columns)
    cursor.close()
    connection.close()
    return df

# Main Streamlit app
def main():
    # Set page config for wider layout
    st.set_page_config(page_title="Bus Details Search", layout="wide")

    # Custom CSS to set background image and styling
    st.markdown("""
        <style>
            body {
                background-size: cover;
                background-position: center;
                color: white;
            }
            .title {
                font-size: 36px;
                font-weight: bold;
                color: #f6f4f0;  /* Dark color */
                text-align: center;  /* Center the title */
            }
            .subheader {
                color: #f6f4f0;  /* Light blue color */
            }
            .stButton>button {
                background-color: #31333F;  /* Gold color */
                color: white;
                font-size: 18px;
                border-radius: 5px;
                width: 100%;
            }
            .stButton>button:hover {
                background-color: white;  /* lighter shade on hover */
                color: #31333F;
            }
            .stTable {
                background-color: rgba(255, 255, 255, 0.8);  /* White with opacity for the table */
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title centered using a div in markdown with inline styles
    st.markdown("<div style='text-align: center;'><h1> Bus Details Search</h1></div>", unsafe_allow_html=True)
    st.markdown("---")  # Horizontal line for separation

    # Layout for inputs
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])  # Centered layout
        with col2:
            st.subheader("Search Parameters")
            route_name = st.text_input("Enter Route Name", "")
            price_sort_order = st.selectbox('Sort by Price', ['Low to High', 'High to Low'])
            min_seats = st.number_input("Seats Required", min_value=1, step=1, value=1)
            st.markdown("")

    # Centered button
    button_placeholder = st.container()
    with button_placeholder:
        col1, col2, col3 = st.columns([1, 20, 1])  # Center the button
        with col2:
            if st.button('🔍 Show Bus Details'):
                if route_name:
                    # Fetch and display bus details
                    bus_details = fetch_bus_details(route_name, min_seats, price_sort_order)
                    st.markdown("---")  # Horizontal line for separation
                    if not bus_details.empty:
                        st.success('Bus details fetched successfully!', icon="✅")
                        st.write(f"### Bus Details for Route: {route_name}")
                        
                        # Display the table in a full-width dataframe
                        
                        st.dataframe(
                            bus_details.style.format({
                                'price': '₹{:.2f}',  # Format price as currency
                                'star_rating': '{:.1f}',  # One decimal for star rating
                            }),
                            use_container_width=True  # Maximize table width
                        )
                    else:
                        st.warning("No buses found matching your criteria.")
                else:
                    st.error("Please enter a route name.")
    
    # Footer
    st.markdown("---")
    st.markdown("© 2024 Bus Finder | All rights reserved.")

if __name__ == '__main__':
    main()