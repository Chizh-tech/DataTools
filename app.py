"""DataTools – Streamlit application entry point.

Run with::

    streamlit run app.py
"""

import io

import matplotlib
import pandas as pd
import streamlit as st

matplotlib.use("Agg")

from src.ai_evaluator import ask_openai, compute_statistics, correlation_matrix
from src.data_processor import get_summary, load_csv, load_excel
from src.image_tools import draw_bounding_boxes, load_image
from src.plot_generator import bar_chart, histogram, line_chart, scatter_chart

st.set_page_config(page_title="DataTools", page_icon="🔧", layout="wide")
st.title("🔧 DataTools")

# ---------------------------------------------------------------------------
# Sidebar – navigation
# ---------------------------------------------------------------------------
section = st.sidebar.radio(
    "Navigation",
    ["Data Processor", "Plot Generator", "Image Tools", "AI Evaluator"],
)

# ---------------------------------------------------------------------------
# Shared state – data uploaded in the Data Processor tab is available to
# subsequent tabs.
# ---------------------------------------------------------------------------
if "df" not in st.session_state:
    st.session_state["df"] = None

# ===========================================================================
# DATA PROCESSOR
# ===========================================================================
if section == "Data Processor":
    st.header("📂 Data Processor")

    uploaded_file = st.file_uploader(
        "Upload a CSV or Excel file", type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = load_csv(uploaded_file)
            else:
                df = load_excel(uploaded_file)
            st.session_state["df"] = df
            st.success(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")
            st.dataframe(df.head(50))

            summary = get_summary(df)
            with st.expander("Dataset Summary"):
                st.write(f"**Shape:** {summary['shape']}")
                st.write("**Column types:**", summary["dtypes"])
                st.write("**Missing values:**", summary["missing"])
                st.dataframe(pd.DataFrame(summary["describe"]))
        except ValueError as exc:
            st.error(str(exc))

# ===========================================================================
# PLOT GENERATOR
# ===========================================================================
elif section == "Plot Generator":
    st.header("📊 Plot Generator")

    df: pd.DataFrame | None = st.session_state.get("df")

    if df is None:
        st.info("Please upload a dataset in the **Data Processor** section first.")
    else:
        chart_type = st.selectbox(
            "Chart type", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"]
        )

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        all_cols = df.columns.tolist()

        if chart_type == "Histogram":
            col = st.selectbox("Column", numeric_cols)
            bins = st.slider("Bins", min_value=5, max_value=100, value=20)
            if st.button("Generate"):
                fig = histogram(df, col, bins=bins)
                st.pyplot(fig)
        else:
            x_col = st.selectbox("X column", all_cols, key="x")
            y_col = st.selectbox("Y column", numeric_cols, key="y")
            if st.button("Generate"):
                if chart_type == "Bar Chart":
                    fig = bar_chart(df, x_col, y_col)
                elif chart_type == "Line Chart":
                    fig = line_chart(df, x_col, y_col)
                else:
                    fig = scatter_chart(df, x_col, y_col)
                st.pyplot(fig)

# ===========================================================================
# IMAGE TOOLS
# ===========================================================================
elif section == "Image Tools":
    st.header("🖼️ Image Tools")

    uploaded_image = st.file_uploader(
        "Upload an image", type=["png", "jpg", "jpeg", "bmp", "gif"]
    )

    if uploaded_image is not None:
        try:
            img = load_image(uploaded_image)
            st.image(img, caption="Original image", use_container_width=True)

            st.subheader("Draw Bounding Boxes")
            st.write(
                "Enter bounding boxes as comma-separated values: "
                "`x0,y0,x1,y1` — one box per line."
            )
            raw_boxes = st.text_area("Bounding boxes", placeholder="10,10,100,100")
            raw_labels = st.text_input(
                "Labels (comma-separated, optional)", placeholder="cat, dog"
            )
            box_color = st.color_picker("Box colour", value="#FF0000")
            box_width = st.slider("Line width", min_value=1, max_value=10, value=2)

            if st.button("Draw boxes"):
                try:
                    boxes = []
                    for line in raw_boxes.strip().splitlines():
                        parts = [int(v.strip()) for v in line.split(",")]
                        if len(parts) != 4:
                            st.error(f"Invalid box: '{line}' – expected x0,y0,x1,y1")
                            boxes = []
                            break
                        boxes.append(tuple(parts))

                    if boxes:
                        labels = (
                            [l.strip() for l in raw_labels.split(",")]
                            if raw_labels.strip()
                            else None
                        )
                        result_img = draw_bounding_boxes(
                            img, boxes, labels=labels, color=box_color, width=box_width
                        )
                        st.image(
                            result_img,
                            caption="Image with bounding boxes",
                            use_container_width=True,
                        )

                        # Offer download
                        buf = io.BytesIO()
                        result_img.save(buf, format="PNG")
                        st.download_button(
                            "Download result",
                            data=buf.getvalue(),
                            file_name="annotated.png",
                            mime="image/png",
                        )
                except ValueError as exc:
                    st.error(str(exc))
        except ValueError as exc:
            st.error(str(exc))

# ===========================================================================
# AI EVALUATOR
# ===========================================================================
elif section == "AI Evaluator":
    st.header("🤖 AI Evaluator")

    df = st.session_state.get("df")

    if df is None:
        st.info("Please upload a dataset in the **Data Processor** section first.")
    else:
        st.subheader("Statistical Analysis")
        stats_result = compute_statistics(df)
        if stats_result:
            st.dataframe(pd.DataFrame(stats_result).T)
        else:
            st.warning("No numeric columns found in the dataset.")

        st.subheader("Correlation Matrix")
        corr = correlation_matrix(df)
        if not corr.empty:
            st.dataframe(corr.style.background_gradient(cmap="coolwarm"))
        else:
            st.warning("Not enough numeric columns to compute correlations.")

        st.subheader("Ask OpenAI about your data")
        api_key = st.text_input("OpenAI API Key", type="password")
        user_prompt = st.text_area(
            "Prompt",
            value="Summarise the key insights from the statistical analysis above.",
        )

        if st.button("Ask AI"):
            summary_text = pd.DataFrame(stats_result).T.to_string() if stats_result else "No numeric data."
            full_prompt = f"{user_prompt}\n\nData statistics:\n{summary_text}"
            try:
                answer = ask_openai(full_prompt, api_key=api_key or None)
                st.write(answer)
            except (ValueError, RuntimeError) as exc:
                st.error(str(exc))
