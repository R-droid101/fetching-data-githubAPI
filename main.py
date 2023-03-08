import requests
import csv
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_data(url):
    access_token = os.getenv('ACCESS_TOKEN')
    headers = {
        'Authorization': 'Token {}'.format(access_token)
    }
    resp = requests.get(url, headers=headers)
    repos = resp.json()

    # repos = data['items']
    print("\nSelected information about each repository:")
    for repo in repos:
        print('Owner ID:', repo['owner']['id'])
        print('Owner Name:', repo['owner']['login'])
        try:
            print('Owner email:', repo['owner']['email'])
        except:
            print("Owner email: None")
        print('Repository Name:', repo['name'])
        print('Repository ID:', repo['id'])
        if(repo['private']):
            print('Status: Private')
        else:
            print('Status: Public')
        print('Stars:', repo['stargazers_count'])
        print("\n\n")

fetch_data('https://api.github.com/user/repos')