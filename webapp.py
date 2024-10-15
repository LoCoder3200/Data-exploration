from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    
@app.route('/showFact')
def render_fact():
    states = get_states()
    state = request.args.get('state')
    county = county_most_under_18(state)
    fact = "In " + state + ", the county with the highest percentage of under 18 year olds is " + county + "."
    return render_template('home.html', states=states, funFact=fact)
    
def get_states():
    """Return a list of state abbreviations from the demographic data."""
    with open('ufo_sightings.json') as demographics_data:
        counties = json.load(demographics_data)
    #states=[]
    #for c in counties:
        #if c["State"] not in states:
            #states.append(c["State"])
    #a more concise but less flexible and less easy to read version is below.
    states=list(set([c["State"] for c in counties])) #sets do not allow duplicates and the set function is optimized for removing duplicates
    return states



def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production