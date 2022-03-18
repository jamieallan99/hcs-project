import json
import pandas as pd
import json
from screenshot import SeleniumScreenshotter

with open('screenshot_analysis.txt', 'r') as f:
    lines = f.readlines()
    urls = [line.strip() for line in lines]

screenshot_data = {}

# Shorthand representations for analysis
kinds = {
    'i': 'implicit',  # You can use the site without clicking anything
    'ia': 'implicit adjustable',
    'e': 'explicit',  # You may be able to use the site but you need to give consent to have cookies turned on 
    'er': 'explicit rejectable',
    'ea': 'explicit adjustable',
    'b': 'blocked',  # You cannot use the site until you have given consent
    'br': 'blocked rejectable',
    'ba': 'blocked adjustable',
}

# Shorthand representations for analysis
locations = {
    't': 'top',
    'b': 'bottom',
    'l': 'left',
    'r': 'right',
    'c': 'centre',
}


# Wraps the user input and then gives a suitable output format
def get_screenshot_data(url):
    colour = input("What colour?: ").lower()
    location = locations[input("Where?: ").lower()]
    size = input('What size?: ').lower()
    kind = input("What kind?: ").lower()
    notes = input("Notes: ")
    try:
        kind = kinds[kind]
    except KeyError:
        pass
    data = {
        f'{url}': {
            'colour': colour,
            'location': location,
            'size': size,
            'type': kind,
            'notes': notes
        }
    }
    return data


s = SeleniumScreenshotter()

# Acts as the main logic loop
for url in urls:
    print(f'Open {s.take_screenshot(url)}')
    print(url)
    screenshot_data = json.load(open('screenshot_data.json'))
    screenshot_data.update(get_screenshot_data(url))
    with open('screenshot_data.json', 'w') as f:
        json.dump(screenshot_data, f, indent=2)

s.quit()
