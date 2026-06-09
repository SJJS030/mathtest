# app.py
# 중2 함수 단원: 일차함수 그래프와 연립방정식의 해 탐구 앱

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import requests

st.set_page_config(
    page_title="일차함수 그래프와 연립방정식",
    page_icon="📈",
    layout="centered"
)

st.title("📈 일차함수의 그래프와 연립방정식의 해")
st.write("두 일차함수의 그래프를 보고, 교점이 연립방정식의 해와 같다는 것을 탐구해 봅시다.")

# -----------------------------
# Wolfram Alpha API 안내
# -----------------------------
st.info(
    "참고: Wolfram Alpha 공식 API는 보통 AppID가 필요합니다. "
    "이 앱은 Streamlit Cloud에서 바로 실행되도록 기본 계산은 파이썬으로 처리하고, "
    "Wolfram Alpha 확인 링크를 함께 제공합니다."
)

# -----------------------------
# 입력 예시 안내
# -----------------------------
st.subheader("1️⃣ 두 일차함수 입력하기")

st.write("아래와 같은 형태로 입력하세요.")
st.code("2*x + 1\n-x + 4\n0.5*x - 2")

col1, col2 = st.columns(2)

with col1:
    expr1_text = st.text_input("첫 번째 일차함수 y =", value="2*x + 1")

with col2:
    expr2_text = st.text_input("두 번째 일차함수 y =", value="-x + 4")

x = sp.symbols("x")

# -----------------------------
# 식을 안전하게 변환하는 함수
# -----------------------------
def parse_linear_expression(text):
    """
    학생이 입력한 문자열을 sympy 식으로 변환합니다.
    x만 변수로 허용합니다.
    """
    try:
        expr = sp.sympify(text)
        if expr.free_symbols - {x}:
            return None, "x 이외의 문자는 변수로 사용할 수 없습니다."
        degree = sp.degree(expr, x)
        if degree is None or degree > 1:
            return None, "일차식 또는 상수식만 입력할 수 있습니다."
        return expr, None
    except Exception:
        return None, "식을 해석할 수 없습니다. 예: 2*x + 1 처럼 입력하세요."

expr1, error1 = parse_linear_expression(expr1_text)
expr2, error2 = parse_linear_expression(expr2_text)

if error1:
    st.error(f"첫 번째 식 오류: {error1}")

if error2:
    st.error(f"두 번째 식 오류: {error2}")

# -----------------------------
# 두 식이 올바를 때만 실행
# -----------------------------
if expr1 is not None and expr2 is not None:
    st.subheader("2️⃣ 그래프로 확인하기")

    f1 = sp.lambdify(x, expr1, "numpy")
    f2 = sp.lambdify(x, expr2, "numpy")

    x_values = np.linspace(-10, 10, 400)
    y1_values = f1(x_values)
    y2_values = f2(x_values)

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(x_values, y1_values, label=f"y = {expr1}")
    ax.plot(x_values, y2_values, label=f"y = {expr2}")

    # 좌표축 표시
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    ax.grid(True)
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("두 일차함수의 그래프")

    # 교점 계산
    solution = sp.solve(sp.Eq(expr1, expr2), x)

    if len(solution) == 1:
        x_intersection = solution[0]
        y_intersection = expr1.subs(x, x_intersection)

        ax.scatter(
            [float(x_intersection)],
            [float(y_intersection)],
            s=80,
            zorder=5
        )

        ax.annotate(
            f"교점 ({sp.nsimplify(x_intersection)}, {sp.nsimplify(y_intersection)})",
            (float(x_intersection), float(y_intersection)),
            textcoords="offset points",
            xytext=(10, 10)
        )

    st.pyplot(fig)

    # -----------------------------
    # 위치관계 설명
    # -----------------------------
    st.subheader("3️⃣ 두 그래프의 위치관계")

    a1 = sp.expand(expr1).coeff(x)
    b1 = sp.expand(expr1).subs(x, 0)

    a2 = sp.expand(expr2).coeff(x)
    b2 = sp.expand(expr2).subs(x, 0)

    if a1 == a2 and b1 == b2:
        st.success("두 그래프는 완전히 같습니다. 해가 무수히 많습니다.")
        relation = "일치"
    elif a1 == a2:
        st.warning("두 그래프는 평행합니다. 교점이 없으므로 연립방정식의 해도 없습니다.")
        relation = "평행"
    else:
        st.success("두 그래프는 한 점에서 만납니다. 그 교점이 연립방정식의 해입니다.")
        relation = "한 점에서 만남"

    # -----------------------------
    # 연립방정식과 해
    # -----------------------------
    st.subheader("4️⃣ 교점과 연립방정식의 해")

    st.write("두 일차함수")
    st.latex(f"y = {sp.latex(expr1)}")
    st.latex(f"y = {sp.latex(expr2)}")

    st.write("는 다음 연립방정식과 같습니다.")
    st.latex(
        r"\begin{cases}"
        + f"y = {sp.latex(expr1)}"
        + r"\\"
        + f"y = {sp.latex(expr2)}"
        + r"\end{cases}"
    )

    if relation == "한 점에서 만남":
        st.write("따라서 두 식의 y값이 같아지는 x를 찾으면 됩니다.")
        st.latex(f"{sp.latex(expr1)} = {sp.latex(expr2)}")
        st.latex(f"x = {sp.latex(sp.nsimplify(x_intersection))}")
        st.latex(f"y = {sp.latex(sp.nsimplify(y_intersection))}")

        st.success(
            f"연립방정식의 해는 "
            f"({sp.nsimplify(x_intersection)}, {sp.nsimplify(y_intersection)}) 입니다."
        )

    elif relation == "평행":
        st.error("두 그래프가 만나지 않으므로 연립방정식의 해가 없습니다.")

    else:
        st.info("두 그래프가 완전히 같으므로 모든 점이 해입니다. 해가 무수히 많습니다.")

    # -----------------------------
    # 학생 탐구 질문
    # -----------------------------
    st.subheader("5️⃣ 탐구 질문")

    st.markdown(
        """
        - 두 그래프가 만나는 점의 x좌표와 y좌표는 무엇인가요?
        - 그 좌표를 두 식에 각각 대입하면 모두 참이 되나요?
        - 두 그래프가 평행하면 연립방정식의 해는 어떻게 되나요?
        - 두 그래프가 완전히 같으면 해는 몇 개일까요?
        """
    )

    # -----------------------------
    # 문제 제공
    # -----------------------------
    st.subheader("6️⃣ 연습 문제")

    st.write("아래 두 일차함수의 교점과 같은 해를 갖는 연립방정식을 찾으세요.")

    problem_expr1 = 3 * x - 2
    problem_expr2 = -x + 6

    st.latex(f"y = {sp.latex(problem_expr1)}")
    st.latex(f"y = {sp.latex(problem_expr2)}")

    answer = st.radio(
        "이 그래프들의 교점과 같은 해를 갖는 연립방정식은?",
        [
            "① y = 3x - 2, y = -x + 6",
            "② y = 3x + 2, y = -x + 6",
            "③ y = -3x - 2, y = x + 6",
            "④ y = 3x - 2, y = x - 6"
        ]
    )

    if st.button("정답 확인"):
        if answer.startswith("①"):
            st.success("정답입니다! 두 그래프의 식을 그대로 연립하면 됩니다.")
        else:
            st.error("아쉽습니다. 그래프의 식 두 개를 그대로 연립방정식으로 나타내야 합니다.")

    # -----------------------------
    # Wolfram Alpha 확인 링크
    # -----------------------------
    st.subheader("7️⃣ Wolfram Alpha로 확인하기")

    query = f"solve y={expr1}, y={expr2}"
    wolfram_url = "https://www.wolframalpha.com/input?i=" + requests.utils.quote(query)

    st.markdown(
        f"[Wolfram Alpha에서 확인하기]({wolfram_url})"
    )
