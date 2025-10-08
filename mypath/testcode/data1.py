import qlib
from qlib.contrib.data.handler import Alpha158

data_handler_config = {
    "start_time": "2025-01-01",
    "end_time": "2025-09-01",
    "fit_start_time": "2025-02-01",
    "fit_end_time": "2025-04-01",
    "instruments": "csi300",
}

if __name__ == "__main__":
    qlib.init()
    h = Alpha158(**data_handler_config)

    # get all the columns of the data
    print(h.get_cols())

    # fetch all the labels
    print(h.fetch(col_set="label"))

    # fetch all the features
    print(h.fetch(col_set="feature"))