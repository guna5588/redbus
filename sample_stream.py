import pandas as pd
import mysql.connector
from datetime import time

import streamlit as st 
from streamlit_option_menu import option_menu  #used for selecting an option from list of options in a menu
import plotly.express as px 
import plotly.graph_objects as go
from tabulate import tabulate

# Load route names from the Kerala CSV file
kerala = []
df_k = pd.read_csv("h:/guvi_txt/new/kerala_data.csv")
for i, r in df_k.iterrows():
        kerala.append(r['Route_name'])
#Andhra bus
andhra=[]
df_a=pd.read_csv("h:/guvi_txt/new/andra_data.csv")
for i,r in df_a.iterrows():
    andhra.append(r['Route_name'])


###############################################

# ---------------> STREAMLIT PART ------------>

###############################################


#setting streamlit page
st.set_page_config(layout="wide", page_icon=":material/directions_bus:", page_title="RedBus Project", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    /* Ensure font size does not change on hover */
    .nav-link {
        font-size: 18px !important;
    }
    .nav-link:hover {
        font-size: 18px !important;
        color: #32789e !important; /* Change only the color on hover */
    }
    .nav-link-selected {
        font-size: 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Theme button in the sidebar
with st.sidebar:
    menu = option_menu(
        "Main Menu", 
        ["Home", 'Bus Routes'], 
        icons=['house', 'map'], 
        menu_icon="cast", 
        default_index=0,
        styles={
            "icon":{"font-size":"25px"}
        }
    )


# "Home" Section
if menu == "Home":
    st.title(":red[:material/analytics:] :green[Redbus Data Scraping with Selenium  & Dynamic Filtering using Streamlit]")
    st.text("")
    st.subheader(" ")
    st.markdown(""" ### :violet[:material/tooltip:] :red[Objective of the Project]

                To Scrape the Data from Redbus Website and to create a user interface and 
     dynamic filtration of data using streamlit and SQL 
    """)
    
    # Load bus data from combined_output.csv
    dfbus = pd.read_csv("h:/guvi_txt/new/combined_output.csv")  # Adjust the path if necessary

    # Scatter Plot: Price vs Star Rating
    fig = px.scatter(dfbus, 
                     x='price', 
                     y='star_rating', 
                     color='bus_type',
                     size='seats_available',
                     hover_name='bus_name',
                     title='Bus Price vs Ratings',
                     labels={'price': 'Ticket Price', 'star_rating': 'Bus Ratings'})

    # Display the plot in Streamlit
    st.plotly_chart(fig)

    st.text("")

    # Pie Chart: Distribution of Star Ratings based on Seats Available
    labels = dfbus['seats_available']
    values = dfbus['star_rating']

    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.1)])
    fig2.update_layout(
        title_text="Distribution of Star Ratings based on Seats Available",
        title_x=0.45
    )
    st.plotly_chart(fig2)
    

# "Bus Routes" Section (already implemented, no changes needed here)
if menu == "Bus Routes":
    
    st.title(" :blue[:material/filter_alt:] :red[Dynamic Filtering of Data]")
    
    col1, col2 = st.columns(2)

    # Traverse through each row and append the 'Route_name' to the kerala list
    
    # Define the filters for

# Define the filters for rating, fare range, and bus type
    def type_and_fare(bus_type, fare_min, fare_max, rate_range, bus_name, time_range):
        start_time, end_time = time_range

        # MySQL connection
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="coombined_data"  # Ensure your database name is correct
        )

        mycursor = mydb.cursor(buffered=True)

        # Filtration for rating
        if rate_range == "5":
            rate_min, rate_max = 4.2, 5
        elif rate_range == '4':
            rate_min, rate_max = 3.0, 4.2
        elif rate_range == "rating not an issue":
            rate_min, rate_max = 2.0, 5
        else:
            rate_min, rate_max = 0, 5

        # Route name filtration
        if bus_name == "government":
            bus_name_option = """
                (bus_name LIKE '%APSRTC%' OR bus_name LIKE '%KSRTC%' OR bus_name LIKE '%CTU%' OR 
                bus_name LIKE '%UPSRTC%' OR bus_name LIKE '%RSRTC%' OR bus_name LIKE '%BSRTC%' OR 
                bus_name LIKE '%PEPSU%' OR bus_name LIKE '%TSRTC%' OR bus_name LIKE '%HRTC%' OR 
                bus_name LIKE '%Assam State Transport Corporation%' OR bus_name LIKE '%KAAC%' OR 
                bus_name LIKE '%KTCL%' OR bus_name LIKE '%SNT%' OR bus_name LIKE '%TGSRTC%')
            """
        elif bus_name == "private":
            bus_name_option = """
                (bus_name NOT LIKE '%APSRTC%' AND bus_name NOT LIKE '%KSRTC%' AND bus_name NOT LIKE '%CTU%' AND 
                bus_name NOT LIKE '%UPSRTC%' AND bus_name NOT LIKE '%RSRTC%' AND bus_name NOT LIKE '%BSRTC%' AND 
                bus_name NOT LIKE '%PEPSU%' AND bus_name NOT LIKE '%TSRTC%' AND bus_name NOT LIKE '%HRTC%' AND 
                bus_name NOT LIKE '%Assam State Transport Corporation%' AND bus_name NOT LIKE '%KAAC%' AND 
                bus_name NOT LIKE '%KTCL%' AND bus_name NOT LIKE '%SNT%' AND bus_name NOT LIKE '%TGSRTC%')
            """

        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_option = "bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_option = "bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "seater":
            bus_type_option = "bus_type LIKE '%Seater%'"
        else:
            bus_type_option = """
                (bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%' AND bus_type NOT LIKE '%Seater%')
            """

        # SQL query to fetch data based on the filters
        mysql_query = f"""
            SELECT id, route_date, route_name, route_link, bus_name, bus_type, departing_time, duration, reaching_time, 
                departure_place, destination_place, star_rating, number_of_customer_reviews, price, deal_price, 
                seats_available, window_seats
            FROM combined_table
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND {bus_name_option}
            AND route_name = '{k}'
            AND {bus_type_option}
            AND departing_time BETWEEN '{start_time}' AND '{end_time}'
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            ORDER BY price DESC, departing_time ASC;
        """

        # Debugging: Print the SQL query (optional)
        st.write(mysql_query)  # Comment this out for production

        mycursor.execute(mysql_query)
        output = mycursor.fetchall()

        # Create DataFrame from output
        df = pd.DataFrame(output, columns=[
            "id", "route_date", "route_name", "route_link", "bus_name", "bus_type", "departing_time", "duration",
            "reaching_time", "departure_place", "destination_place", "star_rating", "number_of_customer_reviews",
            "price", "deal_price", "seats_available", "window_seats"
        ])

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        return df




    # Separate government and private buses into different tables (run this separately)
        # Streamlit UI code

    # Main layout for the bus filters
    st.title("Bus Search Filters") 

    col1, col2 = st.columns(2)

    # Dropdown for selecting the state
    with col1:
        state = st.selectbox("List of States", ["kerala", "Andhra Pradesh", "Telangana", "Goa", "Rajasthan", "Punjab", "Chandigarh", "Bihar", "Assam", "KAAC", "Sikkim", "Meghalaya"])

    # Bus type selection
    with col2:
        select_type = st.selectbox("Choose bus type", ["sleeper", "semi-sleeper", "seater", "others"])

    # Range slider for fare
    with col1:
        select_fare = st.slider("Choose bus fare range", min_value=100, max_value=11500, value=(40, 400), step=10)

    # Dropdown for selecting the rating
    with col2:
        select_rating = st.selectbox("Choose star_rating", ["5", "4", "rating not an issue", "off"])

    # Range slider for selecting time (in 24-hour format)
    with col1:
        TIME = st.slider("Select the time_range", min_value=time(0, 0), max_value=time(23, 59), value=(time(6, 0), time(23, 59)))

    # Sidebar to filter between government and private buses
    with st.sidebar:
        bus_name_option = st.radio("Select Bus Ownership", ["government", "private"])

    # Placeholder for further logic (query and data processing based on selections)
    st.write(f"Selected State: {state}")
    st.write(f"Selected Bus Type: {select_type}")
    st.write(f"Selected Fare Range: {select_fare[0]} - {select_fare[1]}")
    st.write(f"Selected Rating: {select_rating}")
    st.write(f"Selected Time Range: {TIME[0]} - {TIME[1]}")
    st.write(f"Selected Bus Ownership: {bus_name_option}")

# You can use the selected inputs here to query your MySQL database and display results
    start_time = TIME[0].strftime("%H:%M:%S")
    end_time = TIME[1].strftime("%H:%M:%S")
        

    # Kerala Bus Filtering
    if state == "kerala":
        with col2:
            k = st.selectbox("List of routes", kerala)
        
        # Call the function to get the filtered data
        # Make sure to unpack the fare range and format time values correctly
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, (start_time, end_time))
        ###sql_query = f"""
            #SELECT id, route_date, route_name, route_link, bus_name, bus_type, departing_time, duration, reaching_time, 
             #  seats_available, window_seats
            #FROM combined_table
                #WHERE route_name = '{k}'
##           ORDER BY price DESC, departing_time ASC;
  #      """
   #     my_cursor.execute(sql_query)
    #    out=my_cursor.fetchall()
     #   conn.close()
            
      #  df=pd.DataFrame(out,columns=[
       #         "ID","Bus_name","Route_name","Bus_type","Start_time","Duration","End_time","Ratings","Price","Seats_Available","Route_link"
        #    ])
            

        # Display the result in Streamlit
        st.subheader(":blue[Result]")
        st.dataframe(df_result, use_container_width=True)
    # Kerala Bus Filtering
    if state == "Andhra Pradesh":
        with col2:
            k = st.selectbox("List of routes", andhra)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, (start_time, end_time))

        # Display the result in Streamlit
        st.subheader(":blue[Result]")
        st.dataframe(df_result, use_container_width=True)


