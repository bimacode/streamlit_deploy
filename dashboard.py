import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

df = pd.read_csv("https://raw.githubusercontent.com/bimacode/dicoding-bike-sharing/main/bikeshare_day_clean_new.csv")
df['dateday'] = pd.to_datetime(df['dateday'])


st.set_page_config(

    page_title="BIKE SHARING DASHBOARD",
    page_icon="bar_chart: ",
    layout="wide"
)

def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='dateday').agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })

    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "dateday": "yearmonth",
        "count": "total_bikers",
        "casual": "casual_bikers",
        "registered": "registered_bikers"
    }, inplace=True)

    return monthly_users_df


def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "count": "total_bikers",
        "casual": "casual_bikers",
        "registered": "registered_bikers"
    }, inplace=True)
    
    seasonly_users_df = pd.melt(seasonly_users_df,
                                      id_vars=['season'],
                                      value_vars=['casual_bikers', 'registered_bikers'],
                                      var_name='type_of_bikers',
                                      value_name='count_bikers')
    
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    
    return seasonly_users_df

min_date = df["dateday"].min()
max_date = df["dateday"].max()


with st.sidebar:
    # add capital bikeshare logo
    st.image("https://raw.githubusercontent.com/bimacode/dicoding-bike-sharing/main/pngwing.com.png")

    st.sidebar.header("Filter:")

    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.sidebar.header("Muhammad Bima Mauludin")

st.sidebar.markdown("mbima14_")

main_df = df[
    (df["dateday"] >= str(start_date)) &
    (df["dateday"] <= str(end_date))
]

monthly_users_df = create_monthly_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)

st.title(":bar_chart: Capital Bikeshare: Bike-Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_bikers = main_df['count'].sum()
    st.metric("Total Rides", value=total_all_bikers)
with col2:
    total_casual_bikers = main_df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_bikers)
with col3:
    total_registered_bikers = main_df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_bikers)
st.markdown("---")


fig = px.line(monthly_users_df,
              x='yearmonth',
              y=['casual_bikers', 'registered_bikers', 'total_bikers'],
              color_discrete_sequence=["skyblue", "orange", "red"],
              markers=True,
              title="Monthly Count of Bikeshare Rides").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

fig1 = px.bar(seasonly_users_df,
              x='season',
              y=['count_bikers'],
              color='type_of_bikers',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Count of bikeshare rides by season').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig1, use_container_width=True)
st.caption('Copyright (c), create with love by M.Bima Mauludin')