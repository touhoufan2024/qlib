# all ipynb file
```
./examples/benchmarks/TRA/Reports.ipynb
./examples/rl/simple_example.ipynb
./examples/workflow_by_code.ipynb
./examples/tutorial/detailed_workflow.ipynb

```


market = "csi300"  股票池: 表示仅使用 沪深300 里的 成分股

benchmark = "SH000300"  性能基准: 表示沪深300指数


example_df = dataset.prepare("train")
print(example_df.head())


# 常用命令
```
mlflow ui
```


# workflow 步骤
0. 准备 task,  model 和 dateset
1. 初始化qlib;初始化 model 和 dataset
2. 准备 port_analysis_config
3. 开始 experiment
    model.fit
    recorder


# record template类

模板类 可以 以一种 特定格式 生成 回测 结果


SignalRecord: This class generates the prediction results of the model.

SigAnaRecord: This class generates the IC, ICIR, Rank IC and Rank ICIR of the model.

PortAnaRecord: This class generates the results of backtest. The detailed information about backtest as well as the available strategy, users can refer to Strategy and Backtest.



# example

## benchmarks
工作流 yaml 文件
## benchmarks_dynamic


## data_demo
数据模块

## highfreq
高频数据下进行 预测

## hyperparameter
超参数优化, 用于优化模型

## model_interpreter
简单的 模型训练

## model_rolling


## nested_decision_execution

嵌套策略执行

## online_srv

在线 多任务

## orderbook_data
支持非固定频率数据


## portfolio

投资组合优化策略, 优于topk

## rl

强化学习example ipynb

## rl_order_execution
订单执行强化学习示例


## rolling_process_data
## run_all_model.py
## tutorial
## workflow_by_code.ipynb
## workflow_by_code.py


# 代码
global record
R: QlibRecorderWrapper = RecorderWrapper()
RecorderWrapper 的作用是记录、存储和管理实验中的数据和指标，包括：

实验配置记录:比如实验使用了什么因子，数据集是哪一年到哪一年，因子的形态是什么等等。
模型训练记录
记录训练过程:例如训练中模型的超参数、损失函数变化，以及模型权重（保存了 checkpoint）。
交易和回测记录
每一笔交易的详细记录，交易日期、买入的股票、省略股份，以及回测的最终结果：例如收益率、夏普比率。
如果在一天内训练了多个模型，可以通过 RecorderWrapper 同时对多个实验的结果进行对比分析。


R.start() 仅能被 with 调用
这个方法 最终 会 调用到 mlflow 这个 类

R.start
    QlibRecorder.start
        QlibRecorder.start_exp
            ExpManager.start_exp
                ExpManager._start_exp
                    Experiment.start
                        MLflowRecorder.start_run   (active_recorder)
                            return mlflow.start_run  (qlib/workflow/recorder.py)

最终 返回一个 run 对象, 这个对象被保存在 QlibRecorder 里面, run 是 MLflowExperiment 对象


R.get_exp 获取 Experiment


model.fit 方法
继承Model 的 子类 都应该实现 这个方法
        
dataset 使用 task['dataset']初始化, 所以里面没有包含 数据的具体信息, 等于是 只有 这个列表内的信息

真正的股票信息 通过 qlib.init 初始化, 因子的计算 应该是 使用


# data
下载的数据包里面已经包含了 因子了, 所以 model 训练的时候 不需要重复计算


# model

使用的model 来自于 sklearn

coef 和 intercept 这两个 就是 linear model 训练出来的结果


BaseModel
    Model
        ModelFT
        other model class
    RiskNodel


Model 是 "Learnable Models"
规定了两个方法 fit, predict

ModelFT 是 可 微调 的 model, "Model (F)ine(t)unable"

other class 是包装了 来自于 sklearn 的model
