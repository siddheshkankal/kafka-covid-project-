# import pandas as pd

# FILE_PATH = "D:\mine\kafka_project\covid_19_india.csv"
# columns=["Sno","Date","Time","State/UnionTerritory","ConfirmedIndianNational","ConfirmedForeignNational","Cured","Deaths","Confirmed"]


# class Covid:   
#     def __init__(self,record:dict):
#         # for k,v in record.items():
#         #     setattr(self,k,v)
        
#         self.record=record
   
#     @staticmethod
#     def dict_to_covid(data:dict,ctx):
#         return Covid(record=data)

#     def __str__(self):
#         return f"{self.record}"
    
# def get_covid_instance(file_path):
#     df=pd.read_csv(file_path)
#     df=df.iloc[:,:]
#     covids:List[Covid]=[]
#     for data in df.values:
#         covid=Covid(dict(zip(columns,data)))
#         covids.append(covid)
#         print(data)
#         print(covid)


# get_covid_instance(FILE_PATH) 


import boto3
import json
s3_client = boto3.client('s3',aws_access_key_id = 'AKIA2AGRDARF2X7SU636',
aws_secret_access_key = '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')

data = {'Sno': 3090, 'Date': '8/11/2021', 'Time': '8:00 AM', 'State/UnionTerritory': 'Maharashtra', 'ConfirmedIndianNational': 0, 'ConfirmedForeignNational': 0, 'Cured': 6159676, 'Deaths': 134201, 'Confirmed': 6363442}

# data = json.dumps(data).encode('utf-8')
# response = s3_client.put_object(Body = data,Bucket = 'april-demo-1',Key = 'new_file2')
# print(response)


# response = s3_client.get_object(Bucket = 'april-demo-1',Key = 'new_file2')
# print(response['Body'].read().decode('utf-8'))

# or

s3 = boto3.resource('s3',aws_access_key_id = 'AKIA2AGRDARF2X7SU636',aws_secret_access_key = '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')

s3.meta.client.upload_file(r'D:\mine\kafka_project\covid_19_india.csv', 'game-analysis-data','covid_19_india.csv')



