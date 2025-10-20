
import qlib
from qlib.constant import REG_CN
from qlib.utils import init_instance_by_config, flatten_dict
from qlib.workflow import R
from qlib.workflow.record_temp import SignalRecord, PortAnaRecord, SigAnaRecord
from qlib.tests.data import GetData
from qlib.tests.config import CSI300_BENCH, CSI300_GBDT_TASK


provider_uri = "~/.qlib/qlib_data/cn_data"  # target_dir
qlib.init(provider_uri=provider_uri, region=REG_CN)



exps = R.list_experiments()

for a, b in exps.items():
    print(a)
    print(b)

exp = R.get_exp(experiment_name="lgbm", create=False)
recorder = exp.get_recorder(recorder_id="4d360e5bf743427d8b3388117ec3db07")


pred_df = recorder.load_object("pred.pkl")
ic_data = recorder.load_object("sig_analysis/ic.pkl")
ric_data = recorder.load_object("sig_analysis/ric.pkl")
indicators_normal_1day_obj = recorder.load_object("portfolio_analysis/indicators_normal_1day_obj.pkl")
report_normal_1day_df = recorder.load_object("portfolio_analysis/report_normal_1day.pkl")
positions_normal_1day = recorder.load_object("portfolio_analysis/positions_normal_1day.pkl")
indicators_normal_1day = recorder.load_object("portfolio_analysis/indicators_normal_1day.pkl") # 注意这个和上面的 _obj 区分开
port_analysis_1day_df = recorder.load_object("portfolio_analysis/port_analysis_1day.pkl")
indicator_analysis_1day_df = recorder.load_object("portfolio_analysis/indicator_analysis_1day.pkl")
label_df = recorder.load_object("label.pkl")
params_data = recorder.load_object("params.pkl")