import mysql.connector
import csv

# Database Connection
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root'
)
cursor = connection.cursor()
query2 = """
         SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA 
         WHERE SCHEMA_NAME = 'alcohol';
         """
cursor.execute(query2)
fetch = cursor.fetchall()
if fetch == []:
    query1 = """
            CREATE DATABASE alcohol;
            """
    cursor.execute(query1)
fetch1 = cursor.fetchall()
if fetch1 != []:

    query = """ 
            CREATE TABLE alcohol.alcohol_info(
                id INT AUTO_INCREMENT PRIMARY KEY,
                country VARCHAR(30),
                beer INT,
                spirit INT,
                wine INT,
                total DOUBLE
                );
            """
    cursor.execute(query)

# Extract data from a csv file
with open ('drinks.csv') as file:
    csv_reader = csv.DictReader(file)
    # Transform data
    for data in csv_reader:
        country = data["country"]
        beer = data["beer_servings"]
        spirit = data["spirit_servings"]
        wine = data["wine_servings"]
        total = data["total_litres_of_pure_alcohol"] 
        load = (country, int(beer), int(spirit), int(wine), float(total))

        # Load data into database
        query3 = """
                INSERT INTO alcohol.alcohol_info(country,beer,spirit,wine,total)
                VALUES(%s,%s,%s,%s,%s);
                 """         
        cursor.execute(query3,load)
        connection.commit()
