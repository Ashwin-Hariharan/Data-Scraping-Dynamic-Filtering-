import streamlit as st
import mysql.connector
import pandas as pd

# Function to get connection to the database
def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",  
        database="busdetails"  
    )
    return connection

# Function to clear session state
def clear_session_state():
    # Clear the session state variables
    if 'state' in st.session_state:
        del st.session_state['state']
    if 'route_name' in st.session_state:
        del st.session_state['route_name']
    if 'bustype' in st.session_state:
        del st.session_state['bustype']
    if 'duration' in st.session_state:
        del st.session_state['duration']
    if 'departure_time' in st.session_state:
        del st.session_state['departure_time']
    if 'reaching_time' in st.session_state:
        del st.session_state['reaching_time']
    if 'price_range' in st.session_state:
        del st.session_state['price_range']
    if 'min_seats' in st.session_state:
        del st.session_state['min_seats']
    if 'min_rating' in st.session_state:
        del st.session_state['min_rating']
    if 'max_rating' in st.session_state:
        del st.session_state['max_rating']

# Function to fetch available states
def get_states():
    query = "SELECT DISTINCT state FROM bus_routes"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    states = [row[0] for row in results]
    return states

# Function to fetch route names based on the selected state
def get_route_names(state):
    query = "SELECT DISTINCT route_name FROM bus_routes WHERE state = %s"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, (state,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    route_names = [row[0] for row in results]
    return route_names

# Function to fetch bus types based on the selected state and route name
def get_bus_types(state, route_name):
    query = "SELECT DISTINCT bustype FROM bus_routes WHERE state = %s AND route_name = %s"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, (state, route_name))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    bus_types = [row[0] for row in results]
    return bus_types

# Function to fetch durations based on the selected state, route name, and bus type
def get_durations(state, route_name, bustype):
    query = "SELECT DISTINCT duration FROM bus_routes WHERE state = %s AND route_name = %s AND bustype = %s"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, (state, route_name, bustype))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    durations = [row[0] for row in results]
    return durations

# Function to fetch departure times based on the selected state, route name, bus type, and duration
def get_departure_times(state, route_name, bustype, duration):
    query = """
        SELECT DISTINCT departing_time 
        FROM bus_routes 
        WHERE state = %s 
        AND route_name = %s 
        AND bustype = %s 
        AND duration = %s
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, (state, route_name, bustype, duration))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return [row[0] for row in results]

# Function to fetch reaching times based on the selected state, route name, bus type, and duration
def get_reaching_times(state, route_name, bustype, duration):
    query = """
        SELECT DISTINCT reaching_time 
        FROM bus_routes 
        WHERE state = %s 
        AND route_name = %s 
        AND bustype = %s 
        AND duration = %s
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, (state, route_name, bustype, duration))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return [row[0] for row in results]

# Function to fetch bus details based on the filters
def fetch_bus_details(state, route_name, bustype, departure_time, duration, reaching_time, price_range, min_seats, min_rating, max_rating):
    query = """
        SELECT route_name, route_link, busname, bustype, departing_time, 
               duration, reaching_time, star_rating, price, seats_available 
        FROM bus_routes 
        WHERE state = %s
        AND route_name = %s
        AND bustype = %s
        AND departing_time = %s
        AND duration = %s
        AND reaching_time <= %s
        AND price BETWEEN %s AND %s
        AND seats_available >= %s
        AND star_rating BETWEEN %s AND %s
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, (state, route_name, bustype, departure_time, duration, reaching_time, price_range[0], price_range[1], min_seats, min_rating, max_rating))
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

    # Custom CSS for styling
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
                color: #f6f4f0;
                text-align: center;
            }
            .subheader {
                color: #f6f4f0;
            }
            .stButton>button {
                background-color: #31333F;
                color: white;
                font-size: 18px;
                border-radius: 5px;
                width: 100%;
            }
            .stButton>button:hover {
                background-color: white;
                color: #31333F;
            }
            .stTable {
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<div style='text-align: center;'><h1> Bus Details Search</h1></div>", unsafe_allow_html=True)
    st.markdown("---")  # Horizontal line for separation

    # Get available states from the database
    states = get_states()

    # Layout for inputs
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])  # Centered layout
        with col2:
            st.subheader("Search Parameters")

            # Select state with a default message
            state = st.selectbox("Select State", ["Select the state"] + states, key="state")

            if state != "Select the state":
                # Get available route names based on selected state
                route_names = get_route_names(state)
                route_name = st.selectbox("Select Bus Route", ["Select the bus route"] + route_names, key="route_name")

                if route_name != "Select the bus route":
                    # Get available bus types based on selected state and route
                    bustype = st.selectbox("Select Bus Type", ["Select the bus type"] + get_bus_types(state, route_name), key="bustype")

                    if bustype != "Select the bus type":
                        # Get available durations based on the selected state, route, and bus type
                        durations = ["Select Duration"] + get_durations(state, route_name, bustype)
                        duration = st.selectbox("Select Duration", durations, key="duration")

                        if duration != "Select Duration":
                            # Get departure and reaching times based on selected duration
                            departure_times = ["Select Departure Time"] + get_departure_times(state, route_name, bustype, duration)
                            departure_time = st.selectbox("Select Departure Time", departure_times, key="departure_time")

                            reaching_times = ["Select Reaching Time"] + get_reaching_times(state, route_name, bustype, duration)
                            reaching_time = st.selectbox("Select Reaching Time", reaching_times, key="reaching_time")

                            # Set price slider max limit based on fetched price range
                            price_range = (0, 1000)
                            min_seats = st.number_input("Seats Required", min_value=1, step=1, value=1, key="min_seats")
                            min_rating, max_rating = st.slider("Rating Range", min_value=1, max_value=5, value=(1, 5), key="rating")

                            price_min, price_max = st.slider("Price Range (₹)", min_value=price_range[0], max_value=price_range[1], value=price_range, key="price_range")
                            price_range = (price_min, price_max)  # Store slider values in the price_range tuple
                        
    # Fetch and display bus details when the button is clicked
    with st.container():
        col1, col2, col3 = st.columns([1, 20, 1])  # Centered layout for button and table
        with col2:
            if st.button("🔍 Show Bus Details"):
                bus_details = fetch_bus_details(state, route_name, bustype, departure_time, duration, reaching_time, price_range, min_seats, min_rating, max_rating)

                if not bus_details.empty:
                    st.success("Bus details fetched successfully!")

                    # Table display with width adjusted to 20
                    st.table(bus_details.style.format({
                        "price": "₹{:.2f}",  # Format price as currency
                        "star_rating": "{:.1f}",  # One decimal for star rating
                    }))
                else:
                    st.warning("No buses found matching your criteria.")
            if st.button("Reset Filters"):
                clear_session_state()
                st.session_state['state'] = "Select the state"  # Ensure the default state is reset
                st.session_state['route_name'] = "Select the bus route"
                st.session_state['bustype'] = "Select the bus type"
                st.session_state['duration'] = "Select Duration"
                st.session_state['departure_time'] = "Select Departure Time"
                st.session_state['reaching_time'] = "Select Reaching Time"
                st.rerun()  # This will force the app to rerun and reset everything 

    # Footer
    st.markdown("---")
    st.markdown("© 2024 Bus Finder | All rights reserved.")

if __name__ == "__main__":
    main()
