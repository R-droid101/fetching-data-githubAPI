import requests
import csv
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_data(url):
    file = 'repos.csv'
    columns = ['Owner ID', 'Owner Name', 'Owner Email', 'Repository ID', 'Repository Name', 'Status', 'Stars Count']

    with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
    
        access_token = os.getenv('ACCESS_TOKEN')
        headers = {
            'Authorization': 'Token {}'.format(access_token)
        }
        resp = requests.get(url, headers=headers)
        repos = resp.json()

        # repos = data['items']
        print("\nSelected information about each repository:")
        for repo in repos:
            try:
                email = repo['owner']['email']
            except:
                email = ''
            writer.writerow({
                'Owner ID': repo['owner']['id'],
                'Owner Name': repo['owner']['login'],
                'Owner Email': email,
                'Repository ID': repo['id'],
                'Repository Name': repo['name'],
                'Status': 'Private' if repo['private'] else 'Public',
                'Stars Count': repo['stargazers_count']
            })

fetch_data('https://api.github.com/user/repos')