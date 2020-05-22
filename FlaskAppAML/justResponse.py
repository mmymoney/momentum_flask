import urllib.request
import json

data = {
        "Inputs": {
                "input1":
                [
                    {
                            'Open': "1",   
                            'High': "1",   
                            'Low': "1",   
                            'Close': "1",   
                            'Volume': "1",   
                            'T3_Vol_Diff': "1",   
                            'T3_Close_Diff': "1",   
                            'T3_Open_Diff': "1",   
                            'T2_Vol_Diff': "1",   
                            'T2_Close_Diff': "1",   
                            'T2_Open_Diff': "1",   
                            'T1_Vol_Diff': "1",   
                            'T1_Close_Diff': "1",   
                            'T1_Open_Diff': "1",   
                            'Prior_Day_Vert_Delta_Ratio': "1",   
                            'Retracement_Signal': "1",   
                            'Prior_Day_Derivative': "1",   
                            'T+1_Close': "1",   
                            'T+2_Close': "1",   
                            'T+3_Close': "1",   
                    }
                ],
        },
    "GlobalParameters":  {
    }
}

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/00d11b98f56946f286a640541b35f9ec/execute?api-version=2.0&format=swagger'
api_key = '6LgM3hobpFQkecNPOBz2QRHvSIzYJLdQBfahZtC49sPMjiOwIiNMAAtALXDNuZK1zE3DTzsKoJB4yvfZkSmDTQ==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))