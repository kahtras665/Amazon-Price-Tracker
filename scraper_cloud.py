import requests
from bs4 import BeautifulSoup
from discord_webhooks import DiscordWebhooks
import discord_webhook
import time
import datetime
from pytz import timezone

#Put your discord webhook url here.
# If you're hosting on cloud and any kind of error occurs, try using discordapp.com instead of discord.com in the URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/787733891133079582/I4fsSallw0i8v4yzlER5ZlaixBluIWD5yriWQD2hsQhOndx35fpkgWTkWU606F-4jkFU'

url= 'https://www.amazon.in/dp/B07VTWX8MN/ref=twister_B083ZKN5JW?_encoding=UTF8&psc=1'

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
	price_we_want= "3,900.00"
		
	print(title.strip())

	# To send message via discord webhook	
	if (converted_price < price_we_want)==True:

		webhook = DiscordWebhooks(WEBHOOK_URL)

		webhook.set_content(title='Price Drop! :heart:',
		                    description= title)

		# Attaches a footer
		webhook.set_footer(text='Report for %s' % (current_time))

		#Appends a field
		webhook.add_field(name='Dropped price', value="Rs. "+converted_price)
		webhook.add_field(name='Price you wanted', value="Rs. "+price_we_want)
		webhook.add_field(name='Product URL', value=url)

		webhook.send()

		print("Sent message to discord")

	else:

		print("Price has not dropped.")

		webhook = DiscordWebhooks(WEBHOOK_URL)

		# you can use this to add emoticon--> :cry:
		webhook.set_content(title="No drop in price!",
							description= title)

		# Attaches a footer
		webhook.set_footer(text='Report for %s' % (current_time))

		#Appends a field
		webhook.add_field(name='Current price', value="Rs. "+converted_price)
		webhook.add_field(name='Price you wanted', value="Rs. "+price_we_want)
		webhook.add_field(name='Product URL', value=url)

		webhook.send()

		print("Sent message to discord")
		
check_price()