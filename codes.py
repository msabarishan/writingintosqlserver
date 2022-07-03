import psycopg2
import psycopg2.extras
import pandas as pd
import streamlit as st

# Read Excel File
option = st.selectbox('Select the  requirement?',(None,'Add', 'Delete', 'Display','Reset'))
st.write('You selected:', option)
try:
     
     st.subheader('Upload Input Files')
     excel_ip= st.file_uploader("Choose a Machine Priority CSV file")
     if excel_ip is not None:
                df = pd.read_csv(excel_ip) #mp-machine priority data frame
     insert_values = df.values.tolist()

# Use your credentials
     hostname = 'ec2-34-207-12-160.compute-1.amazonaws.com'
     database = 'd5fmmj82e013ta'
     username = 'gpwvcgfprcaaji'
     pwd = 'abf0e72c574eebd3810c44df8d690a1398dc1e551ff6ee306295825801cb39fe'
     port_id = 5432
     conn = None

     try:
         with psycopg2.connect(
                     host = hostname,
                     dbname = database,
                     user = username,
                     password = pwd,
                     port = port_id) as conn:

             with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    
                  if(option=='Reset'):
# Dropping existing table
                       cur.execute('DROP TABLE IF EXISTS employees')
# Create new table
                       create_script = ''' CREATE TABLE IF NOT EXISTS employees (
                                          id      int PRIMARY KEY,
                                          name    varchar(40) NOT NULL,
                                          salary  int,
                                          dept_id varchar(30)) '''
                       cur.execute(create_script)
# List created from input data are passed
                  if(option=='Add'):     
                       insert_script  = 'INSERT INTO employees (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'
                       for record in insert_values:
                                  cur.execute(insert_script, record)
# For Updating salary with 50% hike
                  if(option=='Delete'):
                       number = st.number_input('Enter the ID: ',min_value=1, max_value=100,step=1)
                 #update_script = 'UPDATE employees SET salary = salary + (salary * 0.5)'
                 #cur.execute(update_script)
                 # Deleting records
                       delete_script = 'DELETE FROM employees WHERE ID = %s'
                       cur.execute(delete_script, number)
                  if(option=='Display'):
                     cur.execute('SELECT * FROM EMPLOYEES')
                     record = cur.fetchall()
                     emp_data=pd.DataFrame(record)
                     emp_data.columns=['ID','Name','Salary','Dept Id']
                     st.subheader('Upload data')
                     hide_table_row_index = """
                            <style>
                                 tbody th {display:none}
                                 .blank {display:none}
                            </style> """

# Inject CSS with Markdown
                     st.markdown(hide_table_row_index, unsafe_allow_html=True)

                     st.table(emp_data)
               
                 
     except Exception as error:
         print(error)

     finally:
         if conn is not None:
            conn.close()
except:
    pass
