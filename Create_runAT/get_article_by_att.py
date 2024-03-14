import requests


def exist_article(base_URL, token, compounds_cas):

    URL_4 = (
        base_URL
        + "/cst-api/v1/product-management/articles/get-articles-by-attributes-values"
    )

    headersAPI = {
        "accept": "application/json",
        # "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        #'authorizationContext': 'accessToken'
    }

    CASNumber_exist = []

    for i in range(0, len(compounds_cas)):

        data_csv_4 = [
            {
                "AttributeDefinition": {
                    "CstId": "345FAE2E-54E4-4D62-A693-8A8C00A031F8"
                },
                "Values": [{"String": compounds_cas[i]}],
            }
        ]

        resp_4 = requests.post(URL_4, headers=headersAPI, json=data_csv_4, verify=True)

        if resp_4.json()["result"] == []:
            print(compounds_cas[i] + " The article is not register")
        else:
            CASNumber_exist.append((compounds_cas[i]))

    return CASNumber_exist


def new_article_t(CASNumber_exist, data_csv_csv):

    list_CASNumber = set(data_csv_csv["CAS Number"])

    for i in CASNumber_exist:
        if i in list_CASNumber:
            data_csv_csv.drop(
                data_csv_csv[data_csv_csv["CAS Number"] == i].index, inplace=True
            )
        else:
            continue


def new_article(CASNumber_exist, compounds_cas):

    for i in range(0, len(CASNumber_exist)):
        if bool(CASNumber_exist[i] in compounds_cas) == True:
            compounds_cas.remove(CASNumber_exist[i])
        else:
            continue

    return compounds_cas


def get_att_byCASNumber(base_URL, token, data_csv):

    URL_2 = (
        base_URL
        + "/cst-api/v1/product-management/articles/get-articles-by-attributes-values"
    )

    headersAPI = {
        "accept": "application/json",
        "Authorization": "Bearer " + token,
    }

    for i in data_csv["CAS Number"]:
        if i != "-":
            data = [
                {
                    "AttributeDefinition": {
                        "CstId": "345FAE2E-54E4-4D62-A693-8A8C00A031F8"
                    },
                    "Values": [{"String": i}],
                }
            ]

            resp_2 = requests.post(URL_2, headers=headersAPI, json=data, verify=True)

            if resp_2.status_code == 200:
                tk_2 = resp_2.json()
                ex = tk_2["result"][0]
                ex_2 = ex["attributes"]

                index = data_csv[data_csv["CAS Number"].isin([i])].index

                data_csv.loc[index, "ArtId"] = ex["id"]
                data_csv.loc[index, "IUPAC Name"] = ex = tk_2["result"][0]["label"]

                for j in range(0, len(ex_2)):

                    if ex_2[j]["attributeDefinition"]["id"] == 95:
                        data_csv.loc[index, "Melting point"] = ex_2[j]["flattenedValue"]

                    elif ex_2[j]["attributeDefinition"]["id"] == 169:
                        data_csv.loc[index, "Molar mass"] = ex_2[j]["flattenedValue"]

                    # elif ex_2[i]['attributeDefinition']['id'] == 33:
                    #  data_csv['CAS NUMBER']= ex_2[i]['flattenedValue']

                    elif ex_2[j]["attributeDefinition"]["id"] == 139:
                        data_csv.loc[index, "Dispense Tool Volumetric"] = ex_2[j][
                            "flattenedValue"
                        ]

                    elif ex_2[j]["attributeDefinition"]["id"] == 138:
                        data_csv.loc[index, "Dispense Tool Gravimetric"] = ex_2[j][
                            "flattenedValue"
                        ]

                    elif ex_2[j]["attributeDefinition"]["id"] == 254:
                        data_csv.loc[index, "Internal Standard"] = ex_2[j][
                            "flattenedValue"
                        ]

                    elif ex_2[j]["attributeDefinition"]["id"] == 28:
                        data_csv.loc[index, "Dispensable"] = ex_2[j]["flattenedValue"]

                    elif ex_2[j]["attributeDefinition"]["id"] == 59:
                        data_csv.loc[index, "Density"] = ex_2[j]["flattenedValue"]

                    elif ex_2[j]["attributeDefinition"]["id"] == 294:
                        data_csv.loc[index, "ChemBeads Factor"] = ex_2[j][
                            "flattenedValue"
                        ]

                    elif ex_2[j]["attributeDefinition"]["id"] == 293:
                        data_csv.loc[index, "Molar Concentration"] = ex_2[j][
                            "flattenedValue"
                        ]

                    else:
                        continue
            else:
                pass
        else:
            pass

    return data_csv
