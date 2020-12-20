import requests
from bs4 import BeautifulSoup
from discord_webhooks import DiscordWebhooks
import discord_webhook
import time
import datetime
from pytz import timezone
from keep_running import keep_running

# IMPORTANT : If the webhook url is not working or any error related to it is coming, try using discordapp.com instead of discord.com in the URL
#Put your discord webhook url here.
WEBHOOK_URL = ' '

# Search for my user agent on google and copy the result and paste it over here.
headers= {"User-Agent": ' '}
	
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
			webhook = DiscordWebhooks(WEBHOOK_URL)

			webhook.set_content(title= 'Price Drop :heart:',
			                    description= title[j])

			# Attaches a footer
			webhook.set_footer(text='Report for %s' % (current_time))

			# Appends a field
			webhook.add_field(name='Dropped Price', value="Rs. "+converted_price[j])
			webhook.add_field(name='Price you wanted', value="Rs. "+price_we_want[j])
			webhook.add_field(name='URL', value= url_list[j])

			webhook.send()

			print("Sent message to discord")

			time.sleep(3)


		else:

			print("Price has not dropped.")

			# To send message via discord webhook
			webhook = DiscordWebhooks(WEBHOOK_URL)

			webhook.set_content(title= 'No drop in price :cry:',
			                    description= title[j])

			# Attaches a footer
			webhook.set_footer(text='Report for %s' % (current_time))

			# Appends a field
			webhook.add_field(name='Dropped Price', value="Rs. "+converted_price[j])
			webhook.add_field(name='Price you wanted', value="Rs. "+price_we_want[j])
			webhook.add_field(name='URL', value= url_list[j])

			webhook.send()

			print("Sent message to discord")

			time.sleep(3)

		
keep_running()

while True:
	send_message()
	time.sleep(21600) # will send a message every 6 hours or 4 times a day
