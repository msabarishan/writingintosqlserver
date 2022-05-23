import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import psycopg2
import postgreconnect
from altair import datum

#Define a sql to fetch data from CARS table (PostgreSQL table hosted on Heroku)
sql='Select * from cars;'

#postgreconnect.runquery function is called by passing on the sql. The function runquery returns the data from the CARS table.

#The returned data is converted into a DataFrame.
cars=pd.DataFrame(postgreconnect.runquery(sql))

#The DataFrame lacked columns, hence they were added. 9 Columns. 
cars.columns=['Name','Miles_Per_Gallon','Cylinders','Displacement','Horsepower','Weight_In_Lbs','Acceleration','Year','Origin']
cars['Year']=(pd.to_datetime(cars['Year'])).dt.year

# Identify the list of unique cars by Origin
CarsbyOrigin=cars[['Origin']]

#Identify the list of unique cars by Year
CarsbyYear=cars[['Year']]

#Maximum and Minimum Acceleration
maxacceleration=cars['Acceleration'].max()
minacceleration=cars['Acceleration'].min()

st.set_page_config(
                     layout="wide",
                     initial_sidebar_state="expanded",
                     menu_items={
                                 'About': "# This is an *extremely* cool app!"
                                }
                 )


st.subheader("Cars Data")
chart1=alt.Chart(cars).mark_point().encode(
    x='Miles_Per_Gallon:Q',
    y='Horsepower:Q',
    color='Cylinders'
).configure_legend(
                   titleFontSize=14,
                   labelFontSize=10
                   ).interactive()


st.altair_chart(chart1,use_container_width=True)

b=st.sidebar.multiselect('Pick one or more Country of Manufacturing',sorted(CarsbyOrigin['Origin'].unique()))

if b==[] :
    st.subheader('Waiting for a Country to be Picked...')
else:
    st.subheader('By Country')
    chart2=alt.Chart(cars).mark_point().encode(
                                          x='Miles_Per_Gallon:Q',
                                          y='Horsepower:Q',
                                          color='Origin'
                                          ).transform_filter (
                                                             alt.FieldOneOfPredicate(field='Origin',oneOf=b)                                                                    
                                                             ).configure_legend(
                                                                                titleFontSize=14,
                                                                                labelFontSize=10
                                                                                ) .interactive()

    st.altair_chart(chart2,use_container_width=True)

c=st.sidebar.multiselect('Pick one or more Vintage Year from this List',sorted(CarsbyYear['Year'].unique()))

if c==[]:
    st.subheader('Waiting for a Vintage Year to be Picked..')
else:
    st.subheader('By Vintage Year')
    chart3=alt.Chart(cars).mark_point().encode(
                                          x='Miles_Per_Gallon:Q',
                                          y='Horsepower:Q',
                                          color='Year:O'
                                          ).transform_filter (
                                                              alt.FieldOneOfPredicate(field='Year',oneOf=c)                                                                     
                                                             ).configure_legend(
                                                                                titleFontSize=14,
                                                                                labelFontSize=10
                                                                                ) .interactive()


    st.altair_chart(chart3,use_container_width=True)

d=st.sidebar.slider('Acceleration Greater than',min_value=minacceleration.item(),max_value=maxacceleration.item())
st.subheader('By Acceleration')
chart4=alt.Chart(cars).mark_point().encode(
                                          x='Miles_Per_Gallon:Q',
                                          y='Horsepower:Q',
                                          color='Acceleration'
                                          ).transform_filter (
                                                              alt.FieldGTPredicate(field='Acceleration',gt=d)                                                                      
                                                             ).configure_legend(
                                                                                titleFontSize=14,
                                                                                labelFontSize=10
                                                                                ) .interactive()

st.altair_chart(chart4,use_container_width=True)
