import json
from logger import logging

def load_facet_values(facet_entries, saved_facet_values):
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
            # Populate saved_facet_values
            saved_facet_values[facet] = value 
    except FileNotFoundError:
        pass

def save_facet_values(saved_facet_values):
    """
    Save facet values to a JSON file.

    Parameters:
    - saved_facet_values (dict): A dictionary of facet values.
    """
    gui_logger = logging.getLogger('gui_logger')  
    gui_logger.debug('Saving facet values: ' + str(saved_facet_values))
    with open('data/facet_values.json', 'w') as file:
        json.dump(saved_facet_values, file)

