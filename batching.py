import os
import pandas as pd
import collections
from transformers import AutoModelForCausalLM,AutoTokenizer

#model parameters
model_name = "microsoft/codebert-base"
model = AutoModelForCausalLM.from_pretrained(model_name,is_decoder=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def analyze_code_complexity(code_text):
    result = model.generate(
            tokenizer.encode("Analyze the code for complexity analysis and give a complexity score and justification:" + code_text, return_tensors="pt"),
            max_length = 100,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            num_return_sequences=1,
            )
    generated_text = tokenizer.decode(result[0], skip_special_tokens=True)
    return generated_text 

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
            with open(code_file,'r',encoding='utf-8')as file:
                code_content= file.read()
            combined_code_text += "\n"+ code_content
            print(f"repo {repo_name} batched")

        #complexity_result = analyze_code_complexity(combined_code_text)
        #score = complexity_result[0]["score"]
        #justification = complexity_result[0]["justification"]

        #results_by_repo[repo_name].append({"score":score,"justification":justification})

        df= pd.DataFrame(results_by_repo)
        print(df)    
        df=pd.DataFrame(complexity_metrics)
        mean = df.groupby('repo_name').median().reset_index()
    print(mean)


