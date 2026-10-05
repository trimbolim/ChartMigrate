import os
import requests

def get_snc_charts():
    url = 'https://swingshift.service-now.com/api/now/table/u_chart'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = os.getenv('SNC_USER')
    pwd = os.getenv('SNC_PWD')

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)
    chart_by_num = {}
    for chart in data['result']:
        print (chart['u_sort_field'])
        chart_by_num[chart['u_sort_field']] = chart
    return chart_by_num