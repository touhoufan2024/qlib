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
