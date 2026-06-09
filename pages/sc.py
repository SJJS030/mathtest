# app.py
# 중학교 2학년 함수 단원
# 일차함수 그래프의 교점과 연립방정식의 해의 관계 탐구 앱

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import requests

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

st.set_page_config(
    page_title="일차함수 그래프와 연립방정식",
    page_icon="📈",
    layout="centered"
)

st.title("📈 일차함수의 그래프와 연립방정식의 해")
st.write("두 일차함수의 그래프를 보고, 교점이 연립방정식의 해와 같다는 것을 탐구해 봅시다.")

st.info(
    "이 앱은 학생이 연립방정식을 바로 답만 보는 것이 아니라, "
    "대입법 또는 가감법으로 단계별로 생각하도록 질문을 제공합니다."
)

x = sp.symbols("x")

def parse_linear_expression(text):
    """
    학생이 입력한 문자열을 sympy 식으로 변환합니다.
    2x+1, 0.5x-2, 3(x+1)처럼 곱셈기호를 생략한 입력도 허용합니다.
    """
    try:
        transformations = standard_transformations + (implicit_multiplication_application,)

        expr = parse_expr(
            text,
            transformations=transformations
        )

        if expr.free_symbols - {x}:
            return None, "x 이외의 문자는 변수로 사용할 수 없습니다."

        degree = sp.degree(expr, x)

        if degree is None or degree > 1:
            return None, "일차식 또는 상수식만 입력할 수 있습니다."

        return sp.expand(expr), None

    except Exception:
        return None, "식을 해석할 수 없습니다. 예: 2x+1, -x+4, 0.5x-2"

st.subheader("1️⃣ 두 일차함수 입력하기")

st.info(
    "숫자와 문자 사이의 곱셈기호(*)는 생략할 수 있습니다.\n"
    "예: 2x+1, -x+4, 0.5x-2"
)

st.code("2x+1\n-x+4\n0.5x-2")

col1, col2 = st.columns(2)

with col1:
    expr1_text = st.text_input("첫 번째 일차함수 y =", value="2x + 1")

with col2:
    expr2_text = st.text_input("두 번째 일차함수 y =", value="-x + 4")

expr1, error1 = parse_linear_expression(expr1_text)
expr2, error2 = parse_linear_expression(expr2_text)

if error1:
    st.error(f"첫 번째 식 오류: {error1}")

if error2:
    st.error(f"두 번째 식 오류: {error2}")

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

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    ax.grid(True)
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("두 일차함수의 그래프")

    a1 = sp.expand(expr1).coeff(x)
    b1 = sp.expand(expr1).subs(x, 0)

    a2 = sp.expand(expr2).coeff(x)
    b2 = sp.expand(expr2).subs(x, 0)

    solution = sp.solve(sp.Eq(expr1, expr2), x)

    if a1 == a2 and b1 == b2:
        relation = "일치"
    elif a1 == a2:
        relation = "평행"
    else:
        relation = "한 점에서 만남"

    if relation == "한 점에서 만남" and len(solution) == 1:
        x_intersection = solution[0]
        y_intersection = expr1.subs(x, x_intersection)

        ax.scatter(
            [float(x_intersection)],
            [float(y_intersection)],
            s=80,
            zorder=5
        )

        ax.annotate(
            "교점",
            (float(x_intersection), float(y_intersection)),
            textcoords="offset points",
            xytext=(10, 10)
        )

    st.pyplot(fig)

    st.subheader("3️⃣ 두 그래프의 위치관계 생각하기")

    if relation == "일치":
        st.success("두 그래프는 완전히 같습니다.")
        st.write("두 그래프 위의 모든 점이 두 식을 동시에 만족합니다.")
        st.write("따라서 연립방정식의 해는 무수히 많습니다.")

    elif relation == "평행":
        st.warning("두 그래프는 평행합니다.")
        st.write("두 그래프가 만나지 않으므로 교점이 없습니다.")
        st.write("따라서 연립방정식의 해도 없습니다.")

    else:
        st.success("두 그래프는 한 점에서 만납니다.")
        st.write("이제 그 교점이 연립방정식의 해와 같은지 직접 확인해 봅시다.")

    st.subheader("4️⃣ 그래프를 연립방정식으로 나타내기")

    st.write("두 일차함수는 다음 연립방정식으로 나타낼 수 있습니다.")

    st.latex(
        r"\begin{cases}"
        + f"y = {sp.latex(expr1)}"
        + r"\\"
        + f"y = {sp.latex(expr2)}"
        + r"\end{cases}"
    )

    if relation == "한 점에서 만남":

        st.subheader("5️⃣ 연립방정식을 직접 풀어 보기")

        st.write("풀이 방법을 선택해 봅시다.")

        method = st.radio(
            "어떤 방법으로 풀어볼까요?",
            ["대입법", "가감법"]
        )

        if method == "대입법":
            st.markdown("### 🔁 대입법으로 풀기")

            st.write("두 식 모두 y에 대한 식입니다.")
            st.write("그러면 두 식의 오른쪽을 서로 같다고 놓을 수 있습니다.")

            step1 = st.text_input(
                "질문 1. 두 식의 오른쪽을 같게 놓으면 어떤 식이 되나요?",
                placeholder="예: 2x+1=-x+4"
            )

            if step1:
                st.info("좋습니다. 이제 x가 들어 있는 항은 한쪽으로, 숫자만 있는 항은 다른 쪽으로 모아 봅시다.")

                step2 = st.text_input(
                    "질문 2. x에 대한 일차방정식으로 정리하면 어떻게 되나요?",
                    placeholder="예: 3x=3"
                )

                if step2:
                    st.info("이제 양변을 같은 수로 나누어 x값을 구합니다.")

                    student_x = st.text_input(
                        "질문 3. x의 값은 무엇인가요?",
                        placeholder="예: 1"
                    )

                    if student_x:
                        try:
                            student_x_value = parse_expr(
                                student_x,
                                transformations=standard_transformations + (implicit_multiplication_application,)
                            )

                            correct_x = sp.nsimplify(x_intersection)

                            if sp.simplify(student_x_value - correct_x) == 0:
                                st.success("맞습니다. x값을 잘 구했습니다.")

                                st.write("이제 구한 x값을 둘 중 하나의 식에 대입해서 y값을 구합니다.")

                                student_y = st.text_input(
                                    "질문 4. y의 값은 무엇인가요?",
                                    placeholder="예: 3"
                                )

                                if student_y:
                                    student_y_value = parse_expr(
                                        student_y,
                                        transformations=standard_transformations + (implicit_multiplication_application,)
                                    )

                                    correct_y = sp.nsimplify(y_intersection)

                                    if sp.simplify(student_y_value - correct_y) == 0:
                                        st.success("맞습니다. 연립방정식의 해를 찾았습니다.")
                                        st.latex(
                                            f"(x, y) = ({sp.latex(correct_x)}, {sp.latex(correct_y)})"
                                        )
                                        st.write("이 좌표가 그래프의 교점과 같은지 확인해 봅시다.")
                                    else:
                                        st.error("y값이 아직 맞지 않습니다. 구한 x값을 식에 다시 대입해 보세요.")
                            else:
                                st.error("x값이 아직 맞지 않습니다. 이항 과정을 다시 확인해 보세요.")

                        except Exception:
                            st.error("숫자 또는 분수 형태로 입력해 주세요. 예: 1, 3/2")

        elif method == "가감법":
            st.markdown("### ➕➖ 가감법으로 풀기")

            st.write("먼저 두 식을 일반적인 연립방정식 모양으로 바꿔 봅시다.")
            st.write("즉, x항과 y항을 왼쪽에, 상수항을 오른쪽에 놓습니다.")

            eq1_left = y_minus_1 = sp.expand(-a1 * x + sp.Symbol("y"))
            eq2_left = y_minus_2 = sp.expand(-a2 * x + sp.Symbol("y"))

            st.latex(
                r"\begin{cases}"
                + f"{sp.latex(eq1_left)} = {sp.latex(b1)}"
                + r"\\"
                + f"{sp.latex(eq2_left)} = {sp.latex(b2)}"
                + r"\end{cases}"
            )

            st.write("두 식 모두 y의 계수가 같습니다.")
            st.write("따라서 두 식을 빼면 y항이 사라집니다.")

            step1 = st.text_input(
                "질문 1. 두 식을 빼면 어떤 x에 대한 식이 나오나요?",
                placeholder="예: -3x=-3"
            )

            if step1:
                st.info("좋습니다. 이제 x값을 구해 봅시다.")

                student_x = st.text_input(
                    "질문 2. x의 값은 무엇인가요?",
                    placeholder="예: 1"
                )

                if student_x:
                    try:
                        student_x_value = parse_expr(
                            student_x,
                            transformations=standard_transformations + (implicit_multiplication_application,)
                        )

                        correct_x = sp.nsimplify(x_intersection)

                        if sp.simplify(student_x_value - correct_x) == 0:
                            st.success("맞습니다. x값을 잘 구했습니다.")

                            student_y = st.text_input(
                                "질문 3. 구한 x값을 식에 대입하면 y의 값은 무엇인가요?",
                                placeholder="예: 3"
                            )

                            if student_y:
                                student_y_value = parse_expr(
                                    student_y,
                                    transformations=standard_transformations + (implicit_multiplication_application,)
                                )

                                correct_y = sp.nsimplify(y_intersection)

                                if sp.simplify(student_y_value - correct_y) == 0:
                                    st.success("맞습니다. 연립방정식의 해를 찾았습니다.")
                                    st.latex(
                                        f"(x, y) = ({sp.latex(correct_x)}, {sp.latex(correct_y)})"
                                    )
                                    st.write("이 좌표가 그래프의 교점과 같은지 확인해 봅시다.")
                                else:
                                    st.error("y값이 아직 맞지 않습니다. x값을 식에 대입하는 과정을 다시 확인해 보세요.")
                        else:
                            st.error("x값이 아직 맞지 않습니다. 두 식을 뺀 결과를 다시 확인해 보세요.")

                    except Exception:
                        st.error("숫자 또는 분수 형태로 입력해 주세요. 예: 1, 3/2")

        st.subheader("6️⃣ 그래프의 교점과 비교하기")

        st.write("그래프에서 두 직선이 만나는 점은 다음과 같습니다.")

        st.latex(
            f"({sp.latex(sp.nsimplify(x_intersection))}, "
            f"{sp.latex(sp.nsimplify(y_intersection))})"
        )

        st.write(
            "연립방정식의 해는 두 식을 동시에 만족하는 x, y의 값입니다. "
            "그래프에서는 두 식을 동시에 만족하는 점이 바로 두 그래프의 교점입니다."
        )

        st.success("따라서 일차함수 그래프의 교점은 연립방정식의 해와 같습니다.")

    st.subheader("7️⃣ 탐구 질문 정리")

    st.markdown(
        """
        - 두 그래프가 만나는 점은 두 식을 모두 만족하나요?
        - 대입법으로 구한 해와 그래프의 교점은 같나요?
        - 가감법으로 구한 해와 그래프의 교점은 같나요?
        - 그래프가 평행하면 연립방정식의 해는 왜 없을까요?
        - 그래프가 완전히 같으면 해가 왜 무수히 많을까요?
        """
    )

    st.subheader("8️⃣ 연습 문제")

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
            st.success("정답입니다. 그래프의 두 식을 그대로 연립하면 됩니다.")
        else:
            st.error("아쉽습니다. 그래프의 식 두 개를 그대로 연립방정식으로 나타내야 합니다.")

    st.subheader("9️⃣ Wolfram Alpha로 확인하기")

    query = f"solve y={expr1}, y={expr2}"
    wolfram_url = "https://www.wolframalpha.com/input?i=" + requests.utils.quote(query)

    st.markdown(f"[Wolfram Alpha에서 확인하기]({wolfram_url})")
