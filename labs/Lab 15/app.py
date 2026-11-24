"""Streamlit interface for the Lab 15 portfolio stability decision."""

import copy

import streamlit as st

from portfolio import (CORRELATIONS, OBJECTIVE_RETURN, RESERVE_ELIGIBLE, SLEEVES,
                       estimate_from_prices_csv, search_lowest_risk_mix)

DEFAULT_RESERVE_ASSETS = RESERVE_ELIGIBLE | {"BIL", "IEF"}

st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
st.title("Portfolio Stability Decision")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("Mandate controls")
    objective = st.number_input("Objective: expected return (%)", value=OBJECTIVE_RETURN * 100,
                                step=0.1, format="%.2f") / 100
    reserve_minimum = st.number_input("Reserve minimum (%)", value=3.0,
                                      min_value=0.0, max_value=100.0,
                                      step=1.0, format="%.2f") / 100
    uploaded_prices = st.file_uploader("Upload monthly prices.csv", type="csv")
    last_36 = st.toggle("Use only the last 36 monthly returns", value=False)

try:
    if uploaded_prices is None:
        loaded_sleeves = copy.deepcopy(SLEEVES)
        loaded_correlations = copy.deepcopy(CORRELATIONS)
        source_label = "Meridian inputs"
    else:
        uploaded_prices.seek(0)
        loaded_sleeves, loaded_correlations = estimate_from_prices_csv(uploaded_prices, last_36)
        source_label = "uploaded prices.csv (last 36 monthly returns)" if last_36 else "uploaded prices.csv (all monthly returns)"
except ValueError as error:
    st.error(f"Could not estimate from this CSV: {error}")
    st.stop()

loaded_answer = search_lowest_risk_mix(
    loaded_sleeves, loaded_correlations, objective,
    DEFAULT_RESERVE_ASSETS & set(loaded_sleeves), reserve_minimum
)

st.subheader(f"Expected-return estimates — {source_label}")
st.caption("CSV-based values are annualized arithmetic historical estimates, not forecasts.")
edited_sleeves = copy.deepcopy(loaded_sleeves)
columns = st.columns(len(loaded_sleeves))
for column, name in zip(columns, loaded_sleeves):
    with column:
        edited_sleeves[name]["expected_return"] = st.number_input(
            name, value=loaded_sleeves[name]["expected_return"] * 100,
            step=0.1, format="%.2f", key=f"return_{name}"
        ) / 100

st.subheader("Reserve eligibility")
reserve_eligible = {
    name for name in loaded_sleeves
    if st.checkbox(name, value=name in DEFAULT_RESERVE_ASSETS, key=f"reserve_{name}")
}

edited_answer = search_lowest_risk_mix(
    edited_sleeves, loaded_correlations, objective, reserve_eligible, reserve_minimum
)


def answer_panel(heading, answer):
    st.markdown(f"### {heading}")
    if answer is None:
        st.warning("No mix meets the objective.")
        return
    st.dataframe(
        {"Asset": list(answer["weights"]),
         "Weight (%)": [round(weight * 100, 1) for weight in answer["weights"].values()]},
        hide_index=True, width="stretch",
    )
    first, second, third = st.columns(3)
    first.metric("Expected return", f"{answer['expected_return'] * 100:.2f}%")
    second.metric("Volatility", f"{answer['volatility'] * 100:.2f}%")
    third.metric("Reserve-eligible", f"{answer['reserve_weight'] * 100:.1f}%")


left, right = st.columns(2)
with left:
    answer_panel("Lowest-risk mix", edited_answer)
with right:
    answer_panel("Answer for inputs as loaded", loaded_answer)
    if edited_answer is not None and loaded_answer is not None:
        largest_change = max(
            abs(edited_answer["weights"][name] - loaded_answer["weights"][name])
            for name in loaded_sleeves
        )
        st.metric("Largest weight change", f"{largest_change * 100:.0f} points")
    else:
        st.caption("Largest weight change is unavailable because one answer is infeasible.")
