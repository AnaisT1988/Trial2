import pandas as pd


def node_photochemistry_GC(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Dispense Tool Gravimetric"][i] == "GDU-PFD"
            or data["Dispense Tool Gravimetric"][i] == "GDU-S"
        ):
            data.loc[i, "Node"] = 1637
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif data["Dispense Tool Gravimetric"][i] == "GDU-V":
            data.loc[i, "Node"] = 1638
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif (
            data["Property"][i] == "solvent"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1645
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1644
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1639
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801

    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1641,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "400", "Unit": 1601},
                # Time
                {"ParameterId": 3, "Value": "8", "Unit": 602},
                # LED intensity
                {"ParameterId": 46, "Value": "1", "Unit": 2200},
            ],
        },
        {
            "NodeId": 1648,
            "TrialNumber": 0,
            "ParameterValues": [
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1648,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1651,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  ### change solvent if needed
                            "ArticleId": 218,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1652,
            "TrialNumber": 1,
            "ParameterValues": [
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801},
                # Needle use for air psuhing
                {"ParameterId": 41, "Value": "Needle 3", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1653,
            "TrialNumber": 1,
            "ParameterValues": [
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1653,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.3,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1656,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {  ### change solvent if needed
                            "ArticleId": 218,
                            "Amount": 1.2,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1660,
            "TrialNumber": 2,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 36, "Value": "E-Z-isomer Method 22May23", "Unit": 2600},
                # reaction speed
                {"ParameterId": 37, "Value": "Quantitative", "Unit": 2600},
                # Time
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }
            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1645 or b == 1639 or b == 1644:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )

            # dispense gravimetrically
            else:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Mass", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Mass": "Amount"})
                    .to_dict("records")
                )

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1645 or b == 1639 or b == 1644:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
        wavelength_node = {
            "NodeId": 1646,
            "TrialNumber": 0,
            "ParameterValues": [
                # Wavelength
                {"ParameterId": 47, "Value": data["Wavelength"][i], "Unit": 2600},
            ],
        }

        exp_list[i]["Nodes"].append(wavelength_node)

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 31,
        "Experiments": exp_list,
    }

    return create_run


def node_dispense(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Dispense Tool Gravimetric"][i] == "GDU-PFD"
            or data["Dispense Tool Gravimetric"][i] == "GDU-S"
        ):
            data.loc[i, "Node"] = 1348
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif data["Dispense Tool Gravimetric"][i] == "GDU-V":
            data.loc[i, "Node"] = 1463
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif (
            data["Property"][i] == "solvent"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1483
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1481
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1464
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801

    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1466,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "400", "Unit": 1601},
                # Time
                {"ParameterId": 3, "Value": "8", "Unit": 602},
            ],
        },
        {
            "NodeId": 1469,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1472,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 194,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1473,
            "TrialNumber": 2,
            "ParameterValues": [
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801}
            ],
        },
        {
            "NodeId": 1474,
            "TrialNumber": 3,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.3,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1477,
            "TrialNumber": 3,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 194,
                            "Amount": 1.2,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }
            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1464 or b == 1483 or b == 1481:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )

            # dispense gravimetrically
            else:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Mass", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Mass": "Amount"})
                    .to_dict("records")
                )

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1464 or b == 1483 or b == 1481:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 15,
        "Experiments": exp_list,
    }

    return create_run


def node_photochemistry_UPLC(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Dispense Tool Gravimetric"][i] == "GDU-PFD"
            or data["Dispense Tool Gravimetric"][i] == "GDU-S"
        ):
            data.loc[i, "Node"] = 1594
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif data["Dispense Tool Gravimetric"][i] == "GDU-V":
            data.loc[i, "Node"] = 1595
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif (
            data["Property"][i] == "solvent"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1613
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1612
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1596
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801

    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1598,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "400", "Unit": 1601},
                # Time
                {"ParameterId": 3, "Value": "8", "Unit": 602},
                # LED intensity
                {"ParameterId": 46, "Value": "1", "Unit": 2200},
            ],
        },
        {
            "NodeId": 1623,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1626,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  #### Change solvent if needed
                            "ArticleId": 197,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1627,
            "TrialNumber": 1,
            "ParameterValues": [
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801},
                # Needle use for air psuhing
                {"ParameterId": 41, "Value": "Needle 3", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1628,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.3,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1631,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {  #### Change solvent if needed
                            "ArticleId": 197,
                            "Amount": 1.2,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1633,
            "TrialNumber": 3,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 36, "Value": "E-Z-isomer-240", "Unit": 2600},
                # reaction speed
                {"ParameterId": 37, "Value": "MS-FID", "Unit": 2600},
                # Time
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                #### 4 ml vial #####
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }

            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1613 or b == 1596 or b == 1612:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )
            # dispense gravimetrically
            else:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Mass", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Mass": "Amount"})
                    .to_dict("records")
                )

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1613 or b == 1596 or b == 1612:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
        wavelength_node = {
            "NodeId": 1621,
            "TrialNumber": 0,
            "ParameterValues": [
                # Wavelength
                {"ParameterId": 47, "Value": data["Wavelength"][i], "Unit": 2600},
            ],
        }

        exp_list[i]["Nodes"].append(wavelength_node)

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 30,
        "Experiments": exp_list,
    }

    return create_run


def node_high_temperature(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Dispense Tool Gravimetric"][i] == "GDU-PFD"
            or data["Dispense Tool Gravimetric"][i] == "GDU-S"
        ):
            data.loc[i, "Node"] = 1528
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif data["Dispense Tool Gravimetric"][i] == "GDU-V":
            data.loc[i, "Node"] = 1529
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif (
            data["Property"][i] == "solvent"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1548
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1547
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1530
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801

    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1535,
            "TrialNumber": 0,
            "ParameterValues": [
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1535,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  ### change amount ?
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1538,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  #### Change article ?
                            "ArticleId": 194,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1539,
            "TrialNumber": 2,
            "ParameterValues": [
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801},
                # Needle use for air push
                {"ParameterId": 41, "Value": "Needle 3", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1540,
            "TrialNumber": 2,
            "ParameterValues": [
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1540,
            "TrialNumber": 3,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.3,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1543,
            "TrialNumber": 3,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {  ####  Change article ?
                            "ArticleId": 194,
                            "Amount": 1.2,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1545,
            "TrialNumber": 3,
            "ParameterValues": [
                # Method
                {"ParameterId": 36, "Value": "E-Z-isomer-240", "Unit": 2600},
                # Processing
                {"ParameterId": 37, "Value": "MS-FID", "Unit": 2600},
                # Volume injection
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }
            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1548 or b == 1530 or b == 1547:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )

            # dispense gravimetrically
            else:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Mass", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Mass": "Amount"})
                    .to_dict("records")
                )

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1548 or b == 1530 or b == 1547:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
        pressure_node = {
            "NodeId": 1549,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": data["temperature"][i], "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "400", "Unit": 1601},
                # Time
                {"ParameterId": 3, "Value": "18", "Unit": 602},
                # reaction pressure
                {"ParameterId": 4, "Value": data["pressure (bar)"][i], "Unit": 1501},
                # Settling Duration
                {"ParameterId": 14, "Value": "0", "Unit": 600},
                # Reaction Reactive Gas Valve
                {"ParameterId": 44, "Value": "1", "Unit": 2800},
            ],
        }
        exp_list[i]["Nodes"].append(pressure_node)
    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 25,
        "Experiments": exp_list,
    }

    return create_run


def test_swing_SP(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Dispense Tool Gravimetric"][i] == "GDU-PFD"
            or data["Dispense Tool Gravimetric"][i] == "GDU-S"
        ):
            data.loc[i, "Node"] = 1528
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif data["Dispense Tool Gravimetric"][i] == "GDU-V":
            data.loc[i, "Node"] = 1529
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif (
            data["Property"][i] == "solvent"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1548
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1696
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1530
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801

    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1716,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "400", "Unit": 1601},
                # Time
                {"ParameterId": 3, "Value": "8", "Unit": 602},
                # LED intensity
                {"ParameterId": 46, "Value": "1", "Unit": 2200},
            ],
        },
        {
            "NodeId": 1700,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1703,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  #### Change solvent if needed
                            "ArticleId": 194,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1704,
            "TrialNumber": 1,
            "ParameterValues": [
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801},
                # Needle use for air psuhing
                {"ParameterId": 41, "Value": "Needle 3", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1705,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.3,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1708,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {  #### Change solvent if needed
                            "ArticleId": 194,
                            "Amount": 1.2,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1711,
            "TrialNumber": 3,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 36, "Value": "E-Z-isomer-240", "Unit": 2600},
                # reaction speed
                {"ParameterId": 37, "Value": "MS-FID", "Unit": 2600},
                # Time
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                #### 4 ml vial #####
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }

            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1548 or b == 1696 or b == 1530:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )
            # dispense gravimetrically
            else:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Mass", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Mass": "Amount"})
                    .to_dict("records")
                )

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1548 or b == 1696 or b == 1530:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
        wavelength_node = {
            "NodeId": 1714,
            "TrialNumber": 0,
            "ParameterValues": [
                # Wavelength
                {"ParameterId": 47, "Value": data["Wavelength"][i], "Unit": 2600},
            ],
        }

        exp_list[i]["Nodes"].append(wavelength_node)

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 33,
        "Experiments": exp_list,
    }

    return create_run


def test_swing_SP_with_dispense(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    try:
        for i in range(0, len(data)):
            if (
                data["Dispense Tool Gravimetric"][i] == "GDU-PFD"
                or data["Dispense Tool Gravimetric"][i] == "GDU-S"
            ):
                data.loc[i, "Node"] = 1929
                data.loc[
                    i, "AttributeDefinitionCstId"
                ] = "13196261-41A2-42DB-9F79-82D175396798"
                data.loc[i, "Unit"] = 1002
            elif data["Dispense Tool Gravimetric"][i] == "GDU-V":
                data.loc[i, "Node"] = 1929
                data.loc[
                    i, "AttributeDefinitionCstId"
                ] = "13196261-41A2-42DB-9F79-82D175396798"
                data.loc[i, "Unit"] = 1002
            elif (
                data["Property"][i] == "solvent"
                and data["Dispense Tool Volumetric"][i] == "4NH"
            ):
                data.loc[i, "Node"] = 1932
                data.loc[
                    i, "AttributeDefinitionCstId"
                ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
                data.loc[i, "Unit"] = 801
            elif (
                data["Property"][i] == "Internal standard"
                and data["Dispense Tool Volumetric"][i] == "4NH"
            ):
                data.loc[i, "Node"] = 1912
                data.loc[
                    i, "AttributeDefinitionCstId"
                ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
                data.loc[i, "Unit"] = 801
            else:
                data.loc[i, "Node"] = 1932
                data.loc[
                    i, "AttributeDefinitionCstId"
                ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
                data.loc[i, "Unit"] = 801
    except:

        for i in range(0, len(data)):
                
                if (
                    data["Property"][i] == "solvent"
                    and data["Dispense Tool Volumetric"][i] == "4NH"
                ):
                    data.loc[i, "Node"] = 1932
                    data.loc[
                        i, "AttributeDefinitionCstId"
                    ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
                    data.loc[i, "Unit"] = 801
                elif (
                    data["Property"][i] == "Internal standard"
                    and data["Dispense Tool Volumetric"][i] == "4NH"
                ):
                    data.loc[i, "Node"] = 1912
                    data.loc[
                        i, "AttributeDefinitionCstId"
                    ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
                    data.loc[i, "Unit"] = 801
                else:
                    data.loc[i, "Node"] = 1932
                    data.loc[
                        i, "AttributeDefinitionCstId"
                    ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
                    data.loc[i, "Unit"] = 801

    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1933,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing duration
                {"ParameterId": 10, "Value": "2", "Unit": 601},
                # Mixing speed
                {"ParameterId": 11, "Value": "150", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1928,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "800", "Unit": 1601},
                # Time
                {"ParameterId": 3, "Value": "5", "Unit": 602},
                # LED intensity
                {"ParameterId": 46, "Value": "1", "Unit": 2200},
            ],
        },
        {
            "NodeId": 1913,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {"NodeId": 1913,
            "TrialNumber": 0,
            "ParameterValues": [
               
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1911,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing duration
                {"ParameterId": 10, "Value": "2", "Unit": 601},
                # Mixing speed
                {"ParameterId": 11, "Value": "150", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1916,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  #### Change solvent if needed
                            "ArticleId": 194,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1917,
            "TrialNumber": 1,
            "ParameterValues": [
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801},
                # Needle use for air psuhing
                {"ParameterId": 41, "Value": "Needle 3", "Unit": 2600},
            ],
        },
        {"NodeId": 1918,
            "TrialNumber": 1,
            "ParameterValues": [
               
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1918,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        
          {  "NodeId": 1921,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {  #### Change solvent if needed
                            "ArticleId": 194,
                            "Amount": 1,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
         {
            "NodeId": 1922,
            "TrialNumber": 2,
            "ParameterValues": [
                # Mixing duration
                {"ParameterId": 10, "Value": "2", "Unit": 601},
                # Mixing speed
                {"ParameterId": 11, "Value": "150", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1924,
            "TrialNumber": 2,
            "ParameterValues": [
                 # Instrument Method
                {"ParameterId": 36, "Value": "Method_Agilent_102423", "Unit": 2600},
                # Processing method
                {"ParameterId": 37, "Value": "Birchreduction_SWING_SP", "Unit": 2600},
                # Volume injection
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                #### 4 ml vial #####
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }

            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1932 or b == 1912:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )
            # dispense gravimetrically
            else:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Mass", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Mass": "Amount"})
                    .to_dict("records")
                )

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1932 or b == 1912:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
        wavelength_node = {
            "NodeId": 1926,
            "TrialNumber": 0,
            "ParameterValues": [
                # Wavelength
                {"ParameterId": 47, "Value": data["Wavelength"][i], "Unit": 2600},
            ],
        }

        photochemistry_node=   {
            "NodeId": 1928,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "800", "Unit": 1601},
                # Time
                {"ParameterId": 3, "Value": data["time (h)"][i], "Unit": 602},
                # LED intensity
                {"ParameterId": 46, "Value": "1", "Unit": 2200},
            ],
        },

        exp_list[i]["Nodes"].append(wavelength_node)

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 42,
        "Experiments": exp_list,
    }

    return create_run

def test_swing_SP_with_dispense_order(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Dispense Tool Gravimetric"][i] == "GDU-PFD" or data["Dispense Tool Gravimetric"][i] == "GDU-S" or data["Dispense Tool Gravimetric"][i] == "GDU-S"

        ):
            data.loc[i, "Node"] = 1951
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002

        elif data["Dispense Tool Gravimetric"][i] == "GDU-V":
            data.loc[i, "Node"] = 1956
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        
        elif (
            data["Property"][i] == "solvent A"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1954
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1935
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1957
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801


    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

 
    data.to_csv("C:/Users/TERRIEAI/OneDrive - KAUST/Files_generated_python/Data_createjson.csv")

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1955,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing duration
                {"ParameterId": 10, "Value": "2", "Unit": 601},
                # Mixing speed
                {"ParameterId": 11, "Value": "450", "Unit": 1601},
            ],
        },
       
        {
            "NodeId": 1936,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {"NodeId": 1936,
            "TrialNumber": 0,
            "ParameterValues": [
               
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1934,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing duration
                {"ParameterId": 10, "Value": "2", "Unit": 601},
                # Mixing speed
                {"ParameterId": 11, "Value": "450", "Unit": 1601},
            ],
        },
         
        {
            "NodeId": 1939,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  #### Change solvent if needed
                            "ArticleId": 194,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1940,
            "TrialNumber": 1,
            "ParameterValues": [
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801},
                # Needle use for air psuhing
                {"ParameterId": 41, "Value": "Needle 3", "Unit": 2600},
            ],
        },
        {"NodeId": 1941,
            "TrialNumber": 1,
            "ParameterValues": [
               
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1941,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        
          {  "NodeId": 1943,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {  #### Change solvent if needed
                            "ArticleId": 194,
                            "Amount": 1,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
         {
            "NodeId": 1944,
            "TrialNumber": 2,
            "ParameterValues": [
                # Mixing duration
                {"ParameterId": 10, "Value": "2", "Unit": 601},
                # Mixing speed
                {"ParameterId": 11, "Value": "450", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1946,
            "TrialNumber": 2,
            "ParameterValues": [
                 # Instrument Method
                {"ParameterId": 36, "Value": "Method_Agilent_102423", "Unit": 2600},
                # Processing method
                {"ParameterId": 37, "Value": "Birchreduction_SWING_SP", "Unit": 2600},
                # Volume injection
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                #### 4 ml vial #####
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }

            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1954 or b == 1957 or b == 1935 :
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )
            # dispense gravimetrically
            else:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Mass", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Mass": "Amount"})
                    .to_dict("records")
                )

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1954 or b == 1957 or b==1935:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
        wavelength_node = {
            "NodeId": 1948,
            "TrialNumber": 0,
            "ParameterValues": [
                # Wavelength
                {"ParameterId": 47, "Value": data["Wavelength"][i], "Unit": 2600},
            ],
        }

        photochemistry_node=   {
            "NodeId": 1950,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "800", "Unit": 1601},
                # Time
                {"ParameterId": 3, "Value":str(data["time (h)"][i]), "Unit": 602},
                # LED intensity
                {"ParameterId": 46, "Value": "1", "Unit": 2200},
            ],
        },

        exp_list[i]["Nodes"].append(wavelength_node)
        exp_list[i]["Nodes"].extend(photochemistry_node)

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 43,
        "Experiments": exp_list,
    }

    return create_run


def node_photochemistry_SWING_SP(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Property"][i] == "solvent"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1765
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1770
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1765
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801

    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1787,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing speed
                {"ParameterId": 11, "Value": "150", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1767,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "400", "Unit": 1601},
                # Time
                {"ParameterId": 3, "Value": "8", "Unit": 602},
                # LED intensity
                {"ParameterId": 46, "Value": "1", "Unit": 2200},
            ],
        },
        {
            "NodeId": 1769,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing speed
                {"ParameterId": 11, "Value": "150", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1774,
            "TrialNumber": 0,
            "ParameterValues": [
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1774,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1777,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  ### change solvent if needed
                            "ArticleId": 218,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1778,
            "TrialNumber": 1,
            "ParameterValues": [
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801},
                # Needle use for air psuhing
                {"ParameterId": 41, "Value": "Needle 3", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1779,
            "TrialNumber": 1,
            "ParameterValues": [
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1779,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.3,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1782,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {  ### change solvent if needed
                            "ArticleId": 218,
                            "Amount": 1.2,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1785,
            "TrialNumber": 2,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 36, "Value": "E-Z-isomer Method 22May23", "Unit": 2600},
                # reaction speed
                {"ParameterId": 37, "Value": "Quantitative", "Unit": 2600},
                # Time
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }
            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1765 or b == 1770 or b == 1644:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )

            # dispense gravimetrically
            else:
                pass

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1765 or b == 1770 or b == 1644:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
        wavelength_node = {
            "NodeId": 1772,
            "TrialNumber": 0,
            "ParameterValues": [
                # Wavelength
                {"ParameterId": 47, "Value": data["Wavelength"][i], "Unit": 2600},
            ],
        }

        exp_list[i]["Nodes"].append(wavelength_node)

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 36,
        "Experiments": exp_list,
    }

    return create_run


def node_photochemistry_SWING_SP_waiting(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Property"][i] == "solvent"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1788
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1791
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1788
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801

    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1789,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "400", "Unit": 1601},
                # Time s/minutes/hour 600/601/602
                {"ParameterId": 3, "Value": "1", "Unit": 601},
                # Settling duration
                {"ParameterId": 14, "Value": "5", "Unit": 600},
                # Use photodiodes
                {"ParameterId": 27, "Value": "TRUE", "Unit": 2700},
                # LED intensity
                {"ParameterId": 46, "Value": "1", "Unit": 2200},
            ],
        },
        {
            "NodeId": 1807,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing speed
                {"ParameterId": 11, "Value": "150", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1808,
            "TrialNumber": 0,
            "ParameterValues": [
                # Time
                {"ParameterId": 39, "Value": "1", "Unit": 601},
            ],
        },
        {
            "NodeId": 1790,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing speed
                {"ParameterId": 11, "Value": "150", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1794,
            "TrialNumber": 0,
            "ParameterValues": [
                # Needle use for transfer volumetricaly
                {"ParameterId": 41, "Value": "Needle 1", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1794,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1797,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  ### change solvent if needed
                            "ArticleId": 218,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1798,
            "TrialNumber": 1,
            "ParameterValues": [
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801},
                # Needle use for air psuhing
                {"ParameterId": 41, "Value": "Needle 3", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1799,
            "TrialNumber": 1,
            "ParameterValues": [
                # Needle use for transfer volumetricaly
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1799,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.3,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1802,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {  ### change solvent if needed
                            "ArticleId": 218,
                            "Amount": 1.2,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1805,
            "TrialNumber": 2,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 36, "Value": "E-Z-isomer Method 22May23", "Unit": 2600},
                # reaction speed
                {"ParameterId": 37, "Value": "Quantitative", "Unit": 2600},
                # Time
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }
            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1788 or b == 1791:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )

            # dispense gravimetrically
            else:
                pass

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1788 or b == 1791:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
        wavelength_node = {
            "NodeId": 1792,
            "TrialNumber": 0,
            "ParameterValues": [
                # Wavelength
                {"ParameterId": 47, "Value": data["Wavelength"][i], "Unit": 2600},
            ],
        }

        exp_list[i]["Nodes"].append(wavelength_node)

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 37,
        "Experiments": exp_list,
    }

    return create_run


def node_photochemistry_SWING_SP_waiting_new(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Property"][i] == "solvent"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1809
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1812
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1809
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801

    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1810,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "1000", "Unit": 1601},
                # Time s/minutes/hour 600/601/602
                {"ParameterId": 3, "Value": "3", "Unit": 602},
                # Settling duration
                {"ParameterId": 14, "Value": "5", "Unit": 600},
                # Use photodiodes
                {"ParameterId": 27, "Value": "TRUE", "Unit": 2700},
                # LED intensity
                {"ParameterId": 46, "Value": "1", "Unit": 2200},
            ],
        },
        {
            "NodeId": 1828,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing speed
                {"ParameterId": 11, "Value": "150", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1829,
            "TrialNumber": 0,
            "ParameterValues": [
                # Time
                {"ParameterId": 39, "Value": "1", "Unit": 601},
            ],
        },
        {
            "NodeId": 1811,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing speed
                {"ParameterId": 11, "Value": "150", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1815,
            "TrialNumber": 0,
            "ParameterValues": [
                # Needle use for transfer volumetricaly
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1815,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1818,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  ### change solvent if needed
                            "ArticleId": 194,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1819,
            "TrialNumber": 1,
            "ParameterValues": [
                {"ParameterId": 30, "Value": "10", "Unit": 901},
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801},
                # Needle use for air psuhing
                {"ParameterId": 41, "Value": "Needle 3", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1820,
            "TrialNumber": 1,
            "ParameterValues": [
                # Needle use for transfer volumetricaly
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1820,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1823,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {  ### change solvent if needed
                            "ArticleId": 194,
                            "Amount": 1,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1826,
            "TrialNumber": 2,
            "ParameterValues": [
                # Instrument Method
                {"ParameterId": 36, "Value": "Method_Agilent_102423", "Unit": 2600},
                # Processing method
                {"ParameterId": 37, "Value": "Photochemistry_SWING_SP", "Unit": 2600},
                # Volume injection
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }
            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1809 or b == 1812:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )

            # dispense gravimetrically
            else:
                pass

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1809 or b == 1812:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
        wavelength_node = {
            "NodeId": 1813,
            "TrialNumber": 0,
            "ParameterValues": [
                # Wavelength
                {"ParameterId": 47, "Value": data["Wavelength"][i], "Unit": 2600},
            ],
        }

        exp_list[i]["Nodes"].append(wavelength_node)

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 38,
        "Experiments": exp_list,
    }

    return create_run


def SWING_SP_demo(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Property"][i] == "solvent"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1854
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Dispense Tool Gravimetric"][i] == "GDU-PFD" or data["Dispense Tool Gravimetric"][i] == "GDU-S" 

        ):
            data.loc[i, "Node"] = 1853
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1854
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1854
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801

    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1857,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing speed
                {"ParameterId": 11, "Value": "150", "Unit": 1601},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }
            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1854 or b == 1812:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )

            # dispense gravimetrically
            
            else:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["id", "Mass", "Unit"]]
                    .rename(columns={"id": "ArticleId", "Mass": "Amount"})
                    .to_dict("records")
                )


            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1854 or b == 1812:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 39,
        "Experiments": exp_list,
    }

    return create_run


def node_photochemistry_troubleshooting(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Dispense Tool Gravimetric"][i] == "GDU-PFD"
            or data["Dispense Tool Gravimetric"][i] == "GDU-S"
        ):
            data.loc[i, "Node"] = 1868
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif data["Dispense Tool Gravimetric"][i] == "GDU-V":
            data.loc[i, "Node"] = 1869
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        elif (
            data["Property"][i] == "solvent"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1870
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1870
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1876
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801

    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1641,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "400", "Unit": 1601},
                # Time
                {"ParameterId": 3, "Value": "1", "Unit": 601},
                # LED intensity
                {"ParameterId": 46, "Value": "1", "Unit": 2200},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }
            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1870 or b == 1876:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )

            # dispense gravimetrically
            else:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Mass", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Mass": "Amount"})
                    .to_dict("records")
                )

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1870 or b == 1876:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
        wavelength_node = {
            "NodeId": 1877,
            "TrialNumber": 0,
            "ParameterValues": [
                # Wavelength
                {"ParameterId": 47, "Value": data["Wavelength"][i], "Unit": 2600},
            ],
        }

        exp_list[i]["Nodes"].append(wavelength_node)

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 40,
        "Experiments": exp_list,
    }

    return create_run


def node_SWING_SP_WORKUP(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1897,
            "TrialNumber": 0,
            "ParameterValues": [
                # Needle use for transfer volumetricaly
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1897,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1900,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  ### change solvent if needed
                            "ArticleId": 194,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1901,
            "TrialNumber": 1,
            "ParameterValues": [
                {"ParameterId": 30, "Value": "10", "Unit": 901},
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801},
                # Needle use for air psuhing
                {"ParameterId": 41, "Value": "Needle 3", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1902,
            "TrialNumber": 1,
            "ParameterValues": [
                # Needle use for transfer volumetricaly
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1902,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1904,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {  ### change solvent if needed
                            "ArticleId": 194,
                            "Amount": 1,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1905,
            "TrialNumber": 2,
            "ParameterValues": [
                # Shake
                {"ParameterId": 11, "Value": "500", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1907,
            "TrialNumber": 2,
            "ParameterValues": [
                # Instrument method
                {"ParameterId": 36, "Value": "Method_Agilent_102423", "Unit": 2600},
                # Processing Method
                {"ParameterId": 37, "Value": "N-alkylation_SWING_SP", "Unit": 2600},
                # Time
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
    ]
    exp_list = []

    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []
    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 41,
        "Experiments": exp_list,
    }

    return create_run


def Swing_SP_thermal_reaction(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Dispense Tool Gravimetric"][i] == "GDU-PFD" or data["Dispense Tool Gravimetric"][i] == "GDU-S" or data["Dispense Tool Gravimetric"][i] == "GDU-S"

        ):
            data.loc[i, "Node"] = 1975
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002

        elif data["Dispense Tool Gravimetric"][i] == "GDU-V":
            data.loc[i, "Node"] = 1980
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "13196261-41A2-42DB-9F79-82D175396798"
            data.loc[i, "Unit"] = 1002
        
        elif (
            data["Property"][i] == "solvent A"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1978
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 1959
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1981
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801


    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

 
    data.to_csv("C:/Users/TERRIEAI/OneDrive - KAUST/Files_generated_python/Data_createjson.csv")

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        {
            "NodeId": 1983,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing duration
                {"ParameterId": 10, "Value": "2", "Unit": 601},
                # Mixing speed
                {"ParameterId": 11, "Value": "500", "Unit": 1601},
            ],
        },
       
        {
            "NodeId": 1960,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {
                            "ArticleId": 5,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {"NodeId": 1960,
            "TrialNumber": 0,
            "ParameterValues": [
               
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
   
         
        {
            "NodeId": 1963,
            "TrialNumber": 1,
            "Articles": [
                {
                    "ArticleId": 128,
                    "Assemblies": [
                        {  #### Change solvent if needed
                            "ArticleId": 194,
                            "Amount": 1.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        {
            "NodeId": 1964,
            "TrialNumber": 1,
            "ParameterValues": [
                # Air push volume
                {"ParameterId": 43, "Value": "10", "Unit": 801},
                # Needle use for air psuhing
                {"ParameterId": 41, "Value": "Needle 3", "Unit": 2600},
            ],
        },
        {"NodeId": 1965,
            "TrialNumber": 1,
            "ParameterValues": [
               
                # Needle use for transfer
                {"ParameterId": 41, "Value": "Needle 2", "Unit": 2600},
            ],
        },
        {
            "NodeId": 1965,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {
                            "ArticleId": 128,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
        
          {  "NodeId": 1967,
            "TrialNumber": 2,
            "Articles": [
                {
                    "ArticleId": 126,
                    "Assemblies": [
                        {  #### Change solvent if needed
                            "ArticleId": 194,
                            "Amount": 0.5,
                            "Unit": 801,
                        },{  #### Change solvent if needed
                            "ArticleId": 197,
                            "Amount": 0.5,
                            "Unit": 801,
                        }
                    ],
                }
            ],
        },
         {
            "NodeId": 1968,
            "TrialNumber": 2,
            "ParameterValues": [
                # Mixing duration
                {"ParameterId": 10, "Value": "2", "Unit": 601},
                # Mixing speed
                {"ParameterId": 11, "Value": "500", "Unit": 1601},
            ],
        },
        {
            "NodeId": 1970,
            "TrialNumber": 2,
            "ParameterValues": [
                 # Instrument Method
                {"ParameterId": 36, "Value": "Method_Agilent_102423", "Unit": 2600},
                # Processing method
                {"ParameterId": 37, "Value": "N-alkylation_SWING_SP", "Unit": 2600},
                # Volume injection
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
    ]

    ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                #### 4 ml vial #####
                "Articles": [{"ArticleId": 5, "Assemblies": []}],
            }

            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 1959 or b == 1978 or b==1981 :
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )
            # dispense gravimetrically
            else:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Mass", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Mass": "Amount"})
                    .to_dict("records")
                )

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 1959 or b == 1978 or b==1981:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
        heating_node = {
            "NodeId": 1982,
            "TrialNumber": 0,
            "ParameterValues": [
                # Mixing duration
                {"ParameterId": 10, "Value": data["time (h)"][i], "Unit": 602},
                # Mixing speed
                {"ParameterId": 11, "Value": "500", "Unit": 1601},
                # Mixing temperature
                {"ParameterId": 12, "Value": data["Temperature (C )"][i], "Unit": 201},
            ],
        }

    

        exp_list[i]["Nodes"].append(heating_node)
        

    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 44,
        "Experiments": exp_list,
    }

    return create_run

def node_SWING_SP_test_UPLC_54WP(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    for i in range(0, len(data)):
        if (
            data["Property"][i] == "solvent A"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 2143
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        elif (
            data["Property"][i] == "Internal standard"
            and data["Dispense Tool Volumetric"][i] == "4NH"
        ):
            data.loc[i, "Node"] = 2143
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
        else:
            data.loc[i, "Node"] = 1981
            data.loc[
                i, "AttributeDefinitionCstId"
            ] = "A3662EB7-5735-4CE1-BF41-FFD4160DB057"
            data.loc[i, "Unit"] = 801
    
    # convert specific columns in int to allow serialization json
    convert = {"ArtId": int, "Node": int, "Unit": int}
    data = data.astype(convert)

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
        
        {
            "NodeId": 2145,
            "TrialNumber": 0,
            "ParameterValues": [
                # Shake
                {"ParameterId": 11, "Value": "150", "Unit": 1601},
            ],
        },
        {
            "NodeId": 2144,
            "TrialNumber": 0,
            "ParameterValues": [
                 # Instrument Method
                {"ParameterId": 36, "Value": "UV-MS Test method Full scan 2 mins", "Unit": 2600},
                # Processing method
                {"ParameterId": 37, "Value": "UV_MS 2 mins_Caf ISD", "Unit": 2600},
                # Volume injection
                {"ParameterId": 38, "Value": "3", "Unit": 802},
            ],
        },
        
    ]
   ## Create the json file with value input by the user
    # add all experiement and nodes
    exp_list = []
    list_nodes = list(data["Node"].unique())
    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []

        for j in range(0, len(data["Node"].unique())):
            y = {
                "NodeId": list_nodes[j],
                "TrialNumber": 0,
                #### 2 ml vial #####
                "Articles": [{"ArticleId": 126, "Assemblies": []}],
            }

            exp_list[i]["Nodes"].append(y)

    # add the Article and Assemblies
    for i in range(0, len(data["Experiment No."].unique())):
        for j in range(0, len(data["Node"].unique())):
            a = -exp_list[i]["Id"]
            b = exp_list[i]["Nodes"][j]["NodeId"]
            test = data.loc[(data["Experiment No."] == a) & (data["Node"] == b)]
            # dispense volumetrically
            if b == 2143 :
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Volume", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Volume": "Amount"})
                    .to_dict("records")
                )
            # dispense gravimetrically
            else:
                exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"].extend(
                    test[["ArtId", "Mass", "Unit"]]
                    .rename(columns={"ArtId": "ArticleId", "Mass": "Amount"})
                    .to_dict("records")
                )

            for k in range(
                0, len(exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"])
            ):
                c = exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k]["ArticleId"]
                test2 = data.loc[
                    (data["Experiment No."] == a)
                    & (data["Node"] == b)
                    & (data["ArtId"] == c)
                ]
                if b == 2143:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Volumetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
                else:
                    exp_list[i]["Nodes"][j]["Articles"][0]["Assemblies"][k][
                        "AssemblyInstructions"
                    ] = [
                        {
                            "AttributeDefinitionCstId": test2[
                                "AttributeDefinitionCstId"
                            ].values[0],
                            "Value": {
                                "String": test2["Dispense Tool Gravimetric"].values[0]
                            },
                            "Unit": 2600,
                        }
                    ]
  

    


    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 45,
        "Experiments": exp_list,
    }

    return create_run



def node_SWING_SP_testPhoto(data, label):
    index_nul = data[data["CAS Number"] == "-"].index
    data.drop(index_nul, inplace=True)
    data = data.reset_index()

    ### Create the json file ###

    ## Create the list of the node with default values

    list_node_default = [
         {
            "NodeId": 2149,
            "TrialNumber": 0,
            "ParameterValues": [
                # Temperature
                {"ParameterId": 1, "Value": "25", "Unit": 201},
                # reaction speed
                {"ParameterId": 2, "Value": "150", "Unit": 1601},
                # Time
                {"ParameterId": 3, "Value":"5", "Unit": 601},
                # LED intensity
                {"ParameterId": 46, "Value": "1", "Unit": 2200},
            ],
        },
        {
            "NodeId": 2148,
            "TrialNumber": 0,
            "ParameterValues": [
                # Wavelength
                {"ParameterId": 47, "Value": "395nm", "Unit": 2600},
                
            ],
        },
    ]
    exp_list = []

    len(data["Experiment No."].unique())
    for i in range(0, len(data["Experiment No."].unique())):
        x = {"Id": -data["Experiment No."][i]}
        exp_list.append(x)
        exp_list[i]["Nodes"] = []
    # Merge the node with default parameters and others node
    for i in range(0, len(data["Experiment No."].unique())):
        exp_list[i]["Nodes"].extend(list_node_default)

    # Create the final json file
    create_run = {
        "PlatformId": 1,
        "Label": label,
        "WorkflowId": 46,
        "Experiments": exp_list,
    }

    return create_run