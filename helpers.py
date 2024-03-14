"""
Helper methods for randomizer.py.

"""

import re

def slugify(string):
    """'Slugify' a given string to create a permalink."""

    string = string.lower().strip()
    string = string.replace(' ', '-')
    string = re.sub(r"[\(\)']", '', string)
    string = string.split('-/-')[0].split('/')[0]
    return string

def simplify_date(string):
    """Given a string representation of a date YYYY/MM/DD, simplify the date to 'Month, Year'."""

    months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
              '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
    date = string.split(' ')[0]
    year = date.split('/')[0]
    month = date.split('/')[1]
    return months[month] + ' ' + year