import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import psycopg2
import postgreconnect
from altair import datum

#Define a sql to fetch data from CARS table (PostgreSQL table hosted on Heroku)
sql='INSERT INTO COMPANY VALUES(13,'SAFARAZ',27,'NORTH DAKOTA',3000);'
company_data='Select * from company;'
#postgreconnect.runquery function is called by passing on the sql. The function runquery returns the data from the CARS table.
postgreconnect.runquery(sql)
#The returned data is converted into a DataFrame.
sql_data=pd.DataFrame(postgreconnect.runquery(company_data))

st.table(sql_data)
