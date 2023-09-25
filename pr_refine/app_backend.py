from json.decoder import JSONDecodeError

import streamlit as st

from pr_refine.refine_agent import CheckpointAgent
from pr_refine.select import Select


def ai_say(text: str):
    st.session_state.msgs.append([text, False])


def clear_all():
    clear_msgs()
    clear_select()
    st.session_state.running_step = 0


def clear_msgs():
    st.session_state.msgs = []


def init_pr_refine(pr: str, name: str) -> str:
    clear_all()

    if len(pr) >= 2048:
        return "目前暂不支持长度超过2000的文档分析，敬请期待！"

    st.session_state.pr = pr

    return route()


def step_up():
    st.session_state.running_step += 1


def route() -> str:
    clear_select()
    msg = _route()
    st.session_state.msgs.append((msg, False))
    st.experimental_rerun()


def _route() -> str:
    match st.session_state.running_step:
        case 0:
            return detect_user_problem()
        case 1:
            return detect_feature_value()
        case 2:
            return detect_user_cases()
        case 3:
            return eval_feature_desc()
        case 4:
            return eval_feature_logic_rule()
        case 5:
            return complete()
        case _:
            return f"系统异常，未知评审状态：{st.session_state.refine_step}"


def clear_select():
    st.session_state.select = None


def detect_user_problem() -> str:
    topic = "PRD"
    point = "该需求为用户解决了什么问题的描述文字"
    user_problem = CheckpointAgent(topic, point, st.session_state.pr)
    try:
        flag = user_problem.detect()
        print(f"Flag: {flag}")
    except (ValueError, JSONDecodeError):
        flag = False

    improve_user_problem(user_problem)
    return "生成该需求解决的用户问题，请选择"


def improve_user_problem(user_problem: CheckpointAgent):
    try:
        choices = user_problem.gen_choices()
    except (ValueError, JSONDecodeError):
        st.warning("LLM结果解析失败，请重试！")
        choices = []

    def select_callback(selected_choices: list[str]):
        st.session_state.gen_user_problem = user_problem.summarize(selected_choices)
        step_up()
        route()

    def gen_more_callback():
        choices = user_problem.gen_choices()
        st.session_state.multiselect.choices = choices
        route()

    def skip_callback():
        step_up()
        route()

    select = Select(
        choices=choices,
        choice_label="确认",
        choice_callback=select_callback,
        choice_multi=True,
        input_enabled=True,
        input_btn_text="自定义",
        input_instruction="如果对原始生成的内容不满意，可以在此处给出你的指示",
    )
    select.add_button("重新生成", gen_more_callback)
    select.add_button("跳过", skip_callback)


def detect_feature_value():
    step_up()
    route()


def detect_user_cases():
    step_up()
    route()


def eval_feature_desc():
    step_up()
    route()


def eval_feature_logic_rule():
    step_up()
    route()


def complete():
    clear_select()
