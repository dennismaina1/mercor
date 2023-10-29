import pandas as pd
import collections
import requests



def analyze_code_complexity_bito(code_text):
       api_key = ""  # Replace with your Bito API key
       url = "https://api.bito.ai/code-complexity"  # Bito API endpoint
       headers = {
           "Authorization": f"Bearer {api_key}",
           "Content-Type": "application/json"
       }
       data = {
           "code": code_text
       }
       response = requests.post(url, json=data, headers=headers)
       result = response.json()
       return result["score"], result["justification"]

def analyze_code_complexity(code_text):
    score, justification = analyze_code_complexity_bito(code_text)
    return {"score": score, "justification": justification}

def batch_analysis(files_to_preprocess):
    #initialize dictionary
    batches ={}
    results_by_repo = collections.defaultdict(list)

    for file_info in files_to_preprocess:
        file_path,repo_name = file_info
        if repo_name not in batches:
            batches[repo_name] = []
        batches[repo_name].append(file_path)
    
    for repo_name, code_batch in batches.items():
        combined_code_text = ""
        for code_file in code_batch:
            try:
                with open(code_file,'r',encoding='utf-8')as file:
                    code_content= file.read()
                combined_code_text += "\n"+ code_content
                print(f"repo {repo_name} batched")
            except UnicodeDecodeError:
                print(f"Repo {repo_name}: Skipping file '{code_file}' due to unsupported encoding")
        
        if combined_code_text:
            complexity_result = analyze_code_complexity_bito(combined_code_text)
            score = complexity_result[0]["score"]
            justification = complexity_result[0]["justification"]
            results_by_repo[repo_name].append({"score":score,"justification":justification})

    df= pd.DataFrame(results_by_repo)
    print(df)    
    df=pd.DataFrame(complexity_result)
    mean = df.groupby('repo_name').median().reset_index()
    print(mean)


