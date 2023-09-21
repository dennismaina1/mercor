import sys
import re
import requests
from transformers import GPT2Tokenizer,GPT2Model
import psutil
import gc
import git
import shutil
import os
from tqdm import tqdm


def clone_repository(github_url,target_dir):
    try:
        #check if repos folder is available

        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
            
            #remake the folder 
        os.makedirs(target_dir)
        parts = github_url.split('/')
        username,repository = parts[-2], parts[-1]
        repo_path = os.path.join(target_dir, repository)

        url = f'https://api.github.com/users/{username}'
        #get user
        response = requests.get(url)
        if response.status_code == 200:
            repo =git.Repo.clone_from(github_url, repo_path)
            print(f"repo cloned succesfully")
            return repo
        else:
            print(f"failed to clone repo")

    except Exception as e:
        print (f"error: {str(e)}")

def main():
    target_dir="/home/vagrant/Data_Analysis_Project/repos/"
    while True:
        github_url = input("Enter a GitHub repository eRL (e.g., https://github.com/username/repo): ")
        # Check if the user wants to exit
        if github_url.lower() == 'exit':
            break
        if not re.match(r'^https://github\.com/[^/]+/[^/]+$', github_url):
            print("Invalid GitHub URL. Please use the format https://github.com/username/repository.")
            continue
        print(f"GitHub repo URL: {github_url}")
        #clone the repository
        clone_repository(github_url, target_dir)


if __name__ == "__main__":
        main()
