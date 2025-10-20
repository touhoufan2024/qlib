#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT License.
import qlib
from qlib.constant import REG_CN
from qlib.utils import init_instance_by_config, flatten_dict
from qlib.workflow import R
from qlib.workflow.record_temp import SignalRecord, PortAnaRecord, SigAnaRecord
from qlib.tests.data import GetData
from qlib.tests.config import CSI300_BENCH, CSI300_GBDT_TASK

market = "csi300"
benchmark = "SH000300"

data_handler_config = {
    "start_time": "2008-01-01",
    "end_time": "2020-08-01",
    "fit_start_time": "2008-01-01",
    "fit_end_time": "2014-12-31",
    "instruments": market,  # 确保市场变量是已定义或适当引用
    "infer_processors": [
        {
            "class": "RobustZScoreNorm",
            "kwargs": {
                "fields_group": "feature",
                "clip_outlier": True
            }
        },
        {
            "class": "Fillna",
            "kwargs": {
                "fields_group": "feature"
            }
        }
    ],
    "learn_processors": [
        {
            "class": "DropnaLabel"
        },
        {
            "class": "CSRankNorm",
            "kwargs": {
                "fields_group": "label"
            }
        }
    ]
}

port_analysis_config = {
    "strategy": {
        "class": "TopkDropoutStrategy",
        "module_path": "qlib.contrib.strategy",
        "kwargs": {
            "signal": "<PRED>",  # 确保 <PRED> 适合于您代码中的 signals
            "topk": 50,
            "n_drop": 5
        }
    },
    "backtest": {
        "start_time": "2017-01-01",
        "end_time": "2020-08-01",
        "account": 100000000,
        "benchmark": benchmark,  # 确保 benchmark 变量是已定义或适当引用
        "exchange_kwargs": {
            "limit_threshold": 0.095,
            "deal_price": "close",
            "open_cost": 0.0005,
            "close_cost": 0.0015,
            "min_cost": 5
        }
    }
}

task = {
    "model": {
        "class": "LinearModel",
        "module_path": "qlib.contrib.model.linear",
        "kwargs": {
            "estimator": "ols"
        }
    },
    "dataset": {
        "class": "DatasetH",
        "module_path": "qlib.data.dataset",
        "kwargs": {
            "handler": {
                "class": "Alpha158",
                "module_path": "qlib.contrib.data.handler",
                "kwargs": data_handler_config  # 引用之前定义的 data_handler_config
            },
            "segments": {
                "train": ["2008-01-01", "2014-12-31"],
                "valid": ["2015-01-01", "2016-12-31"],
                "test": ["2017-01-01", "2020-08-01"]
            }
        }
    },
    "record": [
        {
            "class": "SignalRecord",
            "module_path": "qlib.workflow.record_temp",
            "kwargs": {
                "model": "<MODEL>",  # 确保 <MODEL> 被替换为实际模型变量
                "dataset": "<DATASET>"  # 确保 <DATASET> 被替换为实际数据集变量
            }
        },
        {
            "class": "SigAnaRecord",
            "module_path": "qlib.workflow.record_temp",
            "kwargs": {
                "ana_long_short": True,
                "ann_scaler": 252
            }
        },
        {
            "class": "PortAnaRecord",
            "module_path": "qlib.workflow.record_temp",
            "kwargs": {
                "config": port_analysis_config  # 引用之前定义的 port_analysis_config
            }
        }
    ]
}



# use default data
provider_uri = "~/.qlib/qlib_data/cn_data"  # target_dir
qlib.init(provider_uri=provider_uri, region=REG_CN)
# model initialization
model = init_instance_by_config(task["model"])
dataset = init_instance_by_config(task["dataset"])

exps = R.list_experiments()

for a, b in exps.items():
    print(a)
    print(b)

exit(0)

# start exp
with R.start(experiment_name="workflow_linear_Alpha158B"):
    R.log_params(**flatten_dict(task))
    model.fit(dataset)
    R.save_objects(**{"params.pkl": model})

    # prediction
    recorder = R.get_recorder()
    sr = SignalRecord(model, dataset, recorder)
    sr.generate()

    # Signal Analysis
    sar = SigAnaRecord(recorder)
    sar.generate()

    # backtest. If users want to use backtest based on their own prediction,
    # please refer to https://qlib.readthedocs.io/en/latest/component/recorder.html#record-template.
    par = PortAnaRecord(recorder, port_analysis_config, "day")
    par.generate()