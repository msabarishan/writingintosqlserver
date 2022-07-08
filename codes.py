import psycopg2
import psycopg2.extras
import pandas as pd
import streamlit as st

st.header("Employee Data Base")

# Read Excel File
option = st.selectbox('Select the  requirement?',('Sample_file','Add', 'Delete', 'Display','Reset'))
st.write('You selected:', option)
try:
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
                    if st.button('Click to Reset'):
                         
# Dropping existing table
                       cur.execute('DROP TABLE IF EXISTS employees')
# Create new table
                       create_script = ''' CREATE TABLE IF NOT EXISTS employees (
                                          id      int PRIMARY KEY,
                                          name    varchar(40) NOT NULL,
                                          salary  int,
                                          dept_id varchar(30)) '''
                       cur.execute(create_script)
                       st.write('Reset Successfully')
# List created from input data are passed
                  elif(option=='Add'):     
                       excel_ip= st.file_uploader("Choose a CSV file. Select Sample_file option for downloading sample format file")
                       if excel_ip is not None:
                            df = pd.read_csv(excel_ip)
                       insert_values = df.values.tolist()
                       insert_script  = 'INSERT INTO employees (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'
                       for record in insert_values:
                                  cur.execute(insert_script, record)
                       st.write("Added Successfully")
                    
                  elif(option=='Sample_file'):  
                       st.write("Sample_file_download")
                       sample=pd.read_csv('employees.csv')
                       def convert_df(machine):
                              return machine.to_csv(index=False).encode('utf-8')

                       sample_file = convert_df(sample)
                       st.download_button(
                              "Press to Download machine Priority file",
                              sample_file,
                              "sample_file.csv",
                              "text/csv",
                              key='download-csv'
                              )
                    
                  elif(option=='Delete'):
                       number = st.number_input('Enter the ID: ',min_value=1, max_value=100,step=1)
                       if st.button('Click to delete'):
                         
                         delete_script = 'DELETE FROM employees WHERE id = %s'
                         delete_record = (f'{number}',)
                         cur.execute(delete_script, delete_record)
                         st.write("Deleted Successfully")

                 #update_script = 'UPDATE employees SET salary = salary + (salary * 0.5)'
                 #cur.execute(update_script)
                 # Deleting records
                       
                  else:
                     cur.execute('SELECT * FROM EMPLOYEES')
                     record = cur.fetchall()
                     emp_data=pd.DataFrame(record)
                     emp_data.columns=['ID','Name','Salary','Dept Id']
                     st.subheader('Current Employee Details')
                     hide_table_row_index = """
                            <style>
                                 tbody th {display:none}
                                 .blank {display:none}
                            </style> """

# Inject CSS with Markdown
                     st.markdown(hide_table_row_index, unsafe_allow_html=True)

                     st.table(emp_data)
                     st.write("If there is no data, display will be empty")
               
                 
     except Exception as error:
         print(error)

     finally:
         if conn is not None:
            conn.close()
except:
    pass
