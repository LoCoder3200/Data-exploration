from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route("/")
def home():
    states = get_states()
    return render_template('homepage.html', states=states)

@app.route('/findings')
def render_fact():
    states = get_states()
    if "state" in request.args:
        state = request.args.get('state')

        with open('ufo_sightings.json') as ufosightings:
            ufos = json.load (ufosightings)
        most = 0
        for num in ufos:
            if num["Data"] ["Encounter duration"] > most and num["Location"] ["State"] == state:
                most = num["Data"] ["Encounter duration"]
                
            fact = "In " + state + ",the longest encounter is " +str(most) + " seconds."

        return render_template('gage2.html', states=states, funFact=fact)
    return render_template('gage2.html', states=states)
    
@app.route('/datagraph')
def render_graph():
    sighted = get_sighted_years()
    return render_template('gage3.html',data = sighted)
    
def get_sighted_years():
    with open('ufo_sightings.json') as ufosightings:
        ufos = json.load (ufosightings)
    sighted= "["
    for u in ufos:
        if u["Dates"]["Sighted"]["Year"] == 2012 and u["Dates"]["Sighted"]["Month"] == 1:
            sighted += Markup("{x:" + str(u["Date"]["Sighted"]["Day"]) + ",y:" + str(u["Data"]["Encounter duration"]) + "}, ")
    sighted = sighted[:-1] + "]"
    return sighted 
     
def get_states():
    """Return a list of state abbreviations from the demographic data."""
    with open('ufo_sightings.json') as data:
        sightings = json.load(data)
    states=[]
    for c in sightings:
        if c["Location"]["State"] not in states:
            states.append(c["Location"]["State"])
    options=[]
    for s in states:
        options.append(s) #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options



def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url
    
if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production

