from dotenv import load_dotenv
import os
import requests
import random

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
