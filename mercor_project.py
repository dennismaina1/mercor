import sys
from collections import defaultdict
import re
import requests
from transformers import GPT2Tokenizer,GPT2Model
import psutil
import gc
import git
import shutil
import os
import time
from colorama import Fore, Style
from tqdm import tqdm


#print in red
def print_red(text,delay=0.05):
    for char in text:
        sys.stdout.write(Fore.RED + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

#print with delays
def print_green(text,delay=0.05):
    for char in text:
        sys.stdout.write(Fore.GREEN + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()
#print prog language and  percentage
def print_prog_languages(code_files):
    language_counts = defaultdict(int)
    language_percentages = {}
    total_files = len(code_files)

    for file_path in code_files:
        ext = os.path.splitext(file_path)[1]
        #map extention to programming language
        language = {
                '.js': 'Javascript',
                '.c': 'C',
                '.py': 'Python',
                '.java':'Java',
                '.cs': 'C#',
                '.php': 'PHP',
                '.html': 'HTML',
                '.css': 'CSS',
                '.h': 'C/C++ Header',
                '.rb': 'Ruby',
                '.swift':'Swift',
                '.ts': 'Typescript',
                '.kt': 'Kotlin',
                '.kts': 'Kotlin Script'
                }.get(ext, 'Uknown')
        language_counts[language] += 1

    for language, count in language_counts.items():
        percentage = (count /total_files) * 100
        language_percentages[language] = percentage

    for language,percentage in language_percentages.items():
        print_green(f"{language} - {percentage:.2f}%\n")

#Identify/Delete Non-Code Files
def delete_non_code_files(repo_dir, max_file_size):
    code_file_ext = ['.js','.py','.c','.java','.cs','.php','.cpp','.h','.rb','.swift','.ts','.kt','.kts','.css']
    code_files = []

    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            file_path = os.path.join(root,file)

            if any(file_path.endswith(ext) for ext in code_file_ext):
                #check fize size and truncate or skip if too big
                code_files.append(file_path)
                if os.path.getsize(file_path) <= max_file_size:
                    code_files.append(file_path)
                else:
                    print_red(f"->Skipping large file:{file_path}")
            else:
                os.remove(file_path)
    print_green(f"->Deleted all non-code files from repo\n")
    return code_files
            
#function to get readme file 
def read_readme(repo_dir):
    readme_file_path = os.path.join(repo_dir, 'README.md')
    if os.path.exists(readme_file_path):
        with open(readme_file_path, 'r', encoding ='utf-8') as readme_file:
            readme_contents = readme_file.read()
            print_green ("->ReadMe file read successfully\n")
            return readme_contents
    else:
        print_red("->No ReadMe File found\n")
        return None
#function to clone repositoryi
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
            print_green(f"->Repository cloned succesfully\n")
            return repo
            cloning_in_progress=False
        else:
            print_red(f"->Failed to clone repo")

    except Exception as e:
        print_red(f"error: {str(e)}")

def main():
    max_file_size = 1024 * 1024
    target_dir="/home/vagrant/Data_Analysis_Project/repos/"
    while True:
        github_url = input("Enter a GitHub repository URL (e.g., https://github.com/username/repo): ")
        # Check if the user wants to exit
        if github_url.lower() == 'exit':
            break
        if not re.match(r'^https://github\.com/[^/]+/[^/]+$', github_url):
            print_red("Invalid GitHub URL. Please use the format https://github.com/username/repository.")
            continue
        print_green(f"Cloning  gitHub repo URL: {github_url}")
        #clone the repository
        clone_repository(github_url, target_dir)

        #find read me file
        print_green(f"->Analyzing repo to find Readme file\n")
        part = github_url.split('/')
        repo_name = part[-1]
        repo_dir = target_dir + repo_name
        readme_content = read_readme(repo_dir)
        #remove none code files
        code_files= delete_non_code_files(repo_dir,max_file_size)
        print_green("->Code File percentages by language:")
        #list programming languages used and percentage
        print_prog_languages(code_files)


if __name__ == "__main__":
        main()
