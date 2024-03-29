from dotenv import load_dotenv
import os
import requests
import random
from PIL import Image
import io
import helpers as hp
import api_exceptions as exc

load_dotenv()

# API credentials are stored in the .env file. Generate your own at https://www.ravelry.com/pro/developer
API_USER = os.getenv("API_USER")
API_PASS = os.getenv("API_PASS")


######### Methods retrieving pattern search parameters from the Ravelry website


def simplify(list):
    """Recursively retrieve all children from a given list and simplify to include only their names and permalinks."""

    simplified_list = []

    for cat in list:
        category = cat['name']
        permalink = cat.get('permalink', hp.slugify(category))
        if permalink in exc.exceptions_categories.keys(): permalink = exc.exceptions_categories[permalink]
        children = cat.get('children', [])
        if not len(children) == 0:
            simplified_list += [(category, permalink), simplify(children)]
        else:
            simplified_list.append((category, permalink))
    return simplified_list


def simplify_attributes(list):
    """Same as .simplify(), adapted to match irregularities in the pattern attributes list."""

    simplified_list = []

    for cat in list:
        category = cat['name']
        if category == "Age / Size / Fit": continue
        permalink = cat.get('permalink', hp.slugify(category))
        if permalink in exc.exceptions_attributes.keys(): permalink = exc.exceptions_attributes[permalink]
        children = cat.get('children', [])
        if children == []: children = cat.get('pattern_attributes', [])
        if not len(children) == 0:
            simplified_list += [(category, permalink), simplify_attributes(children)]
        else:
            simplified_list.append((category, permalink))
    return simplified_list


def simplify_fit(list):
    """Same as .simplify(), adapted to match irregularities in the pattern age/size/fit attributes list."""

    simplified_list = []

    for cat in list:
        category = cat['name']
        permalink = cat.get('permalink', hp.slugify(category))
        if permalink in exc.exceptions_fit.keys(): permalink = exc.exceptions_fit[permalink]
        children = cat.get('pattern_attributes', [])
        if not len(children) == 0:
            simplified_list += [(category, permalink), simplify_fit(children)]
        else:
            simplified_list.append((category, permalink))
    return simplified_list


def get_all_pattern_categories():
    """Return all pattern categories at the time of the API call as a nested list."""

    url = "https://api.ravelry.com/pattern_categories/list.json"
    response = requests.get(url)
    categories = response.json()['pattern_categories']['children']
    return simplify(categories)


def get_all_pattern_attributes():
    """Return all pattern attributes at the time of the API call as a nested list."""

    url = "https://api.ravelry.com/pattern_attributes/groups.json"
    response = requests.get(url)
    attributes = response.json()['attribute_groups']
    return simplify_attributes(attributes)


def get_all_pattern_age_size_fit():
    """Return all pattern age/size/fit attributes at the time of the API call as a nested list."""

    url = "https://api.ravelry.com/pattern_attributes/groups.json"
    response = requests.get(url)
    fit_attributes = response.json()['attribute_groups'][1]['children']
    return simplify_fit(fit_attributes)


def get_all_yarn_weights():
    """Return all yarn weights at the time of the API call as a list."""

    url = "https://api.ravelry.com/yarn_weights.json"
    response = requests.get(url, auth=(API_USER, API_PASS))
    weights = response.json()['yarn_weights']
    return simplify(weights)


def get_all_pattern_source_types():
    """Return all pattern source types at the time of the API call as a list."""

    url = "https://api.ravelry.com/pattern_source_types/list.json"
    response = requests.get(url)
    sources = response.json()['pattern_source_types']
    return simplify(sources)


######### Logic of the randomizer


def format_queries(query_list, **kwargs):
    """Given tree.metadata and a search term (optional), format the queries as a list of parameters to be passed to generatePatternID()."""

    query_params = {}

    search = kwargs.get('search', None)
    if search:
        query_params['query'] = search
    for param in query_list:
        key = param.split(':')[0]
        value = param.split(':')[-1]
        if value == 'other':
            value = format_others(param)
        if key in query_params.keys(): # If parameter heading already exists in queries, add pipe (OR) operator.
            query_params[key] = query_params[key] + '|' + value
        else:
            query_params[key] = value
    return query_params


def format_others(param):
    """Format any 'other' parameters missing permalinks, and return the correct permalink."""

    split_param = param.split(':')
    category = split_param[-2:]
    return category[1] + "-" + category[0]


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

    pattern_description = pattern['notes']
    description = hp.simplify_description(pattern_description)
    if not description == "":
        return '"' + description + '"'
    else:
        return("No description found.")
    

def get_pattern_price(pattern):
    """Given a pattern, get a formatted version of the pattern's price."""

    if pattern['free']:
        return('Free')
    elif not pattern['price'] == None and not pattern['currency_symbol'] == None:
        price = str(pattern['price'])
        return(str(pattern['currency_symbol']) + price)
    else:
        return('Price unavailable')
    

def get_pattern_languages(pattern):
    """Given a pattern, get a formatted list of all the languages the pattern is available in."""

    languages = ", ".join([lan['name'] for lan in pattern['languages'][:3]]) 
    if len(pattern['languages']) > 3:
        languages = languages + '...'
    if languages == "": languages = "Unavailable"
    return('Languages: ' + languages)