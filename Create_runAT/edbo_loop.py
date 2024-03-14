import pandas as pd
from edbo.utils import Data
from edbo.bro import BO_express


def create_chemical_space(csv_cs, path, label, batch_size):
    csv_cs = csv_cs.dropna(axis=1, how="all")
    dft_columns = csv_cs.loc[:, csv_cs.columns.str.endswith("dft")]
    columns_name_dft = dft_columns.columns
    print(columns_name_dft)
    # Load DFT descriptor CSV files computed with auto-qchem using pandas
    # Instantiate a Data object

    # Use Data.drop method to drop descriptors containing some unwanted keywords
    dft = {}
    dictionary = {}
    for i in columns_name_dft:
        dictionary[i] = Data(pd.read_csv(path + i + ".csv"))
        dictionary[i].drop(
            [
                "file_name" "entry",
                "vibration",
                "correlation",
                "Rydberg",
                "correction",
                "atom_number",
                "E-M_angle",
                "MEAN",
                "MAXG",
                "STDEV",
            ]
        )
        # External descriptor matrices override specified encoding
        dft[i] = dictionary[i].data

    # Parameters in reaction space
    components = {}
    for i in range(0, len(csv_cs.columns)):
        if csv_cs.columns[i].endswith("dft") == True:
            components[csv_cs.columns[i]] = "DFT"
        else:
            my_list = list(csv_cs[csv_cs.columns[i]])
            new_list = [item for item in my_list if str(item) != "nan"]
            components[csv_cs.columns[i]] = new_list

    # Encodings - if not specified EDBO will automatically use OHE

    encoding = {}
    numerical_cols = list(
        csv_cs.select_dtypes(
            include=["int16", "int32", "int64", "float16", "float32", "float64"]
        )
    )
    for i in range(0, len(numerical_cols)):
        encoding[numerical_cols[i]] = "numeric"  # Numerical encoding

    # BO object

    bo = BO_express(
        components,  # Reaction parameters
        encoding=encoding,  # Encoding specification
        descriptor_matrices=dft,  # DFT descriptors
        acquisition_function="EI",  # Use expectation value of improvement
        init_method="rand",  # Use random initialization
        batch_size=batch_size,  # 10 experiments per round
        target="yield",
    )  # Optimize yield

    # Initialization

    bo.init_sample(seed=0)  # Initialize
    bo.export_proposed("init.csv")  # Export design to a CSV file
    bo.save(label)

    return bo.get_experiments()


def bayesian_optimizer(csv, label, export_path):
    bo = BO_express()
    bo.load(label)
    bo.add_results(csv)
    bo.run()
    bo.export_proposed(export_path)
    return bo.get_experiments()
