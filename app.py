#Importing Necessary Libraries
import pickle
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

#Page Configs
st.set_page_config(page_title='Weather Prediction', page_icon='./assets/icon.png', layout = 'wide', initial_sidebar_state='auto')
st.title('Weather Prediction')

#Setting Style on Streamlit
with open('./css/style.css') as f:
    st.markdown (f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Loading Model from Pickle
model = pickle.load(open('savemodel.pkl', 'rb'))

#Defining Function for Break statement
def br(n):
    st.markdown('<br>'*n, unsafe_allow_html=True)


#Upload the csv file
file = st.file_uploader('Upload CSV', type=['csv'])
if file is not None:
    df = pd.read_csv(file)
    df.columns = ['datetime', 'pressure', 'temperature', 'humidity', 'wind_speed', 'wind_direction']
    df = df[['datetime', 'humidity', 'pressure', 'temperature', 'wind_direction', 'wind_speed']]
    st.header('Dataset')
    br(1)
    j1,j2,j3 = st.columns([1,3,1])
    with j2:
        st.write(df)
    br(2)
    df.fillna(df.median(), inplace=True)
    df1 = df.copy(deep=True)
    #Incorporating the year, month, day and hour into dataset for diversity
    df1['datetime'] = pd.DatetimeIndex(df.datetime)
    df1['date'] = df1.datetime.dt.date
    df1['year'] = df1.datetime.dt.year
    df1['month'] = df1.datetime.dt.month
    df1['day'] = df1.datetime.dt.day
    df1['hour'] = df1.datetime.dt.hour
    #Averaging the original feature set according to date
    df1['avg_humidity'] = df1.groupby('date')['humidity'].transform('mean')
    df1['avg_pressure'] = df1.groupby('date')['pressure'].transform('mean')
    df1['avg_temperature'] = df1.groupby('date')['temperature'].transform('mean')
    df1['avg_wind_direction'] = df1.groupby('date')['wind_direction'].transform('mean')
    df1['avg_wind_speed'] = df1.groupby('date')['wind_speed'].transform('mean')
    #Dropping unwanted columns
    df1 = df1.drop(['datetime', 'date'], axis=1).reset_index().drop('index', axis=1)
    #Splitting Page into columns
    k1, k2, k3 = st.columns(3)
    with k2:
        pred = st.button('Predict')
    #Predicting the weather
    if pred:
        df['Predicted Weather'] = model.predict(df1)
        st.markdown('## Dataset After Prediction', unsafe_allow_html=True)
        br(2)
        st.write(df)
        br(3)
        fig = px.pie(df,names='Predicted Weather', values='humidity')
        fig.update_traces(textposition='inside')
        st.header('Pie Chart')
        st.plotly_chart(fig)
    