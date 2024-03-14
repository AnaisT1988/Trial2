import requests


def exist_product(base_URL, token, all_att_DOE):

    URL = (
        base_URL
        + "/cst-api/v1/product-management/products/get-products"
    )

    headersAPI = {
        "accept": "application/json",
        # "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        #'authorizationContext': 'accessToken'
    }

    product_exist = []
    product_tocreate=[]

    articleID=all_att_DOE['ArtId'].unique()
    articleID = [x for x in articleID if str(x) != 'nan']

    #change float to int
    articleID = list(map(int, articleID))

    for i in range(0, len(articleID)):

        data= {"ArticleId":articleID[i]}

        resp= requests.post(URL, headers=headersAPI, json=data, verify=True)

        if resp.json()["result"] == []:
            print( " There is no product related to this articleID "+ str(articleID[i]))
            product_tocreate.append(articleID[i])
        else:
            product_exist.append((articleID[i]))
    
    select_producttocreate=all_att_DOE['ArtId'].isin(product_tocreate)
    df_product_tocreate=all_att_DOE[select_producttocreate]
    

    return df_product_tocreate