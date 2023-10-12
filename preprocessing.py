import re
import os
from collections import defaultdict
from print_preferences import * 
from ipynb import *


def remove_imports(code,ext):
    #C,CPP,header files
    if ext in ['.cpp','.c','.h']:
        code = re.sub(r'#include\s+["<][^">]+[">]', '', code, flags=re.MULTILINE)
    #Javascript ,Python and Typescript
    elif ext in['.ts','.js','.py']:
        code = re.sub(r'^(?:import|from\s+\S+)\s+[^\n]*(?:\n|$)','',code, flags = re.MULTILINE)
    #java & Kotlin
    elif ext in ['.java','.kt','.kts']:
        code = re.sub(r'import\s+[^\n]*(?:\n|$)','',code, flags = re.MULTILINE)
    #C#
    elif ext == '.cs':
        code = re.sub(r'using\s+[^\n]*(?:\n|$)', '', code, flags=re.MULTILINE)
    #ruby
    elif ext == '.rb':
        code = re.sub(r'^(?:require|load)\s+[^\n]*(?:\n|$)', '', code, flags=re.MULTILINE)
    #PHP
    elif ext == '.php':
        code = re.sub(r'^(require|include)\s+[^\n]*(?:\n|$)', '', code, flags=re.MULTILINE)
        code = re.sub(r'^use\s+[^\n]*(?:\n|$)', '', code, flags=re.MULTILINE)
    else:
        code = code

    return (code)




def preprocess_code(files,path,extension):
    try:
        if extension in ['.c','.h','.js','.ts','.js','.swift','.php','.cpp','cs','.kt','.css','.kts','.java']:
            #remove comments single and multiline
            files_preprocessed_1 = re.sub(r'\/\/[^\n]*|\/\*[\s\S]*?\*\/', '', files, flags=re.MULTILINE)
            #remove White spaces
            files_preprocessed_2 = re.sub(r'^\s*\n', '', files_preprocessed_1, flags=re.MULTILINE)

            #remove imports
            files_preprocessed_3 = remove_imports(files_preprocessed_2, extension)

            return files_preprocessed_3,path


        elif extension == '.ipynb':
            #function to convert file to python file
            code, file_path = preprocess_ipynb(files, path)
    
            #remove comments
            files_preprocessed_1 = re.sub(r'(#.*?$|""".*?""")', '', code, flags=re.MULTILINE | re.DOTALL)
            #remove White spaces
            files_preprocessed_2 = re.sub(r'^\s*\n', '', files_preprocessed_1, flags=re.MULTILINE)
            #remove import statements
            files_preprocessed_3 = remove_imports(files_preprocessed_2,extension)
            
            return files_preprocessed_3,file_path

        elif extension =='.py' or extension == '.rb':
            #remove comments
            files_preprocessed_1 = re.sub(r'(#.*?$|""".*?""")', '', files, flags=re.MULTILINE | re.DOTALL)
            #remove White spaces
            files_preprocessed_2 = re.sub(r'^\s*\n', '', files_preprocessed_1, flags=re.MULTILINE)
            #remove import statements
            files_preprocessed_3 = remove_imports(files_preprocessed_2,extension)

            return files_preprocessed_3,path
                
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
                    
        else:
            os.remove(file_path)
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

