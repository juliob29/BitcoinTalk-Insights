"""
Utilities for helping with the testing of charts.
"""
import json
import plotly
import requests
import plotly.plotly as py

from requests.auth import HTTPBasicAuth


def get_pages(username, page_size, auth, headers):
    """
    Original method comes from Plotly's documentation
    at: 

        * https://plot.ly/python/delete-plots/
    """
    url = 'https://api.plot.ly/v2/folders/all?user=' + username + '&page_size=' +str(page_size)

    print(url)
    response = requests.get(url, auth=auth, headers=headers)
    if response.status_code != 200:
        return

    page = json.loads(response.content)
    yield page
    while True:
        resource = page['children']['next'] 
        if not resource:
            break
        response = requests.get(resource, auth=auth, headers=headers)
        if response.status_code != 200:
            break
        page = json.loads(response.content)
        yield page
        
def permanently_delete_files(username, api_key, page_size=100, filetype_to_delete='plot'):
    """
    Original method comes from Plotly's documentation
    at: 

        * https://plot.ly/python/delete-plots/
    """
    auth = HTTPBasicAuth(username, api_key)
    headers = {'Plotly-Client-Platform': 'python'}

    plotly.tools.set_credentials_file(username=username, api_key=api_key)

    for page in get_pages(username, page_size, auth, headers):
        print(page)
        for x in range(0, len(page['children']['results'])):
            fid = page['children']['results'][x]['fid']
            res = requests.get('https://api.plot.ly/v2/files/' + fid, 
                               auth=auth, headers=headers)

            res.raise_for_status()
            if res.status_code == 200:

                json_res = json.loads(res.content)
                if json_res['filetype'] == filetype_to_delete:
                    # move to trash
                    requests.post('https://api.plot.ly/v2/files/'+fid+'/trash', 
                                  auth=auth, headers=headers)

                    # permanently delete
                    requests.delete('https://api.plot.ly/v2/files/'+fid+'/permanent_delete', 
                                    auth=auth, headers=headers)
