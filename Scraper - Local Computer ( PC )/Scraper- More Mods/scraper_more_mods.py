import requests
from bs4 import BeautifulSoup
from discord_webhooks import DiscordWebhooks
import discord_webhook
import time
import datetime
from pytz import timezone

#Put your discord webhook url here.
# IMPORTANT : If you're hosting on pythonanywhere, use discordapp.com instead of discord.com in the URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/787733891133079582/I4fsSallw0i8v4yzlER5ZlaixBluIWD5yriWQD2hsQhOndx35fpkgWTkWU606F-4jkFU'

#url= 'https://www.amazon.in/Sony-Full-Frame-Mirrorless-Interchangeable-Lens-Camera/dp/B07B43WPVK/ref=sr_1_2?dchild=1&keywords=sony+a7&qid=1607783566&sr=8-2'

headers= {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
	
number_of_products= int(input("Enter number of products- "))
while number_of_products>10:
	print("Maximum number of products you can enter is 10")
	number_of_products= int(input("Re-enter number of products- "))

url_list= [0,0,0,0,0,0,0,0,0,0]
title= [0,0,0,0,0,0,0,0,0,0]
converted_price= [0,0,0,0,0,0,0,0,0,0]
price_we_want= [0,0,0,0,0,0,0,0,0,0]

# for loop to take user input of product url and price the user wants for each product
for i in range(0, number_of_products):

	count= str(i+1)
	num= str(number_of_products)

	url_list[i]= str(input("Enter url of product ["+count+"/"+num+"] :- "))

	page= requests.get(url_list[i], headers=headers)

	soup= BeautifulSoup(page.content, 'html.parser')

	title[i]= soup.find(id="productTitle").get_text()
	price= soup.find(id="priceblock_ourprice").get_text()

	print(title[i].strip())
	converted_price[i]= price[2:13]
	print("Current price- Rs.",converted_price[i])

	price_we_want[i]= input("Enter price you want- ")
	print()

def send_message():

	for j in range(0, number_of_products):

		current_time = datetime.datetime.now(timezone('Asia/Kolkata'))
		current_time = current_time.strftime("%b %d, %Y - %H:%M:%S")
		
		if (converted_price[j] < price_we_want[j])==True:

			# To send message via discord webhook
			#WEBHOOK_URL = webhook_url

			webhook = DiscordWebhooks(WEBHOOK_URL)

			webhook.set_content(title= 'Price Drop :heart:',
			                    description= title[j])

			# Attaches a footer
			webhook.set_footer(text='Report for %s' % (current_time))

			# Appends a field
			#webhook.add_field(name='Product Title', value=title[j])
			webhook.add_field(name='Dropped Price', value="Rs. "+converted_price[j])
			webhook.add_field(name='Price you wanted', value="Rs. "+price_we_want[j])

			webhook.send()

			#print("The price is below" ,price_we_want, "and has been reduced to", converted_price)

			print("Sent message to discord")

			time.sleep(3)
		
while True:
	send_message()
	time.sleep(600) # currently this is 10 minutes but make this every 12 hour

# this program will run 24/7