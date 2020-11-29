from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('tbody')
tr = table.find_all('tr')
temp = [] #initiating a tuple

#insert the scrapping process here
for i in range(1, len(tr)):

    row = table.find_all('tr')[i]
    
    #tanggal
    date = row.find_all('td')[0].text
    date = date.strip()
    
    #harga harian
    harga = row.find_all('td')[2].text
    harga = harga.strip()
    
    temp.append((date, harga))    

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('date','harga'))

#insert data wrangling here
df['harga'] = df['harga'].str.replace("IDR","")
df['harga'] = df['harga'].str.replace(",","")
df['harga'] = df['harga'].astype('float64')
df['date'] = df['date'].astype('datetime64') 

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["harga"].mean()}'

	# generate plot
	ax = df.plot(x='date', y='harga', figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
