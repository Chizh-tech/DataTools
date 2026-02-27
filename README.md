# DataTools

A Streamlit-based data analysis toolkit that lets you upload datasets, visualise data, annotate images with bounding boxes, and query OpenAI for AI-powered insights.

---

## Features

| Module | Functionality |
|---|---|
| **Data Processor** | Upload CSV / Excel files, preview data, view summary statistics |
| **Plot Generator** | Bar chart, line chart, scatter plot, histogram |
| **Image Tools** | Upload images, draw labelled bounding boxes, download annotated result |
| **AI Evaluator** | Descriptive statistics, correlation matrix, OpenAI chat integration |

---

## Project Structure

```
DataTools/
├── app.py               # Streamlit application entry point
├── requirements.txt     # Python dependencies
├── src/
│   ├── __init__.py
│   ├── data_processor.py   # CSV / Excel loading & summary
│   ├── plot_generator.py   # Matplotlib chart helpers
│   ├── image_tools.py      # PIL-based image utilities
│   └── ai_evaluator.py     # Statistical analysis + OpenAI wrapper
└── tests/
    ├── __init__.py
    ├── test_data_processor.py
    ├── test_plot_generator.py
    ├── test_image_tools.py
    └── test_ai_evaluator.py
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Running the App

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

---

## Usage

### Data Processor
1. Select **Data Processor** in the sidebar.
2. Upload a `.csv`, `.xlsx`, or `.xls` file.
3. Preview the first 50 rows and expand the **Dataset Summary** section for dtype, missing-value, and descriptive statistics.

### Plot Generator
1. Upload a dataset first (Data Processor tab).
2. Select **Plot Generator**, choose a chart type, and pick your columns.
3. Click **Generate** to render the chart.

### Image Tools
1. Select **Image Tools** and upload a PNG / JPEG image.
2. Enter bounding boxes as `x0,y0,x1,y1` (one per line) and optional comma-separated labels.
3. Click **Draw boxes** then download the annotated image.

### AI Evaluator
1. Upload a dataset first.
2. Select **AI Evaluator** to see descriptive statistics and the correlation matrix.
3. Paste your OpenAI API key, write a prompt, and click **Ask AI** for natural-language insights.

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key used by the AI Evaluator (can also be entered in the UI) |
