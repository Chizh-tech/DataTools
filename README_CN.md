# DataTools

一个基于 Streamlit 的数据分析工具包，支持上传数据集、可视化数据、为图片标注边界框，并通过 OpenAI 获取 AI 驱动的分析洞察。

---

## 功能特性

| 模块 | 功能 |
|---|---|
| **Data Processor（数据处理）** | 上传 CSV / Excel 文件，预览数据，查看汇总统计 |
| **Plot Generator（绘图生成）** | 柱状图、折线图、散点图、直方图 |
| **Image Tools（图像工具）** | 上传图片、绘制带标签的边界框、下载标注结果 |
| **AI Evaluator（AI 评估）** | 描述性统计、相关矩阵、OpenAI 聊天集成 |

---

## 项目结构

```
DataTools/
├── app.py               # Streamlit 应用入口
├── requirements.txt     # Python 依赖
├── src/
│   ├── __init__.py
│   ├── data_processor.py   # CSV / Excel 加载与汇总
│   ├── plot_generator.py   # Matplotlib 图表辅助函数
│   ├── image_tools.py      # 基于 PIL 的图像工具
│   └── ai_evaluator.py     # 统计分析 + OpenAI 封装
└── tests/
    ├── __init__.py
    ├── test_data_processor.py
    ├── test_plot_generator.py
    ├── test_image_tools.py
    └── test_ai_evaluator.py
```

---

## 安装

```bash
pip install -r requirements.txt
```

---

## 运行应用

```bash
streamlit run app.py
```

应用将在浏览器中打开：`http://localhost:8501`。

---

## 使用说明

### Data Processor（数据处理）
1. 在侧边栏选择 **Data Processor**。
2. 上传 `.csv`、`.xlsx` 或 `.xls` 文件。
3. 预览前 50 行数据，并展开 **Dataset Summary** 区域查看数据类型、缺失值和描述性统计。

### Plot Generator（绘图生成）
1. 先上传数据集（Data Processor 标签页）。
2. 选择 **Plot Generator**，选择图表类型并指定列。
3. 点击 **Generate** 渲染图表。

### Image Tools（图像工具）
1. 选择 **Image Tools** 并上传 PNG / JPEG 图片。
2. 以 `x0,y0,x1,y1` 格式输入边界框（每行一个），并可选输入逗号分隔的标签。
3. 点击 **Draw boxes**，然后下载标注后的图片。

### AI Evaluator（AI 评估）
1. 先上传数据集。
2. 选择 **AI Evaluator** 查看描述性统计和相关矩阵。
3. 粘贴 OpenAI API Key，输入提示词，点击 **Ask AI** 获取自然语言洞察。

---

## 运行测试

```bash
pytest tests/ -v
```

---

## 环境变量

| 变量 | 说明 |
|---|---|
| `OPENAI_API_KEY` | AI Evaluator 使用的 OpenAI API Key（也可在 UI 中输入） |
