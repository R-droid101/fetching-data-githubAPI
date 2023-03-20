import requests
import csv
from dotenv import load_dotenv
import os

load_dotenv()

class GitHubScrapper:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.columns = ['Owner ID', 'Owner Name', 'Owner Email', 'Repository ID', 'Repository Name', 'Status', 'Stars Count']
        self.flag = False

    def write_to_csv(self, repos):
        with open(self.csv_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.columns)
            if csvfile.tell() == 0:
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

    def fetch_data(self, url):
        access_token = os.getenv('ACCESS_TOKEN')
        headers = {
            'Authorization': 'Token {}'.format(access_token)
        }

        resp = requests.get(url, headers=headers)
        repos = resp.json()
        if(len(repos) == 0):
            self.flag = True
            print("No more repositories to fetch")
            return
        print("\n adding to csv:")
        self.write_to_csv(repos)

    def scrape_repos(self):
        f = open('repos.csv', 'w+')
        f.close()
        for i in range(1, 10):
            if(self.flag == True):
                break
            else:
                self.fetch_data('https://api.github.com/user/repos?page={}&per_page=100'.format(i))

repo_fetch = GitHubScrapper('repos.csv')
repo_fetch.scrape_repos()