import nbformat
import os

#preprocessing_ipynb
def preprocess_ipynb(file_path):
    file_extension = '.py'
    try:
        with open (file_path,'r',encoding = 'utf-8') as notebook_file:
            content = nbformat.read(notebook_file, as_version=4)

        #code cells
        cells =[]

        #extract code cells and combine to one code block
        for cell in content.cells:
            if cell.cell_type == 'code':
                cells.append(cell.source)

        #combine code to one code string
        python_code = '\n'.join(cells)


        #directory containing original fle
        dir_path = os.path.dirname(file_path)
        #create_new_file
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_name = file_name.replace(' ','_')
        python_file = file_name + file_extension

        #file path
        python_file_path = os.path.join(dir_path, python_file)
        #delete ipynb file
        os.remove(file_path)   
        #return relevant data
        return python_code, python_file_path

    except Exception as e:
        print(f"Error: str{e}")
        
