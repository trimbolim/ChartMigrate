import os
import requests
import config
import pprint

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
    #print(data)
    chart_by_num = {}
    for chart in data['result']:
        #print (chart['u_sort_field'])
        chart_by_num[chart['u_sort_field']] = chart
    return chart_by_num

def update_missing_parts(chart_uuid, missing_parts_string):
    url = f"https://swingshift.service-now.com/api/now/table/u_chart/{chart_uuid}"

    # Eg. User name="admin", Password="admin" for this code sample.
    user = os.getenv('SNC_USER')
    pwd = os.getenv('SNC_PWD')

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    putdata = {"u_missing_parts": f"{missing_parts_string}"}

    # Do the HTTP request
    response = requests.put(url, auth=(user, pwd), headers=headers ,json=putdata)

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        return False

    return True

def get_gigs_with_setlist():

    gigs = {}

    # https://swingshift.service-now.com/api/now/table/u_set_position?sysparm_query=u_gig.u_date%3Ejavascript%3Ags.endOfToday()&sysparm_exclude_reference_link=True&sysparm_fields=u_position%2Cu_gig.u_name%2Cu_gig.sys_id
    snc_path = "/api/now/table/"
    snc_table = "u_set_position"
    sysparm_query = f"u_gig.u_date>javascript:gs.endOfToday()"
    sysparm_exclude_reference_link = "True"
    snc_fields = ["u_gig.sys_id","u_gig.u_name","u_gig.u_date"]

    url = f"https://{config.snc_hostname}{snc_path}{snc_table}"
    url += f"?sysparm_query={sysparm_query}"
    url += f"&sysparm_exclude_reference_link={sysparm_exclude_reference_link}"
    url += f"&sysparm_fields={','.join(snc_fields)}"

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
    gig_data = response.json()

    #pprint.pprint(gig_data)

    for set_pos in gig_data['result']:
        #print (f"set pos is {set_pos}")
        gigs[(set_pos['u_gig.sys_id'])] = set_pos

    return gigs


def get_setlist_by_gig (gig_sys_id):

    gig_set_list = {}
    fields = ['u_position','u_set_list','u_gig.u_name','u_gig.u_date']
    url = f"https://swingshift.service-now.com/api/now/table/u_set_position?sysparm_query=u_gig%3D{gig_sys_id}&sysparm_exclude_reference_link=True&sysparm_fields={','.join(fields)}"

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
    sp_data = response.json()
    #print(sp_data['result'])

    gig_set_list['sets'] = {}

    for set_position in sp_data['result']:
        gig_set_list['gig_name'] = set_position['u_gig.u_name']
        gig_set_list['gig_date'] = set_position['u_gig.u_date']

        sp = set_position['u_position']
        gig_set_list['sets'][sp] = {}
        gig_set_list['sets'][sp]['set_list_id'] = set_position['u_set_list']
        gig_set_list['sets'][sp]['ordered_charts'] = get_setlist_charts(gig_set_list['sets'][sp]['set_list_id'])

    return gig_set_list

def get_setlist_charts(set_list_id):

    #print (f"getting charts for setlist {set_list_id}")
    set_list = []

    snc_path = "/api/now/table/"
    snc_table = "u_list_position"
    sysparm_query = f"u_set_list={set_list_id}"
    sysparm_exclude_reference_link = "True"
    snc_fields = ["u_chart","u_chart.u_sort_field","u_chart.u_slug","u_position"]

    url = f"https://{config.snc_hostname}{snc_path}{snc_table}"
    url += f"?sysparm_query={sysparm_query}"
    url += f"&sysparm_exclude_reference_link={sysparm_exclude_reference_link}"
    url += f"&sysparm_fields={','.join(snc_fields)}"

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
    chart_data = response.json()
    #print(chart_data['result'])

    sorted_positions = sorted(chart_data['result'], key=lambda x: int(x['u_position']))

    for pos in sorted_positions:
        #print (pos)
        set_list.append(pos)

    return set_list

    
        

