import datetime
from dateutil.relativedelta import relativedelta

import requests
from urllib import urlencode
from requests.auth import HTTPBasicAuth

import config

def fetch_report(params={}):
    url = 'https://www.toggl.com/reports/api/v2/details'
    if len(params) > 0:
        url = url + '?{}'.format(urlencode(params))
    print url
    headers = {'content-type': 'application/json'}
    return requests.get(url, headers=headers, auth=HTTPBasicAuth(config.TOGGL_API_TOKEN, 'api_token'))

def fetch_unbilled_hours():

    params = {
        'workspace_id': '701673',
        'since': (datetime.date.today() - relativedelta(months=6)).isoformat(),
        'until': datetime.date.today().isoformat(),
        'user_agent': 'api_test',
        'tag_ids': '0'
    }
    page = 1
    projects = {}
    
    while True:
        params['page'] = page
        report = fetch_report(params).json()
        page_count = 1 + report['total_count']/report['per_page']

        for line in report['data']:
            project = line['project']
            if project not in projects:
                projects[project] = 0.0
            projects[project] += line['dur']/3600000.0

        page += 1
        if page > page_count:
            break

    return projects