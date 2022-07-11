import psycopg2
import psycopg2.extras
import pandas as pd
import streamlit as st
import altair as alt

st.header("Employee Data Base")

# Read Excel File
option = st.selectbox('Select the  requirement?',('Sample_file','Add_Employee','Add_Branch','Add_Supplier','Add_Client','Delete', 'Display','Reset','Create_table'))
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
                          cur.execute('DELETE FROM employee')
                          cur.execute('DELETE FROM client')
                          cur.execute('DELETE FROM works_with')
                          cur.execute('DELETE FROM branch_supplier')
                          cur.execute('DELETE FROM branch')
                          st.write('All data Deleted Successfully')
                           
# Create new table
                  elif(option=='Create_table'):
                          create_script = ''' CREATE TABLE employee (
                                           emp_id INT PRIMARY KEY,
                                           first_name VARCHAR(40),
                                           last_name VARCHAR(40),
                                           sex VARCHAR(1),
                                           salary INT,
                                           super_id INT,
                                           branch_id INT,
                                           age INT
                                         ) '''        
                          cur.execute(create_script)
                          create_script1 = ''' CREATE TABLE branch (
                                            branch_id INT PRIMARY KEY,
                                            branch_name VARCHAR(40),
                                            mgr_id INT,
                                            mgr_start_date DATE,
                                            FOREIGN KEY(mgr_id) REFERENCES employee(emp_id) ON DELETE SET NULL
                                          ) '''        
                          cur.execute(create_script1)
                          create_script2 = ''' ALTER TABLE employee
                                          ADD FOREIGN KEY(branch_id)
                                          REFERENCES branch(branch_id)
                                          ON DELETE SET NULL '''        
                          cur.execute(create_script2)
                          create_script3 = ''' 
                                          ALTER TABLE employee
                                          ADD FOREIGN KEY(super_id)
                                          REFERENCES employee(emp_id)
                                          ON DELETE SET NULL '''        
                          cur.execute(create_script3)
                          create_script4 = ''' CREATE TABLE client (
                                            client_id INT PRIMARY KEY,
                                            client_name VARCHAR(40),
                                            branch_id INT,
                                            FOREIGN KEY(branch_id) REFERENCES branch(branch_id) ON DELETE SET NULL
                                          ) '''        
                          cur.execute(create_script4)
                          create_script5 = ''' CREATE TABLE works_with (
                                            emp_id INT,
                                            client_id INT,
                                            total_sales INT,
                                            PRIMARY KEY(emp_id, client_id),
                                            FOREIGN KEY(emp_id) REFERENCES employee(emp_id) ON DELETE CASCADE,
                                            FOREIGN KEY(client_id) REFERENCES client(client_id) ON DELETE CASCADE
                                          )) '''        
                          cur.execute(create_script5)
                          create_script6 = ''' CREATE TABLE branch_supplier (
                                            branch_id INT,
                                            supplier_name VARCHAR(40),
                                            supply_type VARCHAR(40),
                                            PRIMARY KEY(branch_id, supplier_name),
                                            FOREIGN KEY(branch_id) REFERENCES branch(branch_id) ON DELETE CASCADE
                                          ) '''        
                          cur.execute(create_script6)
                          st.write('Reset Successfully')
# List created from input data are passed
                  elif(option=='Add_Employee'):     
                       excel_ip= st.file_uploader("Choose a CSV file. Select Sample_file option for downloading sample format file")
                       if excel_ip is not None:
                            df = pd.read_csv(excel_ip)
                            df = df.fillna(psycopg2.extensions.AsIs('NULL'))
                       insert_values = df.values.tolist()
                       insert_script  = 'INSERT INTO employee (emp_id,first_name,last_name,sex,salary,super_id,branch_id) VALUES ( %s, %s, %s, %s, %s, %s, %s)'
                       for record in insert_values:
                                  cur.execute(insert_script, record)
                       st.write("Added Successfully")
                  
                  elif(option=='Add_Branch'):     
                       excel_ip= st.file_uploader("Choose a CSV file. Select Sample_file option for downloading sample format file")
                       if excel_ip is not None:
                            df = pd.read_csv(excel_ip)
                            df = df.fillna(psycopg2.extensions.AsIs('NULL'))
                       insert_values = df.values.tolist()
                       insert_script  = 'insert into branch (branch_id,branch_name,mgr_id,mgr_start_date) values ( %s, %s, %s, %s)'
                       for record in insert_values:
                                  cur.execute(insert_script, record)
                       st.write("Added Successfully")
                  
                  elif(option=='Add_Client'):     
                       excel_ip= st.file_uploader("Choose a CSV file. Select Sample_file option for downloading sample format file")
                       if excel_ip is not None:
                            df = pd.read_csv(excel_ip)
                            df = df.fillna(psycopg2.extensions.AsIs('NULL'))
                       insert_values = df.values.tolist()
                       insert_script  = 'INSERT INTO client VALUES( %s, %s, %s)'
                       for record in insert_values:
                                  cur.execute(insert_script, record)
                       st.write("Added Successfully")
                    
                  elif(option=='Add_Supplier'):     
                       excel_ip= st.file_uploader("Choose a CSV file. Select Sample_file option for downloading sample format file")
                       if excel_ip is not None:
                            df = pd.read_csv(excel_ip)
                            df = df.fillna(psycopg2.extensions.AsIs('NULL'))
                       insert_values = df.values.tolist()
                       insert_script  = 'INSERT INTO branch_supplier VALUES( %s, %s, %s)'
                       for record in insert_values:
                                  cur.execute(insert_script, record)
                       st.write("Added Successfully")
                    
                  elif(option=='Add_work_details'):     
                       excel_ip= st.file_uploader("Choose a CSV file. Select Sample_file option for downloading sample format file")
                       if excel_ip is not None:
                            df = pd.read_csv(excel_ip)
                            df = df.fillna(psycopg2.extensions.AsIs('NULL'))
                       insert_values = df.values.tolist()
                       insert_script  = 'INSERT INTO branch_supplier VALUES( %s, %s, %s)'
                       for record in insert_values:
                                  cur.execute(insert_script, record)
                       st.write("Added Successfully")
               
                  elif(option=='Sample_file'):  
                       st.write("Sample_file_download")
                       sample=pd.read_csv('employees.csv')
                       sample1=pd.read_csv('branch.csv')
                       sample2=pd.read_csv('supplier.csv')
                       sample3=pd.read_csv('client.csv')
                       sample4=pd.read_csv('works_with.csv')
                       
                       def convert_df(machine):
                              return machine.to_csv(index=False).encode('utf-8')

                       sample_file = convert_df(sample)
                       sample_file1 = convert_df(sample1)
                       sample_file2 = convert_df(sample2)
                       sample_file3 = convert_df(sample3)
                       sample_file4 = convert_df(sample4)
                       
                       st.download_button("Press to Download Employee Sample File",sample_file,"employee.csv","text/csv",key='download-csv')
                       st.download_button("Press to Download Branch Sample File",sample_file1,"branch.csv","text/csv",key='download-csv')
                       st.download_button("Press to Download Supplier Sample File",sample_file2,"supplier.csv","text/csv",key='download-csv')
                       st.download_button("Press to Download Client Sample File",sample_file3,"client.csv","text/csv",key='download-csv')
                       st.download_button("Press to Download Works_with Sample File",sample_file4,"clientemployee.csv","text/csv",key='download-csv')
                    
                  elif(option=='Delete'):
                       option3 = st.selectbox('Select the data for deletion',('Employee','Branch','Supplier','Client','Workrelation'))
                       if(option3=='Employee'):
                             number = st.number_input('Enter the EMP ID: ',min_value=1, max_value=1000,step=1)
                             if st.button('Click to delete'):
                               delete_script = 'DELETE FROM employee WHERE emp_id = %s'
                               delete_record = (f'{number}',)
                               cur.execute(delete_script, delete_record)
                               st.write("Deleted Successfully")
                       elif(option3=='Branch'):
                             number = st.number_input('Enter the BRANCH ID: ',min_value=1, max_value=1000,step=1)
                             if st.button('Click to delete'):
                               delete_script = 'DELETE FROM branch WHERE branch_id = %s'
                               delete_record = (f'{number}',)
                               cur.execute(delete_script, delete_record)
                               st.write("Deleted Successfully")
                       elif(option3=='Client'):
                             number = st.number_input('Enter the ID: ',min_value=1, max_value=1000,step=1)
                             if st.button('Click to Delete'):
                               delete_script = 'DELETE FROM CLIENT WHERE client_id = %s'
                               delete_record = (f'{number}',)
                               cur.execute(delete_script, delete_record)
                               st.write("Deleted Successfully")
                       elif(option3=='Supplier'):
                             number1 = st.number_input('Enter the Branch ID: ',min_value=1, max_value=1000,step=1)
                             supp_name = st.text_input('Enter_supplier_name')
                             st.write(supp_name)
                             if st.button('Click to Delete'):
                               st.write("Works")
                               delete_script = 'DELETE FROM branch_supplier WHERE branch_id = %s and supplier_name= %s'
                               delete_record = (f'{number1}',supp_name,)
                               cur.execute(delete_script, delete_record)
                               st.write("Deleted Successfully")
                       else:
                             number = st.number_input('Enter the EMP ID: ',min_value=1, max_value=1000,step=1)
                             number1 = st.number_input('Enter the CLIENT ID: ',min_value=1, max_value=1000,step=1)
                          
                             if st.button('Click to delete'):
                               delete_script = 'DELETE FROM works_with WHERE emp_id = %s  AND client_id = %s'
                               delete_record = (f'{number}',f'{number1}',)
                              
                               cur.execute(delete_script, delete_record)
                               st.write("Deleted Successfully")

                 #update_script = 'UPDATE employees SET salary = salary + (salary * 0.5)'
                 #cur.execute(update_script)
                 # Deleting records
                       
                  else:
                     sub_option = st.selectbox('Select the data need to displayed',('Employee','Branch','Supplier','Client','Works_With'))
                     if(sub_option=='Employee'):
                          cur.execute('SELECT * FROM EMPLOYEE    ')
                          record = cur.fetchall()
                          emp_data=pd.DataFrame(record)
                          emp_data.columns=['ID','First_Name','Last_name','Sex','Salary','Sup_id','Branch_id']
                          st.subheader('Current Employee Details')
                          hide_table_row_index = """
                                 <style>
                                      tbody th {display:none}
                                      .blank {display:none}
                                 </style> """
                         
                     elif(sub_option=='Branch'):
                          cur.execute('SELECT * FROM BRANCH    ')
                          record = cur.fetchall()
                          emp_data=pd.DataFrame(record)
                          emp_data.columns=['branch_id','branch_name','mgr_id','mgr_start_date']
                          st.subheader('Current Branch Details')
                          hide_table_row_index = """
                                 <style>
                                      tbody th {display:none}
                                      .blank {display:none}
                                 </style> """
                         
                     elif(sub_option=='Client'):
                          cur.execute('SELECT * FROM CLIENT    ')
                          record = cur.fetchall()
                          emp_data=pd.DataFrame(record)
                          emp_data.columns=['client_id','client_name','branch_id']
                          st.subheader('Current Client Details')
                          hide_table_row_index = """
                                 <style>
                                      tbody th {display:none}
                                      .blank {display:none}
                                 </style> """
                          
                     elif(sub_option=='Supplier'):
                          cur.execute('SELECT * FROM BRANCH_SUPPLIER    ')
                          record = cur.fetchall()
                          emp_data=pd.DataFrame(record)
                          emp_data.columns=['branch_id','supplier_name','supplier_type']
                          st.subheader('Current Supplier Details')
                          hide_table_row_index = """
                                 <style>
                                      tbody th {display:none}
                                      .blank {display:none}
                                 </style> """
                     elif(sub_option=='Works_With'):
                          cur.execute('SELECT * FROM works_with    ')
                          record = cur.fetchall()
                          emp_data=pd.DataFrame(record)
                          emp_data.columns=['emp_id','client_id','total_sales']
                          st.subheader('Current Client & Employee Details')
                          hide_table_row_index = """
                                 <style>
                                      tbody th {display:none}
                                      .blank {display:none}
                                 </style> """
# Inject CSS with Markdown
                     st.markdown(hide_table_row_index, unsafe_allow_html=True)
                     st.table(emp_data)
                     st.write("If there is no data, display will be empty")
                     st.subheader('Sales')
                              
                     chart1=alt.Chart(emp_data).mark_bar().encode(                             
                     alt.X('emp_id', title='Employ ID'),
                     alt.Y('total_sales', title='Sales in Rs')
                     )
                     st.altair_chart(chart1,use_container_width=True)
                         
                     chart2=alt.Chart(emp_data).mark_bar().encode(                             
                     alt.X('client_id', title='Employ ID'),
                     alt.Y('total_sales', title='Sales in Rs')
                     )
                     st.altair_chart(chart2,use_container_width=True)
                    
     except Exception as error:
         print(error)

     finally:
         if conn is not None:
            conn.close()
except:
    pass
