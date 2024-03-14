import pandas as pd


def amount(all_att_DOE):
    try:
        all_att_DOE[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "ChemBeads Factor",
                "Volume",
            ]
        ] = all_att_DOE[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "ChemBeads Factor",
                "Volume"
            ]
        ].apply(
            pd.to_numeric
        )

        all_att_DOE["Dispense Tool Volumetric"].fillna("", inplace=True)
        all_att_DOE["Molar Concentration"].fillna("", inplace=True)

        for i in range(0, len(all_att_DOE)):
            if (
                all_att_DOE["Dispense Tool Volumetric"][i] == ""
                and all_att_DOE["CAS Number"][i] != "-"
            ):
                if all_att_DOE["Dispense Tool Gravimetric"][i] == "GDU-S" or all_att_DOE["Dispense Tool Gravimetric"][i] == "GDU-PFD":
                    all_att_DOE.loc[i, "Mass"] = round(
                        all_att_DOE["Molar mass"][i]
                        * 1000
                        * all_att_DOE["reaction scale (mmol)"][i]
                        * all_att_DOE["Equivalent"][i]
                        * all_att_DOE["ChemBeads Factor"][i],
                        3,
                    )

                else:
                    all_att_DOE.loc[i, "Mass"] = round(
                        all_att_DOE["Molar mass"][i]
                        * 1000
                        * all_att_DOE["reaction scale (mmol)"][i]
                        * all_att_DOE["Equivalent"][i],
                        3,
                    )
            else:
                continue

        for i in range(0, len(all_att_DOE)):
            if all_att_DOE["Property"].str.match('solvent')[i]==True:
                continue
            elif all_att_DOE["Molar Concentration"][i] != "":
                all_att_DOE.loc[i, "Volume"] = (
                    all_att_DOE["reaction scale (mmol)"][i]
                    * all_att_DOE["Equivalent"][i]
                    * (1 / all_att_DOE["Molar Concentration"][i]),
                )
            else:
                all_att_DOE.loc[i, "Volume"] = (
                    (1 / (all_att_DOE["Density"][i] * 0.001))
                    * all_att_DOE["Molar mass"][i]
                    * 1000
                    * all_att_DOE["reaction scale (mmol)"][i]
                    * 0.001
                    * all_att_DOE["Equivalent"][i],
                )
    except:
        all_att_DOE[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "Volume"
            ]
        ] = all_att_DOE[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "Volume"
            ]
        ].apply(
            pd.to_numeric
        )

        all_att_DOE["Dispense Tool Volumetric"].fillna("", inplace=True)
        all_att_DOE["Molar Concentration"].fillna("", inplace=True)

        for i in range(0, len(all_att_DOE)):
            if (
                all_att_DOE["Dispense Tool Volumetric"][i] == ""
                and all_att_DOE["CAS Number"][i] != "-"
            ):
                if all_att_DOE["Dispense Tool Gravimetric"][i] == "GDU-S":
                    all_att_DOE.loc[i, "Mass"] = round(
                        all_att_DOE["Molar mass"][i]
                        * 1000
                        * all_att_DOE["reaction scale (mmol)"][i]
                        * all_att_DOE["Equivalent"][i],
                        3,
                    )

                else:
                    all_att_DOE.loc[i, "Mass"] = round(
                        all_att_DOE["Molar mass"][i]
                        * 1000
                        * all_att_DOE["reaction scale (mmol)"][i]
                        * all_att_DOE["Equivalent"][i],
                        3,
                    )
            else:
                continue

        for i in range(0, len(all_att_DOE)):
            if all_att_DOE["Property"].str.match('solvent')[i]==True:
                continue
            elif all_att_DOE["Molar Concentration"][i] != "":
                all_att_DOE.loc[i, "Volume"] = (
                    all_att_DOE["reaction scale (mmol)"][i]
                    * all_att_DOE["Equivalent"][i]
                    * (1 / all_att_DOE["Molar Concentration"][i]),
                )
            else:
                all_att_DOE.loc[i, "Volume"] = (
                    (1 / (all_att_DOE["Density"][i] * 0.001))
                    * all_att_DOE["Molar mass"][i]
                    * 1000
                    * all_att_DOE["reaction scale (mmol)"][i]
                    * 0.001
                    * all_att_DOE["Equivalent"][i],
                )

    return all_att_DOE
