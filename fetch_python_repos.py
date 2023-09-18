import sys
import re
import requests

def fetch_github_repos(github_url):
    try: 
        #Extract username
        username = github_url.split('/')[-1]

        url = f'https://api.github.com/users/{username}/repos'
        #get user
        response = requests.get(url)
        if response.status_code == 200:
            repositories = response.json()
            print(f"Repositories for {username}:")
            for repo in repositories:
                print(repo['name'])
        else:
            print(f"noo")

        print("Repositories fetched successfully")
    except Exception as e:
        print (f"error: {str(e)}")

def main():
    while True:
        github_url = input("Enter a GitHub URL (e.g., https://github.com/username): ")
        # Check if the user wants to exit
        if github_url.lower() == 'exit':
            break
        if not re.match(r'^https://github\.com/', github_url):
            print("Invalid GitHub URL. Please use the format https://github.com/username.")
            continue
        print(f"GitHub URL: {github_url}")
        fetch_github_repos(github_url)

if __name__ == "__main__":
        main()
