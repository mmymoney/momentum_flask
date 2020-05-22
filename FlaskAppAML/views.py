"""
Routes and views for the flask application.
"""
import json
import urllib.request
import os

from datetime import datetime
from flask import render_template, request, redirect
from FlaskAppAML import app

from FlaskAppAML.forms import SubmissionForm

Bayesian_ML_KEY=os.environ.get('API_KEY', "6LgM3hobpFQkecNPOBz2QRHvSIzYJLdQBfahZtC49sPMjiOwIiNMAAtALXDNuZK1zE3DTzsKoJB4yvfZkSmDTQ==")
Bayesian_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/00d11b98f56946f286a640541b35f9ec/execute?api-version=2.0&details=true")
# Deployment environment variables defined on Azure (pull in with os.environ)

# Construct the HTTP request header
# HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ API_KEY)}

HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ Bayesian_ML_KEY)}

# Our main app page/route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    """Renders the home page which is the CNS of the web app currently, nothing pretty."""

    form = SubmissionForm(request.form)

    # Form has been submitted
    if request.method == 'POST' and form.validate():

        # Plug in the data into a dictionary object 
        #  - data from the input form
        #  - text data must be converted to lowercase
        data =  {
  "Inputs": {
    "input1": {
      "ColumnNames": [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "T3_Vol_Diff",
        "T3_Close_Diff",
        "T3_Open_Diff",
        "T2_Vol_Diff",
        "T2_Close_Diff",
        "T2_Open_Diff",
        "T1_Vol_Diff",
        "T1_Close_Diff",
        "T1_Open_Diff",
        "Prior_Day_Vert_Delta_Ratio",
        "Retracement_Signal",
        "Prior_Day_Derivative",
        "T+1_Close",
      ],
      "Values": [
        [
          form.Open.data,
          form.High.data,
          form.Low.data,
          form.Close.data,
          form.Volume.data,
          form.T3_Vol_Diff.data,
          form.T3_Close_Diff.data,
          form.T3_Open_Diff.data,
          form.T2_Vol_Diff.data,
          form.T2_Close_Diff.data,
          form.T2_Open_Diff.data,
          form.T1_Vol_Diff.data,
          form.T1_Close_Diff.data,
          form.T1_Open_Diff.data,
          form.Prior_Day_Vert_Delta_Ratio.data,
          form.Retracement_Signal.data,
          form.Prior_Day_Derivative.data,
          ""
        ]
      ]
    }
  },
  "GlobalParameters": {}
}

        # Serialize the input data into json string
        body = str.encode(json.dumps(data))
# str.encode
        # Formulate the request
        #req = urllib.request.Request(URL, body, HEADERS)
        req = urllib.request.Request(Bayesian_URL, body, HEADERS)

        # Send this request to the AML service and render the results on page
        try:
            # response = requests.post(URL, headers=HEADERS, data=body)
            response = urllib.request.urlopen(req)
            #print(response)
            respdata = response.read()
            result = json.loads(str(respdata, 'utf-8'))
            result = do_something_pretty(result)
            # result = json.dumps(result, indent=4, sort_keys=True)
            return render_template(
                'result.html',
                title="This is the result from AzureML running our example T+1 Prediction:",
                result=result)

        # An HTTP error
        except urllib.error.HTTPError as err:
            result="The request failed with status code: " + str(err.code)
            return render_template(
                'result.html',
                title='There was an error',
                result=result)
            #print(err)

    # Just serve up the input form
    return render_template(
        'form.html',
        form=form,
        title='Run App',
        year=datetime.now().year,
        message='Demonstrating a website using Azure ML Api')


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/lstm2')
def lstm2():
    """Renders the LSTM page."""
    return render_template(
        'lstm2.html',
        title='LSTM',
        year=datetime.now().year,
        message='Your LSTM page.'
    )

@app.route('/tableau')
def tableau():
    """Renders the LSTM page."""
    return render_template(
        'tableau.html',
        title='Market Data',
        year=datetime.now().year,
        message='Your market data page.'
    )

def do_something_pretty(jsondata):
    """We want to process the AML json result to be more human readable and understandable"""
    import itertools # for flattening a list of tuples below

    # We only want the first array from the array of arrays under "Value" 
    # - it's cluster assignment and distances from all centroid centers from k-means model
    value = jsondata["Results"]["output1"]["value"]["Values"][0]
    # valuelen = len(value)
    print(value)

    scored_label = value[18]
    
    # Convert values (a list) to a list of tuples [(cluster#,distance),...]
    # valuetuple = list(zip(range(valuelen-1), value[1:(valuelen)]))
    # Convert the list of tuples to one long list (flatten it)
    # valuelist = list(itertools.chain(*valuetuple))

    # Convert to a tuple for the list
    # data = tuple(list(value[0]) + valuelist)

    # Build a placeholder for the cluster#,distance values
    #repstr = '<tr><td>%d</td><td>%s</td></tr>' * (valuelen-1)
    # print(repstr)
    output_bayesian=f'Our Bayesian linear regression model would predict a value of {str((float(scored_label)*294.433746) + 43.90625)}'
    # Build the entire html table for the results data representation
    #tablestr = 'Cluster assignment: %s<br><br><table border="1"><tr><th>Cluster</th><th>Distance From Center</th></tr>'+ repstr + "</table>"
    #return tablestr % data
    return output_bayesian
