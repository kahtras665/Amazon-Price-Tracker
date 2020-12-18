import requests
from bs4 import BeautifulSoup
from discord_webhooks import DiscordWebhooks
import discord_webhook
import time
import datetime
from pytz import timezone

#Put your discord webhook url here.
# If you're hosting on cloud and any kind of error occurs, try using discordapp.com instead of discord.com in the URL
WEBHOOK_URL = 'Enter your discord webhook url'

url= 'https://www.amazon.in/Sony-Full-Frame-Mirrorless-Interchangeable-Lens-Camera/dp/B07B43WPVK/ref=sr_1_2?dchild=1&keywords=sony+a7&qid=1607783566&sr=8-2'

# search for my user agent on google and paste it there below.
headers= {"User-Agent": '			'}
	

def check_price():

	current_time = datetime.datetime.now(timezone('Asia/Kolkata'))
	current_time = current_time.strftime("%b %d, %Y - %H:%M:%S")

	page= requests.get(url, headers=headers)

	soup= BeautifulSoup(page.content, 'html.parser')

	title= soup.find(id="productTitle").get_text()
	price= soup.find(id="priceblock_ourprice").get_text()
	converted_price= price[2:13]
	price_we_want= "1,60,000.00"
		
	print(title.strip())
	
	if (converted_price < price_we_want)==True:

		# To send message via discord webhook

		webhook = DiscordWebhooks(WEBHOOK_URL)

		webhook.set_content(title='Price Drop! :heart:',
		                    description= title)

		# Attaches a footer
		webhook.set_footer(text='Report for %s' % (current_time))

		webhook.add_field(name='Dropped price', value="Rs. "+converted_price)
		webhook.add_field(name='Price you wanted', value="Rs. "+price_we_want)

		webhook.send()

		print("The price is below" ,price_we_want, "and has been reduced to", converted_price)

		print("Sent message to discord")
		
while True:
	check_price()
	time.sleep(20)