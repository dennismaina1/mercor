import re
import argparse
import os
from collections import defaultdict 
from ipynb import *

def parse_arguments():
    parser = argparse.ArgumentParser(description="A script to remove whitespace, comments and imports from code files")
    parser.add_argument("file", help="enter file to preprocess")
    args = parser.parse_args()
    
    return args

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
    elif ext in['.R','.Rmd']:
        code = code = re.sub(r'^(?:library|require|source|install.packages)\s*\(.+?\)(?:\n|$)', '', code, flags=re.MULTILINE)
    else:
        code = code

    return (code)




def preprocess_code(files,path,extension):
    try:
        if extension in ['.c','.h','.js','.ts','.js','.swift','.php','.cpp','.cs','.kt','.css','.kts','.java']:
            #remove comments single and multiline
            files_preprocessed_1 = re.sub(r'\/\/[^\n]*|\/\*[\s\S]*?\*\/', '', files, flags=re.MULTILINE)
            #remove imports
            files_preprocessed_2 = remove_imports(files_preprocessed_1, extension)
            #remove white spaces
            files_preprocessed_3 = re.sub(r'^\s*\n', '', files_preprocessed_2, flags=re.MULTILINE)

            return files_preprocessed_3,path


        elif extension == '.ipynb':
            #function to convert file to python file
            code, file_path = preprocess_ipynb(files, path)
            #change ext
            extension = '.py'    
            #remove comments
            files_preprocessed_1 = re.sub(r'(#.*?$|""".*?""")', '', code, flags=re.MULTILINE | re.DOTALL)
            #remove import statements
            files_preprocessed_2 = remove_imports(files_preprocessed_1,extension)
            #remove white spaces
            files_preprocessed_3 = re.sub(r'^\s*\n', '', files_preprocessed_2, flags=re.MULTILINE)

            
            return files_preprocessed_3,file_path

        elif extension in ['.py','.rb','.R','.Rmd']:
            #remove comments
            files_preprocessed_1 = re.sub(r'(#.*?$|""".*?""")', '', files, flags=re.MULTILINE | re.DOTALL)
            #remove import statements
            files_preprocessed_2 = remove_imports(files_preprocessed_1,extension)
            #remove whitespaces
            files_preprocessed_3 = re.sub(r'^\s*\n', '', files_preprocessed_2, flags=re.MULTILINE)

            return files_preprocessed_3,path
                
    except Exception as e:
        print(f"Error: '{str(e)}'")


def analyze_file(file_info):
    file_path, repo_name = file_info
    #CODE FILES
    code_files = ['.ipynb', '.R', '.Rmd', '.js', '.py', '.c', '.java', '.cs', '.php', '.html', '.cpp', '.h', '.rb', '.swift', '.ts', '.kt', '.kts', '.css']
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
                        print(f"File '{file_name}' in '{repo_name}' preprocessed succesfully")
                else:
                    #slice code to fit token limit
                    sliced_code,path = preprocessed_code[:max_tokens_per_file]
                    with open(path, 'w', encoding='utf-8')as file:
                        file.write(sliced_code)

                    print(f"File '{file_name}' in '{repo_name}' preprocessed with token slicing")
                    
        else:
            os.remove(file_path)
            print(f"removed file '{file_name}' in '{repo_name}': Not a code file")
    except Exception as e:
        print(f"Error: '{str(e)}'")



def main(files_to_preprocess):
    #define parameters
    for file_path in files_to_preprocess:
        analyze_file(file_path,repo_name)


if __name__ == "__main__":
    main()                                                                                                 

