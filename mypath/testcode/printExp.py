
import os
import qlib
import pandas as pd
from qlib.constant import REG_CN
from qlib.utils import init_instance_by_config, flatten_dict
from qlib.workflow import R
from qlib.workflow.record_temp import SignalRecord, PortAnaRecord, SigAnaRecord
from qlib.tests.data import GetData
from qlib.tests.config import CSI300_BENCH, CSI300_GBDT_TASK

from qlib.contrib.report import analysis_model, analysis_position

provider_uri = "~/.qlib/qlib_data/cn_data"  # target_dir
qlib.init(provider_uri=provider_uri, region=REG_CN)

class Task:
    def __init__(self, recoder):
        self.pred_df = recorder.load_object("pred.pkl")
        self.ic_data = recorder.load_object("sig_analysis/ic.pkl")
        self.ric_data = recorder.load_object("sig_analysis/ric.pkl")
        self.indicators_normal_1day_obj = recorder.load_object("portfolio_analysis/indicators_normal_1day_obj.pkl")
        self.report_normal_1day_df = recorder.load_object("portfolio_analysis/report_normal_1day.pkl")
        self.positions_normal_1day = recorder.load_object("portfolio_analysis/positions_normal_1day.pkl")
        self.indicators_normal_1day = recorder.load_object("portfolio_analysis/indicators_normal_1day.pkl") # 注意这个和上面的 _obj 区分开
        self.port_analysis_1day_df = recorder.load_object("portfolio_analysis/port_analysis_1day.pkl")
        self.indicator_analysis_1day_df = recorder.load_object("portfolio_analysis/indicator_analysis_1day.pkl")
        self.label_df = recorder.load_object("label.pkl")
        self.params_data = recorder.load_object("params.pkl")

        self.pred_label = pd.concat([self.label_df, self.pred_df], axis=1, sort=True).reindex(self.label_df.index)
        self.pred_label.columns = ['label', 'score'] 

        self.output_dir="myanalysis"


    def SaveFigures(self, fig_list, prefix):
        """
        统一处理图表保存逻辑
        :param fig_list: 图表列表
        :param prefix: 文件名前缀（用于区分不同类型图表）
        """
        # 创建输出目录（如果不存在）
        os.makedirs(self.output_dir, exist_ok=True)
        
        for i, fig in enumerate(fig_list):
            # 统一文件名格式
            base_name = f"{prefix}_{i:02d}"
            img_path = os.path.join(self.output_dir, f"{base_name}.png")
            print(f"保存图片: {img_path}")
            
            # 尝试保存为图片（更高质量展示）
            fig.write_image(
                img_path,
                format="png",
                width=1200,
                height=800,
                scale=2  # 高清缩放
            )

    def SaveAll(self):
        self.report_figs = analysis_position.report_graph(self.report_normal_1day_df, show_notebook=False)
        self.SaveFigures(self.report_figs, "report")
        
        self.risk_figs = analysis_position.risk_analysis_graph(self.port_analysis_1day_df, self.report_normal_1day_df, show_notebook=False)
        self.SaveFigures(self.risk_figs, "risk_analysis")
        
        self.ic_figs = analysis_position.score_ic_graph(self.pred_label, show_notebook=False)
        self.SaveFigures(self.ic_figs, "score_ic")

        self.model_figs = analysis_model.model_performance_graph(self.pred_label, show_notebook=False)
        self.SaveFigures(self.model_figs, "model_performance")


def GetRecorder(en, rid):
    exp = R.get_exp(experiment_name=en, create=False)
    recorder = exp.get_recorder(recorder_id=rid)
    return recorder


def PrintAllExps():
    exps = R.list_experiments()

    for a, b in exps.items():
        print(a)
        print(b)

if __name__ == "__main__":
    PrintAllExps()
    en = "lgbm"
    rid = "056d80acae6e4afa87236165ee10c10c"
    recorder = GetRecorder(en, rid)
    task = Task(recorder)
    task.SaveAll()