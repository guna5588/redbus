import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import streamlit as st 
from streamlit_option_menu import option_menu  #used for selecting an option from list of options in a menu
import plotly.express as px 
import plotly.graph_objects as go
from tabulate import tabulate
from datetime import time
 
#each bus we have to filter
#now we have to take route_name from each dataframe and then append to list
# Traverse through each row and append the 'Route_name' to the kerala list
#kerala bus
kerala=[]
df_k=pd.read_csv("h:/guvi_txt/new/kerala_data.csv")
for i,r in df_k.iterrows():  #traverse through each row
    kerala.append(r['Route_name'])   # add that row in new list


#Andhra bus
andhra=[]
df_a=pd.read_csv("h:/guvi_txt/new/andra_data.csv")
for i,r in df_a.iterrows():
    andhra.append(r['Route_name'])

#Assam bus
assam=[]
df_as=pd.read_csv("h:/guvi_txt/new/Assam_data.csv")
for i,r in df_as.iterrows():
    assam.append(r['Route_name'])


#goa bus
goa=[]
df_g=pd.read_csv("h:/guvi_txt/new/goa_data.csv")
for i,r in df_g.iterrows():
    goa.append(r['Route_name'])
    
#telungana
telungana=[]
df_t=pd.read_csv("h:/guvi_txt/new/telungana_data.csv")
for i,r in df_t.iterrows():
    telungana.append(r['Route_name'])

#Chandigarh
Chandigarh=[]
df_h=pd.read_csv("h:/guvi_txt/new/Chandigarh_data.csv")
for i,r in df_h.iterrows():
    Chandigarh.append(r['Route_name'])

#punjab bus
punjab=[]
df_pb=pd.read_csv("h:/guvi_txt/new/punjab_data.csv")
for i,r in df_pb.iterrows():
    punjab.append(r["Route_name"])

#rajasthan bus
rajasthan=[]
df_r=pd.read_csv("h:/guvi_txt/new/Rajasthan_data.csv")
for i,r in df_r.iterrows():
    rajasthan.append(r['Route_name'])
    
#Meghalaya bus
Meghalaya=[]
df_s=pd.read_csv("h:/guvi_txt/new/Meghalaya_data.csv")
for i,r in df_s.iterrows():
    Meghalaya.append(r["Route_name"])
    
#uttar pradesh bus
KAAC=[]
df_u=pd.read_csv("h:/guvi_txt/new/KAAC_data.csv")
for i,r in df_u.iterrows():
    KAAC.append(r['Route_name'])

# bus
Sikkim=[]
df_sk=pd.read_csv("h:/guvi_txt/new/Sikkim_data.csv")
for i,r in df_sk.iterrows():
    Sikkim.append(r['Route_name'])

#bihar
bihar=[]
df_sk=pd.read_csv("h:/guvi_txt/new/bihar_data.csv")
for i,r in df_sk.iterrows():
    bihar.append(r['Route_name'])

###############################################

# ---------------> STREAMLIT PART ------------>

###############################################



#setting streamlit page
st.set_page_config(layout="wide",page_icon=":material/directions_bus:",page_title="RedBus Project",initial_sidebar_state="expanded")

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
    #THEME CONTROL  OPERATIONAL IN SIDEBAR
    
    
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


if menu=="Home":
    st.title(":red[:material/analytics:] :green[Redbus Data Scraping with Selenium  & Dynamic Filtering using Streamlit]")
    st.text("")
    st.subheader(" ")
    st.markdown(""" ### :violet[:material/tooltip:] :red[Objective of the Project]

                To Scrape the Data from Redbus Website and to create a user interface and 
     dynamic filtration of data using streamlit and SQL 
    """)
    
    dfbus=pd.read_csv("h:/guvi_txt/new/combined_output.csv")#h:/guvi_txt/new
    dfbus['seats_available'] = dfbus['seats_available'].fillna(0)
    dfbus['number_of_customer_reviews'] = dfbus['number_of_customer_reviews'].fillna(0)
    dfbus['star_rating'] = dfbus['star_rating'].fillna(0)
    
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
    
    labels = dfbus['seats_available']
    values = dfbus['star_rating']
    
    
    fig1 = px.scatter(dfbus, 
                 x='price', 
                 y='number_of_customer_reviews', 
                 color='bus_type',
                 size='star_rating',
                 hover_name='bus_name',
                 title='Bus Price vs number_of_customer_reviews',
                 labels={'price': 'Ticket Price', 'number_of_customer_reviews': 'reviews'})

    # Display the plot in Streamlit
    st.plotly_chart(fig1)
    
    st.text("")
    
    labels1 = dfbus['star_rating']
    values1 = dfbus['number_of_customer_reviews']

        
    # Separate government and private buses
    dfbus['bus_type'] = dfbus['bus_name'].apply(lambda x: 'government' if any(keyword in x for keyword in 
        ['APSRTC', 'KSRTC', 'CTU', 'UPSRTC', 'RSRTC', 'BSRTC', 'PEPSU', 'TSRTC', 'HRTC', 'Assam State Transport Corporation', 
        'KAAC', 'KTCL', 'SNT', 'TGSRTC']) else 'private')

    # Filter buses with zero customer reviews and zero star ratings
    zero_reviews = dfbus[dfbus['number_of_customer_reviews'] == 0]
    zero_star_ratings = dfbus[dfbus['star_rating'] == 0]
    # Step 1: Filter out government buses only
    gov_buses = dfbus[dfbus['bus_type'] == 'government']

    # Step 2: Group by each specific government bus (using `bus_name`) for zero reviews and zero star ratings
    # Count zero star ratings
    zero_star_ratings_grouped = gov_buses[gov_buses['star_rating'] == 0].groupby('bus_name').size().reset_index(name='zero_star_rating_count')

    # Count zero reviews
    zero_reviews_grouped = gov_buses[gov_buses['number_of_customer_reviews'] == 0].groupby('bus_name').size().reset_index(name='zero_review_count')

    # Step 3: Merge the two counts (zero star ratings and zero reviews) into one DataFrame
    gov_zero_grouped = pd.merge(zero_star_ratings_grouped, zero_reviews_grouped, on='bus_name', how='outer').fillna(0)

    # Optional: Sort by bus_name or any other criteria
    gov_zero_grouped = gov_zero_grouped.sort_values('bus_name')



    # Scatter plot with lines and spikes
    fig2 = px.scatter(dfbus, 
                    x='price', 
                    y='number_of_customer_reviews', 
                    color='bus_type',  # Distinguishing between government and private buses
                    size='star_rating',
                    hover_name='bus_name',
                    title='Bus Price vs Number of Customer Reviews',
                    labels={'price': 'Ticket Price', 'number_of_customer_reviews': 'Number of Reviews'})

    # Adding separate traces for zero reviews and zero star rating buses

    # Define colors for better contrast
    color_map = {'government': 'blue', 'private': 'orange'}

    # Plot 1: Price vs Number of Customer Reviews
    fig3 = px.scatter(dfbus, 
                    x='price', 
                    y='number_of_customer_reviews', 
                    color='bus_type',
                    color_discrete_map=color_map,
                    size='star_rating',
                    hover_name='bus_name',
                    title='Price vs Number of Customer Reviews',
                    labels={'price': 'Ticket Price', 'number_of_customer_reviews': 'Number of Reviews'})

    # Plot 2: Price vs Star Rating
    fig4 = px.scatter(dfbus, 
                    x='price', 
                    y='star_rating', 
                    color='bus_type',
                    color_discrete_map=color_map,
                    size='number_of_customer_reviews',
                    hover_name='bus_name',
                    title='Price vs Star Rating',
                    labels={'price': 'Ticket Price', 'star_rating': 'Star Rating'})

    # Plot 3: Star Rating vs Number of Customer Reviews
    fig5 = px.scatter(dfbus, 
                    x='star_rating', 
                    y='number_of_customer_reviews', 
                    color='bus_type',
                    color_discrete_map=color_map,
                    size='price',
                    hover_name='bus_name',
                    title='Star Rating vs Number of Customer Reviews',
                    labels={'star_rating': 'Star Rating', 'number_of_customer_reviews': 'Number of Reviews'})

    # Add separate traces for zero reviews and zero star ratings in the Price vs Reviews plot (fig1)
    fig3.add_scatter(x=zero_reviews['price'], 
                    y=zero_reviews['number_of_customer_reviews'], 
                    mode='markers+lines',
                    name='Zero Reviews (Gov/Private)',
                    line=dict(color='green', dash='dash'))

    fig3.add_scatter(x=zero_star_ratings['price'], 
                    y=zero_star_ratings['number_of_customer_reviews'], 
                    mode='markers+lines',
                    name='Zero Star Ratings (Gov/Private)',
                    line=dict(color='red', dash='dot'))

    # Add separate traces in the Price vs Star Rating plot (fig2)
    fig4.add_scatter(x=zero_reviews['price'], 
                    y=zero_reviews['star_rating'], 
                    mode='markers+lines',
                    name='Zero Reviews (Gov/Private)',
                    line=dict(color='green', dash='dash'))

    fig4.add_scatter(x=zero_star_ratings['price'], 
                    y=zero_star_ratings['star_rating'], 
                    mode='markers+lines',
                    name='Zero Star Ratings (Gov/Private)',
                    line=dict(color='red', dash='dot'))

    # Add separate traces in the Star Rating vs Reviews plot (fig3)
    fig5.add_scatter(x=zero_star_ratings['star_rating'], 
                    y=zero_star_ratings['number_of_customer_reviews'], 
                    mode='markers+lines',
                    name='Zero Star Ratings (Gov/Private)',
                    line=dict(color='red', dash='dot'))

    fig5.add_scatter(x=zero_reviews['star_rating'], 
                    y=zero_reviews['number_of_customer_reviews'], 
                    mode='markers+lines',
                    name='Zero Reviews (Gov/Private)',
                    line=dict(color='green', dash='dash'))

    # Show the plots
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)
    st.plotly_chart(fig5)
    


    # Step 1: Filter buses with zero star ratings and zero reviews
    
    zero_reviews_df = dfbus[(dfbus['number_of_customer_reviews'] == 0) & (dfbus['price'] <= 12000)]

    zero_star_df = dfbus[(dfbus['star_rating'] == 0) & (dfbus['price'] <= 12000)]

# Step 3: Group by bus type and count the number of buses with zero star rating
    bus_count = zero_star_df.groupby(['bus_name', 'bus_type']).size().reset_index(name='count')
    # Step 3: Group by both 'bus_name' and 'bus_type' to get details of buses with zero reviews
    
    fig6 = px.bar(bus_count, 
                    x='bus_type', 
                    y='count', 
                    color='bus_type', 
                    title='Count of Buses with Zero Star Ratings (Price <= 12,000)',
                    labels={'bus_type': 'Bus Type', 'count': 'Bus Count'},
                    hover_data=['bus_name'],  # Adding bus_name to hover data for details
                    color_discrete_map={'government': 'blue', 'private': 'orange'})

        
        




        # Step 3: Group by price range and bus type, then count buses for each category
        # Zero star rating buses
   
    # Zero review buses
    bus_count = zero_reviews_df.groupby(['bus_name', 'bus_type']).size().reset_index(name='count')

    # Step 4: Plot the bar chart
    # Step 4: Plot the bar chart for buses with zero reviews
    fig7 = px.bar(bus_count, 
                    x='bus_type', 
                    y='count', 
                    color='bus_type', 
                    title='Count of Buses with Zero Reviews (Price <= 12,000)',
                    labels={'bus_type': 'Bus Type', 'count': 'Bus Count'},
                    hover_data=['bus_name'],  # Adding bus_name to hover data for details
                    color_discrete_map={'government': 'blue', 'private': 'orange'})

        # Step 3: Group by price range and bus type, then count buses for each category
   
    # Optional: Combine zero star ratings and zero reviews into a single plot (if needed)
   
    # Step 5: Show the plots
    st.plotly_chart(fig7)
    st.plotly_chart(fig6)
    bus_count_reviews = zero_reviews_df.groupby('bus_type').size().reset_index(name='count')
    bus_count_star = zero_star_df.groupby('bus_type').size().reset_index(name='count')


    # Pie chart for zero star ratings (fig8)
    fig8 = px.pie(bus_count_star, 
                names='bus_type', 
                values='count', 
                title='Proportion of Buses with Zero Star Ratings (Price <= 12,000)',
                color_discrete_map=color_map)

    # Pie chart for zero reviews (fig9)
    fig9 = px.pie(bus_count_reviews, 
                names='bus_type', 
                values='count', 
                title='Proportion of Buses with Zero Reviews (Price <= 12,000)',
                color_discrete_map=color_map)
    st.plotly_chart(fig8)
    st.plotly_chart(fig9)
    

  #Function to plot Customer Reviews vs Star Rating
    
    

    
    
# Color map for bus types with strong contrast
    
    
    
    
# "Bus Routes" Section (already implemented, no changes needed here)
if menu == "Bus Routes":
    
    st.title(" :blue[:material/filter_alt:] :red[Dynamic Filtering of Data]")
    
    col1, col2 = st.columns(2)

    
    # Define the filters for rating, fare range, and bus type
        


    
# Define the filtering function
    def type_and_fare(bus_type, fare_min, fare_max, rate_range, bus_name, selected_departing_time):
        # Time format dictionary
        time_format = {
            "06:00 - 12:00 Morning": ("06:00:00", "12:00:00"),
            "12:00 - 18:00 Afternoon": ("12:00:00", "18:00:00"),
            "18:00 - 24:00 Evening": ("18:00:00", "24:00:00"),
            "00:00 - 06:00 Night": ("00:00:00", "06:00:00")
        }

        # Fetch the selected time range from the selectbox
        if selected_departing_time in time_format:
            start_time, end_time = time_format[selected_departing_time]
        else:
            start_time, end_time = None, None  # Handle cases where no time range is selected

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
            rate_min, rate_max = 4.1, 5
        elif rate_range == '4':
            rate_min, rate_max = 3.1, 4.0
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
            AND {bus_type_option}
            AND route_name = '{k}'
            
        """
        if start_time and end_time:
            mysql_query += f" AND TIME(departing_time) BETWEEN '{start_time}' AND '{end_time}'"

        mysql_query += f"""
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            ORDER BY price DESC, departing_time ASC;
        """
        
        mycursor.execute(mysql_query)
        output = mycursor.fetchall()

            # Convert the result to a DataFrame
        df = pd.DataFrame(output, columns=[
                "id", "route_date", "route_name", "route_link", "bus_name", "bus_type", "departing_time", "duration",
                "reaching_time", "departure_place", "destination_place", "star_rating", "number_of_customer_reviews",
                "price", "deal_price", "seats_available", "window_seats"
            ])

            # Handle NaN values for 'star_rating' and 'number_of_customer_reviews'
        df['star_rating'].fillna(0, inplace=True)  # Replace NaN with 0 in star_rating
        df['number_of_customer_reviews'].fillna(0, inplace=True)  # Replace NaN with 0 in number_of_customer_reviews

            # Convert 'departing_time' and 'reaching_time' columns to time format
        df['departing_time'] = df['departing_time'].apply(lambda x: (pd.Timestamp('today') + x).time())
        df['reaching_time'] = df['reaching_time'].apply(lambda x: (pd.Timestamp('today') + x).time())

        
            # Create scatter plot based on filtered data
        fig1 = px.scatter(df,
                            x='price',
                            y='number_of_customer_reviews',
                            color='bus_type',
                            size='star_rating',
                            hover_name='bus_name',
                            title='Bus Price vs Customer Reviews',
                            labels={'price': 'Ticket Price', 'number_of_customer_reviews': 'Reviews'})
            
            # Display the plot in Streamlit
        zero_reviews_df = df[(df['number_of_customer_reviews'] == 0) & (df['price'] <= 12000)]

        zero_star_df = df[(df['star_rating'] == 0) & (df['price'] <= 12000)]

    # Step 3: Group by bus type and count the number of buses with zero star rating
        
        # Step 4: Plot the bar chart
        
        # Step 1: Group by both 'bus_name' and 'bus_type' to get details of buses with zero star ratings
        bus_count_star = zero_star_df.groupby(['bus_name', 'bus_type']).size().reset_index(name='count')

        # Step 2: Plot the bar chart for buses with zero star ratings
        fig2 = px.bar(bus_count_star, 
                    x='bus_type', 
                    y='count', 
                    color='bus_type', 
                    title='Count of Buses with Zero Star Ratings (Price <= 12,000)',
                    labels={'bus_type': 'Bus Type', 'count': 'Bus Count'},
                    hover_data=['bus_name'],  # Adding bus_name to hover data for details
                    color_discrete_map={'government': 'blue', 'private': 'orange'})

        # Step 3: Group by both 'bus_name' and 'bus_type' to get details of buses with zero reviews
        bus_count_reviews = zero_reviews_df.groupby(['bus_name', 'bus_type']).size().reset_index(name='count')

        # Step 4: Plot the bar chart for buses with zero reviews
        fig3 = px.bar(bus_count_reviews, 
                    x='bus_type', 
                    y='count', 
                    color='bus_type', 
                    title='Count of Buses with Zero Reviews (Price <= 12,000)',
                    labels={'bus_type': 'Bus Type', 'count': 'Bus Count'},
                    hover_data=['bus_name'],  # Adding bus_name to hover data for details
                    color_discrete_map={'government': 'blue', 'private': 'orange'})




            # Step 3: Group by price range and bus type, then count buses for each category
    
        # Optional: Combine zero star ratings and zero reviews into a single plot (if needed)
    
        # Step 5: Show the plots
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
        # Close the cursor and connection
        mycursor.close()
        mydb.close()
        return(df)
    






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
        # Streamlit selectbox for departure time range
        departure_time_options = ["", "06:00 - 12:00 Morning", "12:00 - 18:00 Afternoon", "18:00 - 24:00 Evening", "00:00 - 06:00 Night"]
        selected_departure_time = st.selectbox(
            "Departure Time",
            options=departure_time_options,
            index=departure_time_options.index(st.session_state.selected_departure_time) if 'selected_departure_time' in st.session_state else 0,
            key='selected_departure_time'
        )

# Handle the SQL query with proper time range



    # Sidebar to filter between government and private buses
    with st.sidebar:
        bus_name_option = st.radio("Select Bus Ownership", ["government", "private"])

    # Placeholder for further logic (query and data processing based on selections)
    st.write(f"Selected State: {state}")
    st.write(f"Selected Bus Type: {select_type}")
    st.write(f"Selected Fare Range: {select_fare[0]} - {select_fare[1]}")
    st.write(f"Selected Rating: {select_rating}")
    st.write(f"Selected Time format: {selected_departure_time}")
    st.write(f"Selected Bus Ownership: {bus_name_option}")

    


    # Kerala Bus Filtering
    
    if state == "kerala":
        with col2:
            k = st.selectbox("List of routes", kerala)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
    # Kerala Bus Filtering
    
    if state == "Andhra Pradesh":
        with col2:
            k = st.selectbox("List of routes", andhra)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
    

    # telungana Bus Filtering
    
    if state =="Telangana":
        with col2:
            k = st.selectbox("List of routes", telungana)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
    # Meghalaya Bus Filtering
    
    if state =="Meghalaya":
        with col2:
            k = st.selectbox("List of routes", Meghalaya)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
    # Sikkim Bus Filtering
    
    if state =="Sikkim":
        with col2:
            k = st.selectbox("List of routes", Sikkim)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
    # goa Bus Filtering
    
    if state =="Goa":
        with col2:
            k = st.selectbox("List of routes", goa)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
    # KAAC Bus Filtering
    
    if state =="KAAC":
        with col2:
            k = st.selectbox("List of routes", KAAC)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
    #  assam Bus Filtering
    
    if state =="Assam":
        with col2:
            k = st.selectbox("List of routes", assam)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
    # rajasthan Bus Filtering
    
    if state =="Rajasthan":
        with col2:
            k = st.selectbox("List of routes", rajasthan)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
    # Bihar Bus Filtering
    
    if state =="Bihar":
        with col2:
            k = st.selectbox("List of routes", bihar)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
    # Chandigarh Bus Filtering
    
    if state =="Chandigarh":
        with col2:
            k = st.selectbox("List of routes", Chandigarh)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
    # Punjab Bus Filtering
    
    if state =="Punjab":
        with col2:
            k = st.selectbox("List of routes", punjab)
        
        # Call the function to get the filtered data
        df_result = type_and_fare(select_type, select_fare[0], select_fare[1], select_rating, bus_name_option, selected_departure_time)
       
        # Display the result in Streamlit
        st.subheader(":green[Result]")
        st.dataframe(df_result, use_container_width=True)
