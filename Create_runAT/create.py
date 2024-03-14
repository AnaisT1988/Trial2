import requests
import pandas as pd
import numpy as np


def test(data_raw):
    data_f=data_raw[['CAS Number','Property','Molecular Weight','IUPAC Name','SMILES', 'CID', 'Density',
        'Melting Point', 'Boiling Point', 'Boiling Point Unit',
        'Melting Point Unit','Dispense Tool Volumetrically','Dispense Tool Gravimetrically','Stock solution','Molar concentration']]
    data_csv=data_f.drop_duplicates()
    data_csv=data_csv.dropna(how='all')
    data_csv = data_csv.fillna('')
    data_csv['IUPAC Name'] = data_csv['IUPAC Name'].str.replace(';','')
    data_csv= data_csv.replace('N/A','')
    return data_csv

############ create article - LOOP -- don't add emplty values ###########################

def create_article(base_URL,token,att_new_article):

    URL_2 = base_URL +"cst-api/v1/product-management/articles/create-articles"

    headersAPI = {
    "accept": "application/json",
    #"Content-Type": "application/json",
    'Authorization': 'Bearer '+token,
    #'authorizationContext': 'accessToken'
    }
    data_f=att_new_article[['CAS Number','Property','Molecular Weight','IUPAC Name','SMILES', 'CID', 'Density',
        'Melting Point', 'Boiling Point', 'Boiling Point Unit',
        'Melting Point Unit','Dispense Tool Volumetrically','Dispense Tool Gravimetrically','Stock solution','Molar concentration']]
    data_csv=data_f.drop_duplicates()
    data_csv=data_csv.dropna(how='all')
    data_csv = data_csv.fillna('')
    data_csv['IUPAC Name'] = data_csv['IUPAC Name'].str.replace(';',' ')
    data_csv= data_csv.replace('N/A','')


    for i in data_csv.index:
    
        data={
        "Label": data_csv['IUPAC Name'][i],
        "Comment": "creation via API",
        "Attributes": [

            # Melting point
            ({
            "AttributeId": 95,
            "CstIdentifier": "322934DE-1CC3-4DA6-83B0-971831F4FE5F",
            "Value": data_csv['Melting Point'][i],
            "Unit": data_csv['Melting Point Unit'][i],
            "InsertedAt": "2022-11-30T11:41:06.076Z",
            }if data_csv['Melting Point'][i] !='' else {}),

            #Molar mass
        ({
            
            "AttributeId": 169,
            "CstIdentifier": "FB93A3DA-1C50-4C68-BF0F-EA0DE99B6CBF",
            "Value": data_csv['Molecular Weight'][i],
            #"Unit": 'None',
            "InsertedAt": "2022-11-30T11:41:06.076Z",
        }if data_csv['Molecular Weight'][i] !='' else {}),

            #Density
            ({
            
            "AttributeId": 59,
            "CstIdentifier": "B942B95D-E489-4864-B4AD-220AADFABE17",
            "Value": data_csv['Density'][i],
            #"Unit": 1200,
            "InsertedAt": "2022-11-30T11:41:06.076Z",
            }if data_csv['Density'][i] !='' else {}),


            #SMILES
            ({
            
            "AttributeId": 283,
            "CstIdentifier": "DB738391-E68A-4779-B471-11DDF045F890",
            "Value": data_csv['SMILES'][i],
            #"Unit": 'None',
            "InsertedAt": "2022-11-30T11:41:06.076Z",
            }if data_csv['SMILES'][i] !='' else {}),

            #Molar Concentration
            ({
            
            "AttributeId": 293,
            "CstIdentifier": "AAC544F2-D40A-4AB7-82D3-9A3CB880FC44",
            "Value": data_csv['Molar concentration'][i],
            #"Unit": 'None',
            "InsertedAt": "2022-11-30T11:41:06.076Z",
            }if data_csv['Molar concentration'][i] !='' else {}),

            #CAS Number
            ({
            
            "AttributeId": 33,
            "CstIdentifier": "345FAE2E-54E4-4D62-A693-8A8C00A031F8",
            "Value": data_csv['CAS Number'][i],
            #"Unit": 'None',
            "InsertedAt": "2022-11-30T11:41:06.076Z",
            }if data_csv['CAS Number'][i] !='' else {}),

            # Tag solvent
            ({
            
            "AttributeId": 247,
            "CstIdentifier": "8BF88CC4-77A1-43A6-B49F-F4CF31CB620F",
            "Value": bool(data_csv['Property'][i]=='solvent'),
            #"Unit": 'None',
            "InsertedAt": "2022-11-30T11:41:06.076Z",
            }if bool(data_csv['Property'][i]=='solvent') !='' else {}),

            # Tag dispensable or not
            {
            
            "AttributeId": 28,
            "CstIdentifier": "9E61F679-693D-4D72-94A7-B63F7B771175",
            "Value": True,
            #"Unit": 'None',
            "InsertedAt": "2022-11-30T11:41:06.076Z",
            },

            # Volumetric Tool
            ({
            
            "AttributeId": 139,
            "CstIdentifier": "A3662EB7-5735-4CE1-BF41-FFD4160DB057",
            "Value": data_csv['Dispense Tool Volumetrically'][i],
            #"Unit": 'None',
            "InsertedAt": "2022-11-30T11:41:06.076Z",
            }if data_csv['Dispense Tool Volumetrically'][i] !='' else {}),

        
            # Gravimetric Tool
            ({
            
            "AttributeId": 138,
            "CstIdentifier": "13196261-41A2-42DB-9F79-82D175396798",
            "Value": data_csv['Dispense Tool Gravimetrically'][i],
            #"Unit": 'None',
            "InsertedAt": "2022-11-30T11:41:06.076Z",
            }if data_csv['Dispense Tool Gravimetrically'][i] !='' else {})
        ]
        }

        data["Attributes"]=list(filter(None, data["Attributes"]))

        resp_2 = requests.post(URL_2,headers=headersAPI,json=data,verify=True)
        #print(resp_2.headers['Content-Type'])
        json_response=resp_2.json()

        no_Add=[]
        added=[]
        added_DF=pd.DataFrame()
        added_IUPAC_Name=[]

        if resp_2.status_code != 200:
            print('error: ' + str(resp_2.status_code))
            print(resp_2.json())
            no_Add=no_Add.append(data_csv['CAS Number'][i])
        else:
            print('Success')
            added_DF['CAS Number']=data_csv['CAS Number'][i]
            added_DF['IUPAC Name']=data_csv['IUPAC Name'][i]
            added_DF['ArtID']=json_response['result']
           # added=added.append(data_csv['CAS Number'][i])
            #added_IUPAC_Name=added_IUPAC_Name.append(data_csv['IUPAC Name'][i])
        
    return no_Add,added_DF#added

def create_product(base_URL,token,new_product):

    URL = base_URL +"cst-api/v1/product-management/products/create-product"

    headersAPI = {
    "accept": "application/json",
    #"Content-Type": "application/json",
    'Authorization': 'Bearer '+token,
    #'authorizationContext': 'accessToken'
    }

    new_product_unique=new_product[['ArtId','IUPAC Name']]
    new_product_unique.drop_duplicates(inplace=True)
    #new_product_unique.reset_index(inplace=True)

    new_product_unique['ArtId']=new_product_unique['ArtId'].astype(str)
    new_product_unique.to_csv('test_creation_product.csv')

    for i in new_product_unique.index:
        data= {"Label":new_product_unique['IUPAC Name'][i],"ArticleId":new_product_unique['ArtId'][i]}
        resp = requests.post(URL,headers=headersAPI,json=data,verify=True)

        if resp.status_code != 200:
            print('error: ' + str(resp.status_code))
    
        else:
            print('Success:' + new_product_unique['IUPAC Name'][i]+ ' have been created')

        json_resp=resp.json()

        new_product_unique['ProductID'][i]=json_resp['result']
    
    return new_product_unique