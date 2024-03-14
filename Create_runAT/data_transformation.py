import pandas as pd
import numpy as np


def DT(data_raw, reactiontype):
    # data_raw.insert(
    #     loc=0, column="Experiment No.", value=list(range(1, len(data_raw.index) + 1))
    # )
    # data_raw.columns = data_raw.columns.str.replace("\_(.*)", "")

    columns_select = data_raw.loc[:, "Experiment No.":"reaction scale (mmol)"]
    columns_list = columns_select.columns

    columns_name = columns_list[1:-1]
    df = []
    DF = pd.DataFrame()

    number_solvent = 0
    for ele in list(columns_name):
        if ele.startswith('solvent'):
            number_solvent = number_solvent + 1

    if reactiontype == "HTemperature":
        for i in range(0, len(columns_name)):
            if i in range(0, len(columns_name) - number_solvent):
                df = data_raw[
                    [
                        "Experiment No.",
                        columns_name[i],
                        "temperature",
                        "pressure (bar)",
                        "time (h)",
                        "reaction scale (mmol)",
                        columns_name[i] + " equivalent",
                    ]
                ]
                df = df.rename(
                    columns={
                        columns_name[i]: "CAS Number",
                        columns_name[i] + " equivalent": "Equivalent",
                    }
                )
                df["Property"] = columns_name[i]
                DF = pd.concat([DF, df])
            else:
                df = data_raw[
                    [
                        "Experiment No.",
                        columns_name[i],
                        "temperature",
                        "pressure (bar)",
                        "time (h)",
                        "reaction scale (mmol)",
                    ]
                ]
                df = df.rename(columns={columns_name[i]: "CAS Number"})
                df["Property"] = columns_name[i]
                DF = pd.concat([DF, df])

    else:
        for i in range(0, len(columns_name)):
            if i in range(0, len(columns_name) - number_solvent):
                df = data_raw[
                    [
                        "Experiment No.",
                        columns_name[i],
                        "Wavelength",
                        "reaction scale (mmol)",
                        "time (h)",
                        "Temperature (C )",
                        columns_name[i] + " equivalent",
                    ]
                ]
                df = df.rename(
                    columns={
                        columns_name[i]: "CAS Number",
                        columns_name[i] + " equivalent": "Equivalent",
                    }
                )
                df["Property"] = columns_name[i]
                DF = pd.concat([DF, df])
            else:
                df = data_raw[
                    [
                        "Experiment No.",
                        columns_name[i],
                        "Wavelength",
                        "time (h)",
                        "Temperature (C )",
                        "reaction scale (mmol)",
                    ]
                ]
                df = df.rename(columns={columns_name[i]: "CAS Number"})
                df["Property"] = columns_name[i]
                DF = pd.concat([DF, df])

    DF.reset_index(drop=True, inplace=True)
    DF.to_csv("C:/Users/TERRIEAI/OneDrive - KAUST/Files_generated_python/DT.csv")

    for i in range(0, len(DF)):
        if DF['Property'].str.match('solvent')[i]==True:
            prop=DF.loc[i,'Property']
            DF.loc[i, "Volume"] = data_raw.loc[
                            DF.loc[i, "Experiment No."] - 1, prop + " amount (ml)"
                        ]
        else:
            continue

    return DF


def DT_filtered(main_df):
    data_f = main_df[["CAS Number", "Property"]]
    data_f = data_f.drop_duplicates()
    data_f = data_f[data_f["CAS Number"] != "-"]
    compounds_cas = data_f["CAS Number"].to_list()
    return compounds_cas
