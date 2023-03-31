import os 
import openai
import sys
import json
import jsonlines
import pandas as pd

def call_openai(desc:str) -> str:
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=desc,
        temperature=0.5,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response

def write_csv_file(data:str,columns:[str]):
    df = pd.DataFrame([row.split('|') for row in data.split('\n')],columns=columns)
    print(df)
    df.to_csv('result.csv')

def read_csv_file(path:str) -> pd.DataFrame:
    df = pd.read_csv(path,index_col=None)
    return df

def dataframe_analysis(df:pd.DataFrame):

    response = call_openai(f'Can you make a detail analysis for me about the quality of this dataframe ? {df}')
    return f"""
    ----Analisys Result----

    First 10 lines of the Dataframe:

    {df.head(10)}

    Conclusion:

    {response['choices'][0]['text']}
    """

    
if __name__ == '__main__':
    #desc = 'A three-column spreadsheet with a index and authors of a bestsellers:\n\nIndex | Title |  Author'
    #result = create_sample_data(desc)
    #data = result['choices'][0]['text']
    df = read_csv_file('result_6000.csv')
    #write_csv_file(data,['index','title','author'])
    
    result = dataframe_analysis(df)
    print(result)