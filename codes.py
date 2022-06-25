import psycopg2
import psycopg2.extras
import pandas as pd

# Read Excel File
df=pd.read_csv('employees.csv')
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
            insert_script  = 'INSERT INTO employees (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'
            for record in insert_values:
                cur.execute(insert_script, record)
# For Updating salary with 50% hike
            update_script = 'UPDATE employees SET salary = salary + (salary * 0.5)'
            cur.execute(update_script)
# Deleting records
            delete_script = 'DELETE FROM employees WHERE name = %s'
            delete_record = ('James',)
            cur.execute(delete_script, delete_record)

            cur.execute('SELECT * FROM EMPLOYEES')
            for record in cur.fetchall():
                print(record['name'], record['salary'])
except Exception as error:
    print(error)
finally:
    if conn is not None:
      conn.close()
