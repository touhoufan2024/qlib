import os
import qlib
import pandas as pd
import argparse
import webbrowser
import plotly.io as pio

from qlib.workflow import R
from qlib.contrib.report import analysis_model, analysis_position
from tabulate import tabulate

# Move these inside __main__ and add multiprocessing protection
if __name__ == "__main__":
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='QLib Experiment Test Report Tool')
    parser.add_argument('--exp-name', type=str, required=True,
                       help='Exp Name, e.g. lstm_Alpha158')
    
    args = parser.parse_args()
    
    # 参数验证
    if not args.exp_name or args.exp_name.strip() == "":
        parser.error("Exp Name cannot be empty")
    
    experiment_name = args.exp_name.strip()
    
    # Suppress gym warnings
    import warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning, message='.*Gym.*')

    qlib.init(provider_uri="~/.qlib/qlib_data/cn_data", region="cn")
    
    # 1. 先验证实验是否存在
    try:
        exp = R.get_exp(experiment_name=experiment_name, create=False)
    except RecorderInitializationError as e:
        raise ValueError(f"Experiment {experiment_name} not found!") from e
    
    # 2. 交互式选择记录器
    recorders = exp.list_recorders()
    recorder_list = list(recorders.items())
    
    # 生成带序号的表格数据
    table_data = [
        [idx, rid[:8]+"...", r.info.get('name', 'N/A'), r.status] 
        for idx, (rid, r) in enumerate(recorder_list, 1)
    ]
    
    # 打印格式化表格
    print(tabulate(table_data, 
                   headers=["No.", "ID(abbr)", "Name", "Status"], 
                   tablefmt="grid",
                   maxcolwidths=[None, 10, 20, None]))
    
    # 用户交互选择
    max_retry = 3  # 添加最大重试次数
    retry_count = 0
    
    while retry_count < max_retry:
        try:
            select = int(input("\n请输入要选择的记录器序号 (1-{}): ".format(len(recorder_list))))
            if 1 <= select <= len(recorder_list):
                selected_rid = recorder_list[select-1][0]
                recorder = exp.get_recorder(recorder_id=selected_rid)
                break
            print(f"输入超出范围，剩余重试次数：{max_retry - retry_count - 1}")
        except ValueError:
            print(f"请输入1-{len(recorder_list)}之间的整数，剩余重试次数：{max_retry - retry_count - 1}")
        retry_count += 1
    else:
        raise RuntimeError("超过最大重试次数，程序退出")
    
    print(recorder.info)
    
    # 加载记录器存储的结果
    label_df = recorder.load_object("label.pkl")
    pred_df = recorder.load_object("pred.pkl")
    report_normal_df = recorder.load_object("portfolio_analysis/report_normal_1day.pkl")
    positions = recorder.load_object("portfolio_analysis/positions_normal_1day.pkl")
    analysis_df = recorder.load_object("portfolio_analysis/port_analysis_1day.pkl")
    
    pred_label = pd.concat([label_df, pred_df], axis=1, sort=True).reindex(label_df.index)
    pred_label.columns = ['label', 'score'] 
    
    print("Merged columns:", pred_label.columns)
    print("data load done!")
    
    # 图表处理工具函数
    def save_figures(fig_list, prefix, all_figures, output_dir="analysis_figures"):
        """
        统一处理图表保存逻辑
        :param fig_list: 图表列表
        :param prefix: 文件名前缀（用于区分不同类型图表）
        :param all_figures: 收集所有图表的列表（用于后续合并）
        :param output_dir: 输出目录
        """
        # 创建输出目录（如果不存在）
        os.makedirs(output_dir, exist_ok=True)
        
        for i, fig in enumerate(fig_list):
            # 统一文件名格式
            base_name = f"{prefix}_{i:02d}"
            img_path = os.path.join(output_dir, f"{base_name}.png")
            html_path = os.path.join(output_dir, f"{base_name}.html")
            
            try:
                # 尝试保存为图片（更高质量展示）
                fig.write_image(
                    img_path,
                    format="png",
                    width=1200,
                    height=800,
                    scale=2  # 高清缩放
                )
                print(f"成功保存图片: {img_path}")
            except Exception as e:
                # 保存图片失败时转为保存HTML
                fig.write_html(html_path)
                print(f"图片保存失败 [{e}]，已转为保存HTML: {html_path}")
            
            # 将图表添加到总列表用于合并
            all_figures.append((prefix, fig))


    # 初始化图表列表
    all_figures = []
    output_dir = "analysis_figures"  # 统一输出目录

    # 1. 生成并保存Report图表
    print("生成Report图表...")
    report_figs = analysis_position.report_graph(report_normal_df, show_notebook=False)
    save_figures(report_figs, "report", all_figures, output_dir)

    # 2. 生成并保存Risk analysis图表
    print("生成风险分析图表...")
    risk_figs = analysis_position.risk_analysis_graph(analysis_df, report_normal_df, show_notebook=False)
    save_figures(risk_figs, "risk_analysis", all_figures, output_dir)

    # 3. 生成并保存IC analysis图表
    print("生成IC分析图表...")
    ic_figs = analysis_position.score_ic_graph(pred_label, show_notebook=False)
    save_figures(ic_figs, "score_ic", all_figures, output_dir)

    # 4. 生成并保存Model analysis图表
    print("生成模型性能图表...")
    model_figs = analysis_model.model_performance_graph(pred_label, show_notebook=False)
    save_figures(model_figs, "model_performance", all_figures, output_dir)


    # 创建合并所有图表的HTML（修复CSS转义问题）
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>量化分析图表汇总</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 1400px; margin: 0 auto; padding: 20px; }}
            .section {{ margin-bottom: 60px; }}
            .section h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .figure-container {{ margin: 30px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 15px; border-radius: 8px; }}
            .header {{ text-align: center; margin: 40px 0; }}
            .header h1 {{ color: #2c3e50; }}
            .footer {{ text-align: center; margin-top: 80px; color: #7f8c8d; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>量化策略分析图表汇总</h1>
            <p>生成时间: {generate_time}</p>
        </div>
    """

    # 添加生成时间（此时只有 {generate_time} 是需要替换的变量，其他 {} 已转义）
    from datetime import datetime
    html_content = html_content.format(generate_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 按图表类型分组添加
    current_group = None
    for group_name, fig in all_figures:
        if group_name != current_group:
            # 新分组开始
            if current_group is not None:
                html_content += "</div>"  # 关闭上一个分组
            html_content += f'<div class="section"><h2>{group_name.replace("_", " ").title()}</h2>'
            current_group = group_name
        
        # 添加图表
        fig_div = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
        html_content += f'<div class="figure-container">{fig_div}</div>'

    # 关闭最后一个分组和页面
    html_content += """
        </div>
        <div class="footer">
            <p>分析图表由QLib生成 | 更多信息请参考QLib文档</p>
        </div>
    </body>
    </html>
    """

    # 保存合并的HTML文件
    combined_html_path = os.path.join(output_dir, "all_analysis_figures.html")
    with open(combined_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 在浏览器中打开合并的HTML文件
    try:
        webbrowser.open(f"file://{os.path.abspath(combined_html_path)}")
        print(f"所有图表已成功生成并合并到: {os.path.abspath(combined_html_path)}")
        print(f"单独图表文件保存在: {os.path.abspath(output_dir)}")
    except Exception as e:
        print(f"图表已生成，但自动打开浏览器失败: {e}")
        print(f"请手动打开文件查看: {os.path.abspath(combined_html_path)}")