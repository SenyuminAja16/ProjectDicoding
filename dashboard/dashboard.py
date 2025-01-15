import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_monthly_rent_df(df):
    monthly_rent_df = df.resample(rule='ME', on='dteday').agg({
        'casual_x' : 'sum',
        'registered_x' : 'sum'
    })
    
    monthly_rent_df.index = monthly_rent_df.index.strftime('%B %Y')
    monthly_rent_df = monthly_rent_df.reset_index()
    
    return monthly_rent_df

def create_day_rent_df(df):
    day_rent_df = df.groupby(by='day').cnt_x.sum().reset_index()
    day_rent_df['day'] = pd.Categorical(day_rent_df['day'], ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
    
    return day_rent_df

def create_bytemp_df(df):
    bytemp_df = df.groupby(by='category_temp').cnt_x.sum().reset_index()
    bytemp_df['category_temp'] = pd.Categorical(bytemp_df['category_temp'], ['Low', 'Medium-Low', 'Medium-high', 'High'])
    
    return bytemp_df

def create_byhumidity_df(df):
    byhumidity_df = df.groupby(by='category_humidity').cnt_x.sum().reset_index()
    byhumidity_df['category_humidity'] = pd.Categorical(byhumidity_df['category_humidity'], ['Low Humidity', 'Moderate Humidity', 'High Humidity', 'Very High Humidity'])
    
    return byhumidity_df

def create_bywindspeed_df(df):
    bywindspeed_df = df.groupby(by='category_windspeed').cnt_x.sum().reset_index()
    bywindspeed_df['category_windspeed'] = pd.Categorical(bywindspeed_df['category_windspeed'], ['Calm Wind', 'Gentle Wind', 'Moderate Wind', 'Strong Wind'])

    return bywindspeed_df

def create_byhour_df(df):
    byhour_df = df.groupby(by='hr').cnt_x.sum().reset_index()
    return byhour_df

def create_bycategory_day_df(df):
    bycategory_day_df = df.groupby(by='category_day').cnt_x.sum().reset_index()
    return bycategory_day_df

def create_byweathersit_df(df):
    byweathersit_df = df.groupby(by='weathersit_x').cnt_x.mean().reset_index()
    return byweathersit_df

def create_byseason_df(df):
    byseason_df = df.groupby(by='category_season').cnt_x.sum().reset_index()
    return byseason_df

def create_comparasion_bycategory_day_df(df):
    diferent_bycategory_day_df = df.groupby(by='category_day').agg({
        'casual_x' : 'sum',
        'registered_x' : 'sum'
    }).reset_index()
    
    return diferent_bycategory_day_df

def create_total_casual_rent_df(df):
    total_casual_rent = df.casual_x.sum()
    return total_casual_rent

def create_total_registered_rent_df(df):
    total_registered_df = df.registered_x.sum()
    return total_registered_df

hour_day_df = pd.read_csv('dashboard/hour_day_df.csv')

datetime_columns = ['dteday']
hour_day_df.sort_values(by='dteday', inplace=True)
hour_day_df.reset_index(inplace=True)

for columns in datetime_columns:
    hour_day_df[columns] = pd.to_datetime(hour_day_df[columns])
    
min_date = hour_day_df['dteday'].min()
max_date = hour_day_df['dteday'].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Watu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date,max_date]
    )

main_df = hour_day_df[(hour_day_df['dteday'] >= str(start_date)) & (hour_day_df['dteday'] <= str(end_date))]

monthly_rent_df = create_monthly_rent_df(main_df)
day_rent_df = create_day_rent_df(main_df)
bytemp_df = create_bytemp_df(main_df)
byhumidity_df = create_byhumidity_df(main_df)
bywindspeed_df = create_bywindspeed_df(main_df)
byhour_df = create_byhour_df(main_df)
bycategory_day_df = create_bycategory_day_df(main_df)
byweathersit_df = create_byweathersit_df(main_df)
byseason_df = create_byseason_df(main_df)
comparasion_bycategory_day_df = create_comparasion_bycategory_day_df(main_df)
total_casual = create_total_casual_rent_df(main_df)
total_registred = create_total_registered_rent_df(main_df)

st.header('Bike Sharing Dataset :sparkles:')
col1, col2 = st.columns(2)
with col1:
    total_casual = monthly_rent_df['casual_x'].sum()
    st.metric('Total Casual: ', value=total_casual)

with col2:
    total_registred = monthly_rent_df['registered_x'].sum()
    st.metric('Total Registered', value=total_registred)

fig, ax = plt.subplots(figsize=(100,20))
ax.plot(monthly_rent_df['dteday'], monthly_rent_df['casual_x'], marker='o', linewidth=2, label='casual', color='red')
ax.plot(monthly_rent_df['dteday'], monthly_rent_df['registered_x'], marker='o', linewidth=2, label='registered', color='green')
ax.legend(fontsize=30)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

st.header('Most Frequent Rental Time')

fig, ax = plt.subplots(figsize=(35,15))
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3",  "#D3D3D3","#72BCD4", "#D3D3D3", ]
sns.barplot(data=day_rent_df, x=day_rent_df['day'], y=day_rent_df['cnt_x'], palette=colors)
ax.set_title('Frequency in Days', loc='center', fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=35)
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35,15))
sns.barplot(data=byhour_df, x=byhour_df['hr'], y=byhour_df['cnt_x'])
ax.set_title('Frequency in Hours', loc='center', fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=35)
ax.set_xlabel('24 Hours', loc='center', fontsize=30)
ax.set_ylabel(None)
st.pyplot(fig)


st.header('Amount of Rent Based on Natural Conditions')
fig, ax = plt.subplots(figsize=(35,15))
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]
sns.barplot(data=bytemp_df, x=bytemp_df['category_temp'], y=bytemp_df['cnt_x'], palette=colors)
ax.set_title('Frequency by Temperature', loc='center', fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=35)
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35,15))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(data=byhumidity_df, x=byhumidity_df['category_humidity'], y=byhumidity_df['cnt_x'], palette=colors)
ax.set_title('Frequency by Humidity', loc='center', fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=35)
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35,15))
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]
sns.barplot(data=bywindspeed_df, x=bywindspeed_df['category_windspeed'], y=bywindspeed_df['cnt_x'], palette=colors)
ax.set_title('Frequency by Windspeed', loc='center', fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=35)
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35,15))
colors = ["#72BCD4","#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(data=byweathersit_df, x=byweathersit_df['weathersit_x'], y=byweathersit_df['cnt_x'], palette=colors)
ax.set_title('Frequency by weathersit', loc='center', fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=35)
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35,15))
colors = ["#72BCD4","#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(data=byseason_df, x=byseason_df['category_season'], y=byseason_df['cnt_x'], palette=colors)
ax.set_title('Frequency by Season', loc='center', fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=35)
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

st.header('Comaparasion of Casual & Registered User')
fig,ax = plt.subplots(ncols=2, nrows=1, figsize=(35,15))
color = ['green', 'blue']
ax[0].pie(x=comparasion_bycategory_day_df['casual_x'], labels=comparasion_bycategory_day_df['category_day'], autopct='%1.1f%%', colors=color,textprops={'fontsize':20})
ax[0].set_title('Number of Casual by Category Day', fontsize=30)

ax[1].pie(x=comparasion_bycategory_day_df['registered_x'], labels=comparasion_bycategory_day_df['category_day'], autopct='%1.1f%%', colors=color, textprops={'fontsize':20})
ax[1].set_title('Number of Registered by Category Day', fontsize=30)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35,15))
plt.pie(x=bycategory_day_df['cnt_x'], labels=bycategory_day_df['category_day'], autopct='%1.1f%%', colors=color, textprops={'fontsize':20})
ax.set_title('Number of rent by Category Day (Causal + registered)', fontsize=30)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35,15))
plt.pie(x=[total_casual,total_registred], labels=['Casual', 'Registered'], autopct='%1.1f%%', colors=color, textprops={'fontsize':30})
ax.set_title('comparison of casual and registered rentals', fontsize=30)
st.pyplot(fig)
