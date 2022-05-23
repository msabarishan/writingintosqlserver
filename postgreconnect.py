import psycopg2

def runquery(sql):
    try:
        #Connect to the heroku postgresql database
        connection=psycopg2.connect(user="gpwvcgfprcaaji",
                                password="abf0e72c574eebd3810c44df8d690a1398dc1e551ff6ee306295825801cb39fe",
                                host="ec2-34-207-12-160.compute-1.amazonaws.com",
                                database="d5fmmj82e013ta")

        #Create a cursor to perform database operations
        cursor=connection.cursor()

        #Use the cursor to run an SQL. The exact SQL is defined in another python script.
        cursor.execute(sql)

        #Fetch all records from the table using the SQL. 

        record = cursor.fetchall()

        #Return the fetched records to the calling program.
        return(record)
    except:
        print("Error while fetching data")
    finally:
        #Close Cursor and Database Connection
        cursor.close()
        connection.close()
        
