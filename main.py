import json
import concurrent.futures
import asyncio
import os
import re
import shutil
import subprocess
from urllib.request import urlopen

def clone_repo(repo_url, target_dir):
    try:
        #create directories for different repos
        repo_name = repo_url.split('/')[-1]
        repo_dir = os.path.join(target_dir, repo_name)
        if not os.path.exists(repo_dir): 
            os.mkdir(repo_dir)

        #clone repos
        subprocess.call(['git', 'clone', repo_url, repo_dir],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Sucessfully clone repo {repo_url}")
    except Exception as e:
        print(f" Failed to clone repo {repo_url} Error: {str(e)}")

def fetch_repo_content(github_url,target_dir):
    try:
        #extractusername
        username = github_url.split('/')[-1]

        #github API for repos
        reposLink = f"https://api.github.com/users/{username}/repos?type=all&per_page=100=1"
        #fetch the repos
        f = urlopen(reposLink)
        repos = json.loads(f.readline())
        print("Total number of repositories: {0}".format(len(repos)))

        #Delete target dir if exists
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        if not os.path.exists(target_dir):
            os.mkdir(target_dir)

        #clone repos
        with concurrent.futures.ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            clone_tasks = [loop.run_in_executor(executor, clone_repo,repo['html_url'],target_dir) for repo in repos]
            loop.run_until_complete(asyncio.gather(*clone_tasks))


    except Exception as e:
        print(f"Error:{str(e)}")

def main():
    #target Dir
    target_dir = "/home/vagrant/Data_Analysis_Project/repos/"

    #input github url  for analysis
    while True:
        github_url = input("Enter a GitHub user URL (e.g., https://github.com/username): ")
        #check if command is exit
        if github_url.lower()=='exit':
            break

        #check validity of data entered
        if not re.match(r'^https://github\.com/[^/]+$', github_url):
              print("Invalid GitHub URL. Use format 'https://github.com/username/repo'")
              continue

        print("Fetching repositories")
        fetch_repo_content(github_url, target_dir)

if __name__ == "__main__":
    main()
