import requests
import csv
from dotenv import load_dotenv
import os

load_dotenv()

f = open('repos.csv', "w+")
f.close()
flag = False

def fetch_data(url, flag):
    file = 'repos.csv'
    columns = ['Owner ID', 'Owner Name', 'Owner Email', 'Repository ID', 'Repository Name', 'Status', 'Stars Count']
    with open(file, 'a', newline='') as csvfile:
          
        access_token = os.getenv('ACCESS_TOKEN')
        headers = {
            'Authorization': 'Token {}'.format(access_token)
        }

        resp = requests.get(url, headers=headers)
        repos = resp.json()
        # print(repos)
        if(len(repos) == 0):
            flag = True
            print("No more repositories to fetch")
            return flag
        print("\n adding to csv:")
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
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
    return flag
for i in range(1, 10):
    if(flag == True):
        break
    else:
        flag = fetch_data('https://api.github.com/user/repos?page={}&per_page=100'.format(i), flag)
# fetch_data('https://api.github.com/user/repos?page=&per_page=100')