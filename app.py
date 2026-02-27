import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Load Data --- #
df = pd.read_csv('data/apple_sales_data.csv')

# Subset non-returned data
df_net = df[df['return_status'] != 'Returned']


# --- Streamlit App --- #

## --- Page Configuration --- ##
st.set_page_config(
    page_title = 'Dashboard',
    layout = 'wide',
    page_icon='🍏',
)

st.title('Apple Sales Dashboard')
st.write('Welcome to the Apple Sales Dashboard! Explore key insights and trends in the sales data across different regions, products, and customer segments. Use the tabs below to navigate through various analyses and visualizations that will help you understand our performance and make informed decisions.')
st.write('<i>Note: All data is fictional and for portfolio purposes only.</i>',
         unsafe_allow_html=True)

## --- Tab Configuration --- ##
tab1, tab2, tab3, tab4 = st.tabs(['Executive Overview', 'Geographic Performance', 'Product & Prices Analytics', 'Customer Insights'])




