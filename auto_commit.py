import os
import requests
from datetime import datetime
import base64

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = 'mid-works'  # Replace with your GitHub username
REPO_NAME = 'auto_commit'  # Replace with your repository name
FILE_PATH = 'README.md'  # File to update
BRANCH_NAME = 'main'

URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"

def get_file_sha():
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        return response.json()['sha']
    return None

def commit_to_github(content, sha=None):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    data = {
        'message': f'Automated commit - {datetime.now()}',
        'content': base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        'branch': BRANCH_NAME,
    }
    if sha:
        data['sha'] = sha

    response = requests.put(URL, json=data, headers=headers)
    if response.status_code == 201 or response.status_code == 200:
        print('Successfully committed to GitHub')
    else:
        print(f'Failed to commit: {response.json()}')

if __name__ == "__main__":
    new_content = "Automated update on " + str(datetime.now()) + "\n"
    sha = get_file_sha()
    commit_to_github(new_content, sha=sha)
