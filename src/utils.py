import json
from logger import logging

def load_facet_values(facet_entries):
    """
    Load facet values from a JSON file and populate the facet entries.

    Parameters:
    - facet_entries (dict): A dictionary of Tkinter Entry widgets for facets.
    """
    try:
        with open('data/facet_values.json', 'r') as file:
            facet_values = json.load(file)
        for facet, value in facet_values.items():
            facet_entries[facet].insert(0, value)
    except FileNotFoundError:
        pass

def save_facet_values(facet_entries):
    """
    Save facet values to a JSON file.

    Parameters:
    - facet_entries (dict): A dictionary of Tkinter Entry widgets for facets.
    """
    gui_logger = logging.getLogger('gui_logger')
    facet_values = {facet: entry.get() for facet, entry in facet_entries.items()}
    gui_logger.debug('Saving facet values: ' + str(facet_values))
    with open('data/facet_values.json', 'w') as file:
        json.dump(facet_values, file)
