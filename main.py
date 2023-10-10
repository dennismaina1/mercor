import json
import os
import re
import shutil
import subprocess
from urllib.request import urlopen

 fetch_repo_content(github_url,target_dir):
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
            os.makedirs(target_dir)

        #change directoryto target
        os.chdir(target_dir)

        #json file containing repo info
        with open('repos.json', 'w')as outfile:
            json.dump(repos,outfile,indent=2)

        #clone repos
        for repo in repos:
            print (f"cloning repo {repo['html_url']}")
            subprocess.call(['git','clone',repo['html_url']],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"succesfully cloned repo {repo['html_url']}")

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

