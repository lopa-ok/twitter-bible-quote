import requests
from PIL import Image, ImageDraw, ImageFont
import tweepy
import os

# Twitter API credentials
CONSUMER_KEY = 'your_consumer_key'
CONSUMER_SECRET = 'your_consumer_secret'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

def fetch_daily_verse():
    response = requests.get('https://beta.ourmanna.com/api/v1/get/?format=json&order=daily')
    data = response.json()
    verse_text = data['verse']['details']['text']
    verse_reference = data['verse']['details']['reference']
    return f"{verse_text}\n\n- {verse_reference}"

def create_quote_image(quote, output_path):
    img = Image.new('RGB', (800, 800), color='white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', size=24)
    text_width, text_height = draw.textsize(quote, font=font)
    position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
    draw.text(position, quote, fill='black', font=font)
    img.save(output_path)

def post_to_twitter(image_path, status):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    api.update_with_media(image_path, status=status)

if __name__ == "__main__":
    quote = fetch_daily_verse()
    image_path = 'daily_verse.png'
    create_quote_image(quote, image_path)
    post_to_twitter(image_path, status='Daily Bible Quote')

    # Clean up
    os.remove(image_path)
