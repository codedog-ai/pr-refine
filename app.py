import streamlit as st
from st_chat_message import message

from pr_refine.app_backend import init_pr_refine
from pr_refine.select import Select

st.set_page_config(page_title="PR Refine", layout="wide")

st.session_state.setdefault("pr", "")

st.session_state.setdefault("msgs", [["你好，我会帮你生成需求", False]])
st.session_state.setdefault("choices", [])

st.session_state.setdefault("running", False)
st.session_state.setdefault("running_step", 0)

st.session_state.setdefault("select", None)

st.session_state.setdefault("gen_user_problem", "")
inter, raw = st.columns([3, 1])

with inter:
    chat_placeholder = st.empty()

    with chat_placeholder.container():
        for i in range(len(st.session_state.msgs)):
            msg, is_user = st.session_state.msgs[i]
            message(msg, is_user=is_user)

        spinner_div = st.empty()

        select: Select = st.session_state.select

        if select:
            flags = []
            options = []
            input_text = ""
            choices = select.choices

            if select.choice_multi:
                for choice in select.choices:
                    flags.append(st.checkbox(label=choice))
            else:
                option = st.radio("", options=select.choices, label_visibility="hidden")
                options.append(option)
            if select.input_enabled:
                input_text = st.text_input(label=select.input_instruction, value="")
            btn = st.button(select.choice_label, use_container_width=True)
            if btn:
                if select.choice_multi:
                    options = [
                        choice for choice, flag in zip(select.choices, flags) if flag
                    ]

                if options:
                    with spinner_div.container():
                        with st.spinner("运行中..."):
                            select.choice_callback(options)

            if select.input_enabled:
                input_btn = st.button(select.input_btn_text, use_container_width=True)
                if input_btn:
                    with spinner_div.container():
                        with st.spinner("运行中..."):
                            select.input_callback(input_text)
            for btext, func in select.extra_buttons:
                btn = st.button(btext, use_container_width=True)
                if btn:
                    with spinner_div.container():
                        with st.spinner("运行中..."):
                            func()

with raw:
    if st.session_state.gen_user_problem:
        st.text_area("问题描述", st.session_state.gen_user_problem, height=500)

demo_pr = "搜索日志时推荐字段和字段值"
demo_name = "日志搜索框推荐交互"
with st.sidebar:
    pr_text = st.text_input("一句话需求")
    start_btn = st.button("启动", use_container_width=True)
    demo_btn = st.button("demo", use_container_width=True)

    if demo_btn:
        with spinner_div.container():
            with st.spinner("运行中..."):
                init_pr_refine(demo_pr, demo_name)

    st.markdown("## 知识库设置")
