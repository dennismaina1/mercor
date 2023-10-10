import re
import os
from collections import defaultdict
from print_preferences import * 
from ipynb import *


def preprocess_code(files,path,extension):
    try:
        if (extension == '.h' or extension == '.c'):
            #remove include_Statements
            files_preprocessed = re.sub(r'#include\s+["<][^">]+[">]', '', files, flags=re.MULTILINE)
            #remove comments single and multiline
            files_preprocessed_1 = re.sub(r'\/\/[^\n]*|\/\*[\s\S]*?\*\/', '', files_preprocessed, flags=re.MULTILINE)
            #remove White spaces
            files_preprocessed_2 = re.sub(r'^\s*\n', '', files_preprocessed_1, flags=re.MULTILINE)
            
            return files_preprocessed_2,path

        if (extension == '.ipynb'):
            #function to convert file to python file
            code, file_path = preprocess_ipynb(files, path)

            #remove imports
            files_preprocess_1 = re.sub(r'^(?:import|from\s+\S+)\s+[^\n]*(?:\n|$)', '', code, flags=re.MULTILINE)
            #remove comments
            files_preprocess_2 = re.sub(r'(#.*?$|""".*?""")', '', files_preprocess_1, flags=re.MULTILINE | re.DOTALL)
            #remove White spaces
            files_preprocessed_3 = re.sub(r'^\s*\n', '', files_preprocess_2, flags=re.MULTILINE)
            
            return files_preprocessed_3,file_path
                
    except Exception as e:
        print(f"Error: '{str(e)}'")


def analyze_file(repo_name, file_path, code_files):
    #max tokens per file
    max_tokens_per_file=4096
    try:

        #check if the file to read is a code file 
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension in code_files:
            with open(file_path,'r',encoding='utf-8') as file:
                content = file.read()
                preprocessed_code,path = preprocess_code(content, file_path,file_extension)
            
                #count tokens to find  large files
                token_count = len(preprocessed_code.split())
                if token_count <= max_tokens_per_file:
                    with open(path,'w', encoding='utf-8') as file:
                        file.write(preprocessed_code)
                        print_green(f"File '{file_name}' in '{repo_name}' preprocessed succesfully")
                else:
                    #slice code to fit token limit
                    sliced_code,path = preprocessed_code[:max_tokens_per_file]
                    with open(path, 'w', encoding='utf-8')as file:
                        file.write(sliced_code)

                    print_green(f"File '{file_name}' in '{repo_name}' preprocessed with token slicing")
                    
            #print(f"Ignoring file '{file_name}' in '{repo_name}': Not a code file")
    except Exception as e:
        print_red(f"Error: '{str(e)}'")



def main():
   code_files = ['.ipynb','.js', '.py', '.c', '.java', '.cs', '.php','.html', '.cpp', '.h', '.rb', '.swift', '.ts', '.kt', '.kts', '.css']
   target_dir = "/home/vagrant/Data_Analysis_Project/repos/"
   for root,dirs,files in os.walk(target_dir):
       for file_name in files:
           file_path = os.path.join(root, file_name)

           #store repo name
           repo_name = os.path.basename(root)
           #analyze the files
           analyze_file(repo_name, file_path,code_files)


if __name__ == "__main__":
    main()                                                                                                 

