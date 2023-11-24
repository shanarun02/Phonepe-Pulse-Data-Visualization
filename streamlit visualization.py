import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Database connection
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Arun@5851',
    database='phonepe'
)

# Create a cursor
mycursor = mydb.cursor()

# Streamlit app for Transaction Data Visualization
import streamlit as st

def load_data():
    query = "SELECT * FROM india_transaction_data;"
    df = pd.read_sql(query, mydb)
    return df

# Function to filter data based on selected year and quarters
def filter_data(df, selected_year, selected_quarters):
    # Adjust column names
    filtered_df = df[(df['Transaction_year'] == selected_year) & (df['Quarters'].isin(selected_quarters))]
    return filtered_df

# Function to create a pie chart using Plotly Express
def create_pie_chart(df):
    fig = px.pie(df, names='Transaction_Type', values='Transaction_count', title='Transaction Count by Type')
    return fig

# Streamlit app for Transaction Data Visualization
def main_transaction_data():
    st.title("Transaction Data Visualization")

    # Get unique years and quarters from india_transaction_data
    query_years = "SELECT DISTINCT Transaction_year FROM india_transaction_data"
    query_quarters = "SELECT DISTINCT Quarters FROM india_transaction_data"
    
    years = get_query_result(query_years)
    quarters = get_query_result(query_quarters)

    # Sidebar for user input
    st.sidebar.title("Transaction Data Options")
    selected_data_type = st.sidebar.radio("Select Data Type:", ["India", "State-wise", "Combined Analysis", "piechart"])
    
    if selected_data_type == "piechart":
        st.title("Overall Transaction Data")

        # Load data from the MySQL database
        data = load_data()

        # Create sidebar for user input
        st.sidebar.header("Select Filters")
        selected_year = st.sidebar.selectbox("Select Transaction Year", sorted(data['Transaction_year'].unique()))
        selected_quarters = st.sidebar.multiselect("Select Quarters", sorted(data['Quarters'].unique()))

        # Filter data based on user input
        filtered_data = filter_data(data, selected_year, selected_quarters)

        # Convert selected quarters to strings before joining
        selected_quarters_str = [str(q) for q in selected_quarters]

        # Display filtered data
        st.write(f"Displaying data for {selected_year} - Quarters: {', '.join(selected_quarters_str)}")

        # Create and display pie chart
        pie_chart = create_pie_chart(filtered_data)
        st.plotly_chart(pie_chart)

    elif selected_data_type == "India":
        selected_year = st.sidebar.selectbox("Select Transaction Year:", years)
        selected_quarter = st.sidebar.selectbox("Select Quarter:", quarters)

        st.subheader("India Transaction Data:")
        india_data = get_transaction_data("india_transaction_data", selected_year, selected_quarter)
        
        # Display the transaction data table
        st.write(india_data.drop(columns=["Transaction_year", "Quarters"]))
        
        # Get total transaction amount and count
        query_total = f"SELECT SUM(transaction_amount) as total_sales FROM india_transaction_data WHERE transaction_year='{selected_year}' AND quarters='{selected_quarter}'"
        query_count = f"SELECT SUM(transaction_count) as total_sales FROM india_transaction_data WHERE transaction_year='{selected_year}' AND quarters='{selected_quarter}'"
        
        total = get_query_result(query_total)
        count = get_query_result(query_count)

        if total and count:
            # Assuming total is a list
            formatted_total = [f"{amount:.2f}" for amount in total]
            formatted_total_str = ", ".join(formatted_total)
            st.markdown(f"**Total payment value:** {formatted_total_str}")

            # Assuming count is a list
            formatted_count = [f"{c:.0f}" for c in count]
            formatted_count_str = ", ".join(formatted_count)
            st.markdown(f"**All PhonePe transactions (UPI + Cards + Wallets):** {formatted_count_str}")
        else:
            st.warning("No data found for the selected year and quarter.")


    elif selected_data_type == "State-wise":
        # Get unique states from state_wise_transaction_data
        query_states = "SELECT DISTINCT name FROM state_wise_transaction_data"
    
        # Add a dropdown for selecting states
        selected_state = st.sidebar.selectbox("Select State:", get_query_result(query_states))

        # Get unique years and quarters based on the selected state
        state_query_years = f"SELECT DISTINCT Transaction_year FROM state_wise_transaction_data WHERE name = '{selected_state}'"
        state_query_quarters = f"SELECT DISTINCT Quarters FROM state_wise_transaction_data WHERE name = '{selected_state}'"
    
        state_years = get_query_result(state_query_years)
        state_quarters = get_query_result(state_query_quarters)

        # Add dropdowns for year and quarter
        selected_state_year = st.sidebar.selectbox("Select State-wise Transaction Year:", state_years)
        selected_state_quarter = st.sidebar.selectbox("Select State-wise Quarter:", state_quarters)

        # Use placeholders in the queries and remove hardcoded values
        query_total_amount = f"SELECT SUM(transaction_amount) FROM state_wise_transaction_data WHERE name = '{selected_state}' AND transaction_year = '{selected_state_year}' AND Quarters = '{selected_state_quarter}'"
        query_total_count = f"SELECT SUM(transaction_count) FROM state_wise_transaction_data WHERE name = '{selected_state}' AND transaction_year = '{selected_state_year}' AND Quarters = '{selected_state_quarter}'"

        total_amount = get_query_result(query_total_amount)
        total_count = get_query_result(query_total_count)

        st.subheader("State-wise Transaction Data:")
        state_data = get_state_transaction_data("state_wise_transaction_data", selected_state, selected_state_year, selected_state_quarter)
    
        # Remove Transaction_year and Quarters columns only in the displayed output table
        st.write(state_data.drop(columns=["Transaction_year", "Quarters"])) 
    
        # Assuming total_amount is a list
        formatted_total_amount = [f"{amount:.2f}" for amount in total_amount]
        formatted_total_amount_str = ", ".join(formatted_total_amount)
        st.markdown(f"**Total payment value:** {formatted_total_amount_str}")

        # Assuming total_count is a list
        formatted_total_count = [f"{count:.0f}" for count in total_count]
        formatted_total_count_str = ", ".join(formatted_total_count)

        # Use the formatted value in your Markdown string
        st.markdown(f"**All PhonePe transactions (UPI + Cards + Wallets):** {formatted_total_count_str}")




    # ...

    elif selected_data_type == "Combined Analysis":
        # Get unique years, quarters, and names from india_map_trans
        map_query_years = "SELECT DISTINCT year FROM india_map_trans"
        map_query_quarters = "SELECT DISTINCT quarter FROM india_map_trans"
        map_query_names = "SELECT DISTINCT name FROM india_map_trans"
        map_years = get_query_result(map_query_years)
        map_quarters = get_query_result(map_query_quarters)
        map_names = get_query_result(map_query_names)

        # Add dropdowns for year, quarter, and name
        selected_map_year = st.sidebar.selectbox("Select Map Year:", map_years)
        selected_map_quarter = st.sidebar.selectbox("Select Map Quarter:", map_quarters)
        selected_map_name = st.sidebar.selectbox("Select Name:", map_names)

        st.subheader("India Transaction:")
        india_data = get_transaction_data("india_transaction_data", selected_map_year, selected_map_quarter)
        #Remove Transaction_year and Quarters columns only in the displayed output table
        st.write(india_data.drop(columns=["Transaction_year", "Quarters"]))

        st.subheader("State Transaction :")
        state_data = get_state_transaction_data("state_wise_transaction_data", selected_map_name, selected_map_year, selected_map_quarter)
        # Remove Transaction_year and Quarters columns only in the displayed output table
        st.write(state_data.drop(columns=["Transaction_year", "Quarters"]))
        st.subheader("India Map Transaction Data:")

        # Show combined data for India Map
        map_data_individual = get_map_transaction_data("india_map_trans", selected_map_year, selected_map_quarter, selected_map_name)
        st.write(f"Simplified State Data ---> {selected_map_name}:")
        st.write(map_data_individual)

        # Calculate total for India
        query_total_india = f"SELECT SUM(transaction_amount) as total_sales FROM india_transaction_data WHERE transaction_year='{selected_map_year}' AND quarters='{selected_map_quarter}'"
        query_count_india = f"SELECT SUM(transaction_count) as total_sales FROM india_transaction_data WHERE transaction_year='{selected_map_year}' AND quarters='{selected_map_quarter}'"

        total_india = get_query_result(query_total_india)
        count_india = get_query_result(query_count_india)

        if total_india and count_india:
            # Assuming total_india is a list
            formatted_total_india = [f"{amount:.2f}" for amount in total_india]
            formatted_total_india_str = ", ".join(formatted_total_india)
            st.markdown(f"**Total payment value for India:** {formatted_total_india_str}")

            # Assuming count_india is a list
            formatted_count_india = [f"{c:.0f}" for c in count_india]
            formatted_count_india_str = ", ".join(formatted_count_india)
            st.markdown(f"**All PhonePe transactions for India (UPI + Cards + Wallets):** {formatted_count_india_str}")
        else:
            st.warning("No data found for the selected year and quarter in India.")



# Streamlit app for User Data Visualization
def main_user_data():
    st.title("User Data Visualization")

    # Get unique years from india_user_data
    query_years_india = "SELECT DISTINCT year FROM india_user_data"
    years_india = get_query_result(query_years_india)

    # Get unique quarters from india_user_data
    query_quarters_india = "SELECT DISTINCT quarter FROM india_user_data"
    quarters_india = get_query_result(query_quarters_india)

    # Get unique years from top_india_state_data
    query_years_top = "SELECT DISTINCT year FROM top_india_state_data"
    years_top = get_query_result(query_years_top)

    # Get unique quarters from top_india_state_data
    query_quarters_top = "SELECT DISTINCT quarter FROM top_india_state_data"
    quarters_top = get_query_result(query_quarters_top)

    # Sidebar for user input
    st.sidebar.title("User Data Options")
    selected_table = st.sidebar.selectbox("Select Table:", ["India", "Top India State"])

    if selected_table == "India":
        selected_year = st.sidebar.selectbox("Select Year:", years_india)
        selected_quarter = st.sidebar.selectbox("Select Quarter:", quarters_india)


        st.subheader("India User Data:")
        india_user_data = get_user_data("india_user_data", selected_year, selected_quarter)
        # Display brand and count columns only in the output table
        st.table(india_user_data[["brand", "count"]])

    elif selected_table == "Top India State":
        selected_year = st.sidebar.selectbox("Select Year:", years_top)
        selected_quarter = st.sidebar.selectbox("Select Quarter:", quarters_top)

        st.subheader("Top India State Data:")
        top_india_state_data = get_top_data("top_india_state_data", selected_year, selected_quarter)
        # Display entityname, count, and amount columns only in the output table
        st.table(top_india_state_data[["entityname", "count", "amount"]])

def get_query_result(query):
    mycursor.execute(query)
    result = mycursor.fetchall()
    return [item[0] for item in result]

def get_transaction_data(table_name, year, quarter):
    query = f"SELECT * FROM {table_name} WHERE Transaction_year = {year} AND Quarters = '{quarter}'"
    mycursor.execute(query)
    result = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]
    return pd.DataFrame(result, columns=columns)

def get_state_transaction_data(table_name,name, year, quarter):
    query = f"SELECT * FROM {table_name} WHERE  Transaction_year = {year} AND Quarters = '{quarter}' AND Name = '{name}'"
    mycursor.execute(query)
    result = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]
    return pd.DataFrame(result, columns=columns)

def get_map_transaction_data(table_name, year, quarter, name):
    query = f"SELECT * FROM {table_name} WHERE year = {year} AND quarter = '{quarter}' AND name = '{name}'"
    mycursor.execute(query)
    result = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]
    return pd.DataFrame(result, columns=columns)

def get_user_data(table_name, year, quarter):
    query = f"SELECT brand, count FROM {table_name} WHERE year = {year} AND quarter = '{quarter}' "
    mycursor.execute(query)
    result = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]
    return pd.DataFrame(result, columns=columns)

def get_top_data(table_name, year, quarter):
    query = f"SELECT entityname, count, amount FROM {table_name} WHERE year = {year} AND quarter = '{quarter}' "
    mycursor.execute(query)
    result = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]
    return pd.DataFrame(result, columns=columns)

if __name__ == "__main__":
    # Run the respective main functions based on the selected app
    selected_app = st.sidebar.selectbox("Select App:", ["Transaction Data Visualization", "User Data Visualization"])
    if selected_app == "Transaction Data Visualization":
        main_transaction_data()
    elif selected_app == "User Data Visualization":
        main_user_data()



