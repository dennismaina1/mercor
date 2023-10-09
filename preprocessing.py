import re
import os
from collections import defaultdict
from print_preferences import * 
`
def remove_imports(content, file_extension):
    rules =  {
            '.java':lambda content: re.sub(r'^\s*(import.*?;)\s*','',content,flags=re.MULTILINE),
            '.c': lambda content: re.sub(r'^\s*#include\s+<.*?>\s*$','',content,flags=re.MULTILINE),
             '.py': lambda content: re.sub(r'^\s*(import .*?|from .*? import .*?)\s*\n', '', content, flags=re.MULTILINE)
            }
    if file_extension in rules:
        preprocess = rules[file_extension](content)
    else:
        preprocess = content
    return (preprocess)


def preprocess_code(files,extension):
    try:
        if extension == '.c':
            #remove comments c style code
            CSTYLE = re.compile('''
            (//[^\n]*(?:\n|$))    #Everything between // and the end of the line/file
            |
            (/\*.*?\*/)           #Everything between /* and */
            ''', re.VERBOSE | re.MULTILINE | re.DOTALL)

            files_preprocessed = CSTYLE.sub('\n',files)
            #remove white spaces
            files_preprocessed = re.sub(r'^\s*\n', '', files, flags=re.MULTILINE) 
             
            return files_preprocessed

        elif extension == '.py':
            #remove comments from python style code
            PYSTYLE = re.compile(r'(?m)^ *#.*\n?',re.MULTILINE)
            files_preprocessed = PYSTYLE.sub('', files)
            #remove white leading spaces from code
            files_preprocessed = re.sub(r'^\s*\n', '', files, flags=re.MULTILINE)
            
            return files_preprocessed
        
        else:
            return files
                
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
                import_remove = remove_imports(content,file_extension)
                preprocessed_code = preprocess_code(import_remove, file_extension)
            
                #count tokens to find  large files
                token_count = len(preprocessed_code.split())
                if token_count <= max_tokens_per_file:
                    with open(file_path,'w', encoding='utf-8') as file:
                        file.write(preprocessed_code)
                        print_green(f"File '{file_name}' in '{repo_name}' preprocessed succesfully")
                else:
                    #slice code to fit token limit
                    sliced_code = preprocessed_code[:max_tokens_per_file]
                    with open(file_path, 'w', encoding='utf-8')as file:
                        file.write(sliced_code)

                    print_green(f"File '{file_name}' in '{repo_name}' preprocessed with token slicing")
                    
            #print(f"Ignoring file '{file_name}' in '{repo_name}': Not a code file")
    except Exception as e:
        print_red(f"Error: '{str(e)}'")



def main():
   code_files = ['.js', '.py', '.c', '.java', '.cs', '.php', '.cpp', '.h', '.rb', '.swift', '.ts', '.kt', '.kts', '.css']
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

