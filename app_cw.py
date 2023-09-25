import time
from io import BytesIO

import pandas as pd
import streamlit as st

from pr_refine.cw_check import Checker, Report

st.set_page_config(layout="wide")


@st.cache_data
def to_excel(df: pd.DataFrame):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    processed_data = output.getvalue()
    return processed_data


st.session_state.setdefault("reports", [])
st.session_state.setdefault("data", [])
st.session_state.setdefault("status", "")

st.markdown("# 项目需求检查")

with st.sidebar:
    st.markdown("请注意，目前仅支持由feishu文档导出为docx的需求文档，并且要求文档中的章节格式都做了标题，否责将无法正确解析文章内容")

    uploaded_files = st.file_uploader(
        label="上传需求文档",
        accept_multiple_files=True,
        type=["docx"],
        key="cases",
        label_visibility="hidden",
    )

    check_btn = st.button(label="check")

if check_btn and uploaded_files:
    st.session_state.reports.clear()
    st.session_state.data.clear()
    st.session_state.status = ""

    case_count = len(uploaded_files)
    pb = st.progress(0, text=f"0/{case_count} 文档")
    cost, time_usage = 0, 0
    t0 = time.time()

    for i in range(case_count):
        t1 = time.time()
        case = uploaded_files[i]
        case_name = case.name

        print(f"开始检查文档{case_name}")
        report: Report = Checker(case).check()
        print(f"结束检查文档{case_name}，耗时：{time.time()-t1:.2f}s")

        st.session_state.reports.append(report)
        curr_cost = report.cost
        st.session_state.data.append(
            {"case": report.name, "flag": report.flag, "report": report.report}
        )
        cost += curr_cost
        pb.progress((i + 1) / case_count, text=f"{i+1}/{case_count} 文档")

    time_usage = time.time() - t0
    st.session_state.status = f"耗时:{time_usage:.0f}s 成本:${cost:.4f}"


if st.session_state.data:
    st.dataframe(
        st.session_state.data,
        use_container_width=True,
        column_config={
            "case": st.column_config.TextColumn("方案", width="small"),
            "flag": st.column_config.CheckboxColumn("检查结果", width="small"),
            "report": st.column_config.TextColumn("文档解析", width="large", default=""),
        },
    )

if len(st.session_state.reports) > 0:
    keys = [report.name for report in st.session_state.reports]
    tabs = st.tabs(["status"] + list(keys))

    with tabs[0]:
        st.markdown(st.session_state.status)

    for tab, report in zip(tabs[1:], st.session_state.reports):
        assert isinstance(report, Report)
        with tab:
            data = pd.DataFrame(report.table)
            excel_data = to_excel(data)
            st.download_button(
                "下载",
                data=excel_data,
                file_name=f"{report.name}.xlsx",
            )
            st.dataframe(
                data,
                use_container_width=True,
            )
