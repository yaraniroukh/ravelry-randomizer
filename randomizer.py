from dotenv import load_dotenv
import os
import requests
import random
import textwrap
from PIL import Image
import io

load_dotenv()

# API credentials are stored in the .env file. Generate your own at https://www.ravelry.com/pro/developer
API_USER = os.getenv("API_USER")
API_PASS = os.getenv("API_PASS")


######### Logic of the randomizer


def check_matches_exist(response):
    """Return true if matches are found (if response is non-empty)."""

    return [] != response.json()["patterns"]


def generate_pattern_ID(query_params):
    """Given a list of parameters, return a random pattern ID from the Ravelry website (or -100 if no matches)."""

    url = "https://api.ravelry.com/patterns/search.json"
    response = requests.get(url, params=query_params, auth=(API_USER, API_PASS))

    if not check_matches_exist(response):
        return -100
    
    all_patterns = response.json()["patterns"]
    page_count = response.json()["paginator"]["page_count"]

    if page_count > 2: # Choose a random page to take the pattern from.
        random_page = random.randint(1, page_count)
        query_params["page"] = random_page
        response = requests.get(url, params=query_params, auth=(API_USER, API_PASS))
        all_patterns = response.json()["patterns"]

    return random.choice(all_patterns)["id"]


######### Methods to get information about a generated pattern


def get_pattern(id):
    """Given a pattern ID, get the associated pattern."""
    
    url = f"https://api.ravelry.com/patterns/{id}.json"
    response = requests.get(url, auth=(API_USER, API_PASS))

    if response.status_code == 200:
        pattern = response.json()['pattern']
        return pattern
    
    else:
        return("Error: cannot find pattern")
    
def get_pattern_URL(pattern):
    """Given a pattern, get the associated pattern URL."""
    
    permalink = pattern['permalink']
    url = f"https://www.ravelry.com/patterns/library/{permalink}"
    return url

def get_pattern_author_URL(pattern):
    """Given a pattern, get the pattern author's URL."""
    
    permalink = pattern['pattern_author']['permalink']
    url = f"https://www.ravelry.com/designers/{permalink}"
    return url

def get_pattern_image(pattern):
    """Given a pattern, get the pattern's image."""

    images = pattern['photos']
    if images != []:
        image_url = pattern['photos'][0]['small2_url']
        response = requests.get(image_url, stream=True)
        response.raw.decode_content = True
        img = Image.open(response.raw)
        img = img.resize((320,320))
        bio = io.BytesIO()
        img.save(bio, format='PNG')
        return bio.getvalue()
    else:
        return None

def get_pattern_description(pattern):
    """Given a pattern, get a formatted version of the pattern's description."""

    description = pattern['notes']
    if description is not None: description = description.replace('\r', ' ').replace('\n', ' ')
    description_shortened = description[:320]
    if len(description) > 320: description_shortened = description_shortened + '...'
    if not description == "": 
        description = '"' + description + '"'
        return textwrap.fill(description_shortened, 39)
    else:
        return("No description found.")
    
def get_pattern_price(pattern):
    """Given a pattern, get a formatted version of the pattern's price."""

    if pattern['currency_symbol'] == None or pattern['price'] == None:
        return('Price unavailable')
    elif not pattern['free']:
        price = str(pattern['price'])
        return(str(pattern['currency_symbol']) + price)
    else:
        return('Free')
    
def get_pattern_languages(pattern):
    """Given a pattern, get a formatted list of all the languages the pattern is available in."""

    languages = ""
    for lan in pattern['languages'][:3]:
        languages = languages + ', ' + lan['name']
    if len(pattern['languages']) > 3:
        languages = languages + '...'
    languages = languages[2:]
    if languages == "": languages = "Unavailable"
    return('Languages: ' + languages)