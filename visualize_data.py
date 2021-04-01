import mysql.connector
import pandas as pd
from vincent.colors import brews

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root' 
)
cursor = connection.cursor()
query = """
        SELECT beer,spirit,wine FROM alcohol.alcohol_info
        """
cursor.execute(query)
fetch = cursor.fetchall()
beerqu = 0
spiritqu = 0
winequ = 0
qu = {}
for data in fetch:
    beerqu += data[0]
    spiritqu += data[1]
    winequ += data[2]
qu['b'] = beerqu
qu['s'] = spiritqu
qu['w'] = winequ
df = pd.DataFrame([qu], index=['Qu'])
excel_file = 'alcohol_visualize.xlsx'
sheet_name = 'Sheet1'

writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
df.to_excel(writer, sheet_name=sheet_name)
workbook = writer.book
worksheet = writer.sheets[sheet_name]

# Create a chart object.
chart = workbook.add_chart({'type': 'pie'})

# Configure the chart from the dataframe data. Configuring the segment
# colours is optional. Without the 'points' option you will get Excel's
# default colours.
chart.add_series({
    'categories': '=Sheet1!B1:D1',
    'values':     '=Sheet1!B2:D2',
    'points': [
        {'fill': {'color': brews['Set1'][0]}},
        {'fill': {'color': brews['Set1'][1]}},
        {'fill': {'color': brews['Set1'][2]}},
    ],
})

# Insert the chart into the worksheet.
worksheet.insert_chart('B4', chart)

# Close the Pandas Excel writer and output the Excel file.
writer.save()

   
    


