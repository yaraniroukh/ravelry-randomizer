"""
GUI for the Ravelry randomizer application, written with PySimpleGUI.

Allows users to:
    * customise their search query, given parameters taken from the Ravelry website
    * view a random pattern matching the query

"""

import randomizer as rd
import re
import PySimpleGUI as sg
from ctypes import windll
import helpers as hp
import webbrowser

windll.shcore.SetProcessDpiAwareness(1)

sg.LOOK_AND_FEEL_TABLE['RRTheme'] = {'BACKGROUND': '#F7F8F8', 
                                        'TEXT': '#2E4273', 
                                        'INPUT': '#ACBDCF', 
                                        'TEXT_INPUT': '#ACBDCF', 
                                        'SCROLL': '#ACBDCF', 
                                        'BUTTON': ('#FFFFFF', '#6282A2'), 
                                        'PROGRESS': ('#D1826B', '#CC8019'), 
                                        'BORDER': 1, 'SLIDER_DEPTH': 0,  
                                        'PROGRESS_DEPTH': 0} 
sg.theme('RRTheme')

# Checked and unchecked boxes using Base64 image encoding system
checked = b'iVBORw0KGgoAAAANSUhEUgAAABQAAAALBAMAAACNJ7BwAAAAAXNSR0IB2cksfwAAAAlwSFlzAAALEwAACxMBAJqcGAAAADBQTFRFvb29AAAA////////////AAAA////////////////////////////////////////aWfaEgAAABB0Uk5T/wA9AwTZKAECGAUIFQZDErNVXTwAAABXSURBVHicRc1LDYBADITh9oCAn01ZHjYwUj0bzgjBCk5QgAO2YQM9fZlMpiJx2qc1SQeYDnnPog6uE1QahlYhintwDBrB+U8Xvm6hLcBB24UTeb+xXfcDRREMM30B1B0AAAAASUVORK5CYII='
unchecked = b'iVBORw0KGgoAAAANSUhEUgAAABQAAAALBAMAAACNJ7BwAAAAAXNSR0IB2cksfwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAC1QTFRFvb29AAAA////////////////////////////////////////////////////otwswQAAAA90Uk5T/wA9AwQoAQIYBQgVBkMSyhnoTQAAADxJREFUeJxjYAABRiFhE2EGRkEgYBQVKxODMiUEBWFMIEsQzhRHMCURTCkEMwvBnIxgbhFkgNgmmHP5IQCwiwmTrDp7NQAAAABJRU5ErkJggg=='

no_image_found = b'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'

PARAMETERS = {
    ("Craft", "craft") : [("Crochet", "crochet"), ("Knitting", "knitting"), ("Machine Knitting", "machine-knitting"), ("Loom Knitting", "loom-knitting")],
    ("Availability", "availability") : [("Free", "free"), ("Purchase online", "online"), ("Purchase in print", "inprint"), ("Ravelry download", "ravelry"), ("Discontinued", "discontinued")],
    ("Has photo", "photo") : [("Yes", "yes"), ("No", "no")],
    ("Category", "pc") : rd.get_all_pattern_categories(),
    ("Attributes", "pa") : rd.get_all_pattern_attributes(),
    ("Age / Size / Fit", "fit") : rd.get_all_pattern_age_size_fit(),
    ("Yarn weight", "weight") : rd.get_all_yarn_weights(),
    ("Pattern source", "source-type") : rd.get_all_pattern_source_types()
}


######### Making the parameter tree


def get_unclickable_rows():
    """Return a list of all rows in the tree that should not be clickable, ie. impossible queries."""

    unclickable_categories = list(i[1] for i in PARAMETERS.keys())
    attributes = rd.get_all_pattern_attributes()
    unclickable_attributes = list(i[1] for i in attributes if type(i) is tuple)
    unclickable_attributes += get_unclickable_attributes(attributes, [])
    unclickable_fit_attributes = list(i[1] for i in rd.get_all_pattern_age_size_fit() if type(i) is tuple)
    return unclickable_categories + unclickable_attributes + unclickable_fit_attributes


def get_unclickable_attributes(attributes, unclickable):
    """Return a list of all subcategories in pattern attributes - these are impossible queries."""

    if attributes != []:
        if type(attributes[0]) is list and any(type(i) is list for i in attributes[0]):
            for cat in (i for i in attributes[0] if type(i) is tuple):
                unclickable.append(cat[1])
        get_unclickable_attributes(attributes[1:], unclickable)
    return unclickable


treedata = sg.TreeData()
latestnode = 0
unclickable_rows = get_unclickable_rows()


def generate_nodes(key, value):
    """Generate tree nodes from a nested list."""

    for param in value:
        if type(param) is list:
            generate_nodes(latestnode, param)
        else:
            icon = unchecked if param[1] not in unclickable_rows or key[:2] == 'pc' or param[0] == 'collared' else None
            treedata.insert(key, key + ':' + param[1], param[0], [param[1]], icon=icon)
            latestnode = key + ':' + param[1]


for key, value in PARAMETERS.items():
    treedata.insert("", key[1], key[0], value)
    generate_nodes(key[1], value)


tree = sg.Tree(data=treedata,
               headings=[],
               num_rows=len(PARAMETERS)+5, 
               show_expanded=False, 
               enable_events=True, 
               key="-PARAM TREE-",
               expand_y=True,
               row_height=30,
               auto_size_columns=False,
               col0_width=23,
               vertical_scroll_only=True,
               border_width=1,
               metadata=[])


######### Window methods


def update_windows(pattern, window):
    """Update all windows to display the pattern information after pattern generation."""

    image = rd.get_pattern_image(pattern)
    if image is not None:
        window['-PATTERN IMAGE-'].update(image)
    else:
        window['-PATTERN IMAGE-'].update(no_image_found)

    window['-PATTERN NAME-'].update(pattern['name'])
    window['-PATTERN NAME-'].set_cursor('hand2')
    window['-DATE PUBLISHED-'].update('Published: ' + hp.simplify_date(pattern['created_at']))
    window['-FAVORITES COUNT-'].update('Favourites count: ' + str(pattern['favorites_count']))
    window['-PROJECTS COUNT-'].update('Projects count: ' + str(pattern['projects_count']))
    window['-YARN WEIGHT-'].update('Yarn weight: ' + pattern.get('yarn_weight', {}).get('name', 'N/A'))
    window['-CRAFT TYPE-'].update('Craft: ' + pattern['craft']['name'])
    window['-PATTERN CATEGORY-'].update('Category: ' + pattern['pattern_categories'][0]['name'])
    window['-PATTERN DESCRIPTION-'].update(rd.get_pattern_description(pattern))
    window['-PATTERN AUTHOR-'].update('Author: ' + pattern['pattern_author']['name'])
    window['-PATTERN AUTHOR-'].set_cursor('hand2')
    window['-PRICE-'].update(rd.get_pattern_price(pattern))
    window['-LANGUAGES-'].update(rd.get_pattern_languages(pattern))


def clear_windows(window):
    """Update all windows to be empty if no pattern is found."""

    window['-PATTERN IMAGE-'].update('')
    window['-PATTERN NAME-'].update('')
    window['-PATTERN NAME-'].set_tooltip('')
    window['-PATTERN NAME-'].set_cursor('')
    window['-DATE PUBLISHED-'].update('')
    window['-FAVORITES COUNT-'].update('')
    window['-PROJECTS COUNT-'].update('')
    window['-YARN WEIGHT-'].update('')
    window['-CRAFT TYPE-'].update('')
    window['-PATTERN CATEGORY-'].update('')
    window['-PATTERN DESCRIPTION-'].update('')
    window['-PATTERN AUTHOR-'].update('')
    window['-PATTERN AUTHOR-'].set_tooltip('')
    window['-PATTERN AUTHOR-'].set_cursor('')
    window['-PRICE-'].update('')
    window['-LANGUAGES-'].update('')


######### Layout construction
    
parameter_column = sg.Column([
    [sg.Text('Search', size=(6,1)), sg.InputText(key='-SEARCH-', size=(15,1)), sg.Button('OK', key='-SEARCH BUTTON-')],
    [tree],
    [sg.Column([[]], size=(None, 130))],
    [sg.Column([[]], size=(15, 1)), sg.Column([[sg.Button("Deselect all", key="-DESELECT-"), sg.Button("Randomize", key="-RANDOMIZE-")]])],
], size=(280, 610))


pattern_view_column = sg.Column([
    [sg.Push(), sg.Text(key="-PATTERN NAME-", enable_events=True, font=('Helvetica', 11,'bold')), sg.Push()],
    [sg.Push(), sg.Column([[sg.Image(key="-PATTERN IMAGE-")]], size=(320, 320)), sg.Push()],
    [sg.Column([[sg.Text(key='-PATTERN AUTHOR-', enable_events=True)]], element_justification="left"), sg.Push(), sg.Column([[sg.Text(key='-PRICE-')]], element_justification="right")],
    [sg.Column([[sg.Text(key='-LANGUAGES-')]], element_justification="left"), sg.Push()],
    [sg.Column([[sg.Text(key='-DATE PUBLISHED-')], [sg.Text(key='-CRAFT TYPE-')], [sg.Text(key='-PATTERN CATEGORY-')], [sg.Text(key='-YARN WEIGHT-')], [sg.Text(key='-PROJECTS COUNT-')], [sg.Text(key='-FAVORITES COUNT-')],], element_justification="left", size=(225, None), vertical_alignment="top"), sg.Column([[sg.Text(key='-PATTERN DESCRIPTION-', expand_x=True, size=(None, None))]], element_justification="left", expand_x=True, vertical_alignment="top")],
], size=(560, 610), expand_x=True)


def main():

    layout= [
        [
            parameter_column,
            sg.VSeparator(),
            pattern_view_column
        ]
    ]


    window = sg.Window("Ravelry Pattern Randomizer", layout, finalize=True)
    window['-PARAM TREE-'].bind('<Double-Button-1>', ' double_click')
    window['-SEARCH-'].bind('<Return>', ' enter')
    window['-PARAM TREE-'].Widget['show'] = 'tree'
    search_term = ''
    pattern_found = False


    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == '-PARAM TREE- double_click':
            row = values['-PARAM TREE-'][0]

            if window['-PARAM TREE-'].TreeData.tree_dict[row].icon is not None:
            
                if row in tree.metadata:
                    tree.metadata.remove(row)
                    tree.update(key=row, icon=unchecked)
                else:
                    tree.metadata.append(row)
                    tree.update(key=row, icon=checked)

        if event == '-SEARCH- enter' or event == '-SEARCH BUTTON-':

            search_term = values['-SEARCH-']

            if re.search(r'[^a-zA-Z\d\s]', search_term):
                search_term = ''
                window['-SEARCH-'].update('')

        if event == '-DESELECT-':

            rows = tree.metadata
            tree.metadata = []

            for row in rows:
                tree.update(key=row, icon=unchecked)

            search_term = ''
            window['-SEARCH-'].update('')

        if event == '-RANDOMIZE-':
            queries = rd.format_queries(tree.metadata, search=search_term)
            random_pattern_id = rd.generate_pattern_ID(queries)

            if random_pattern_id == -100:
                pattern_found = False
                clear_windows(window)
                window['-PATTERN NAME-'].update("No pattern found matching your selections.")
            
            else:
                pattern_found = True
                pattern = rd.get_pattern(random_pattern_id)
                update_windows(pattern, window)
                pattern_url = rd.get_pattern_URL(pattern)
                pattern_author_url = rd.get_pattern_author_URL(pattern)

                window['-PATTERN NAME-'].set_tooltip(pattern_url)
                window['-PATTERN AUTHOR-'].set_tooltip(pattern_author_url)

        if event == '-PATTERN NAME-' and pattern_found:
            webbrowser.open(pattern_url)

        if event == '-PATTERN AUTHOR-' and pattern_found:
            webbrowser.open(pattern_url)

    window.close()

if __name__ == '__main__':
    main()