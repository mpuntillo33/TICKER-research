"""A testable Streamlit robo-advisor exercise. Educational use only."""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd
import requests
import streamlit as st

FRENCH_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip"
GS10_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=GS10"
START, END = "1990-01", "2025-12"


def suggested_allocation(age: int, horizon: int, needed_within_3_years: bool,
                         emergency_fund: bool, max_loss: float, reaction: str) -> tuple[int, int, int]:
    """Return stocks, bonds, cash in 10% increments using the documented risk budget."""
    stock = min(90, max(20, 110 - age))
    if horizon < 5:
        stock -= 30
    elif horizon < 10:
        stock -= 10
    if needed_within_3_years:
        stock -= 20
    if not emergency_fund:
        stock -= 10
    if max_loss <= 10:
        stock -= 20
    elif max_loss <= 15:
        stock -= 10
    if reaction == "Sell or reduce risk":
        stock -= 10
    elif reaction == "Buy more":
        stock += 10
    stock = int(np.clip(round(stock / 10) * 10, 0, 90))
    cash = 20 if needed_within_3_years or not emergency_fund else 0
    bonds = 100 - stock - cash
    return stock, bonds, cash


def _french_monthly() -> pd.DataFrame:
    response = requests.get(FRENCH_URL, timeout=30)
    response.raise_for_status()
    raw = zipfile.ZipFile(io.BytesIO(response.content)).read("F-F_Research_Data_Factors.csv").decode("latin1")
    lines = raw.splitlines()
    header = next(i for i, line in enumerate(lines) if line.strip().startswith(",Mkt-RF"))
    data = []
    for line in lines[header + 1:]:
        fields = [x.strip() for x in line.split(",")]
        if not fields or not fields[0].isdigit() or len(fields[0]) != 6:
            break
        data.append(fields[:5])
    frame = pd.DataFrame(data, columns=["yyyymm", "Mkt-RF", "SMB", "HML", "RF"])
    frame["date"] = pd.to_datetime(frame["yyyymm"], format="%Y%m")
    for column in ["Mkt-RF", "RF"]:
        frame[column] = pd.to_numeric(frame[column]) / 100
    return frame[["date", "Mkt-RF", "RF"]]


def load_returns() -> pd.DataFrame:
    """Download, align, and calculate monthly stock/cash/approximate Treasury returns."""
    french = _french_monthly()
    fred = pd.read_csv(GS10_URL)
    fred["date"] = pd.to_datetime(fred["observation_date"])
    fred["GS10"] = pd.to_numeric(fred["GS10"], errors="coerce") / 100
    data = french.merge(fred[["date", "GS10"]], on="date", how="inner").sort_values("date")
    y0, y1 = data["GS10"].shift(1), data["GS10"]
    n = 2 * (10 - 1 / 12)
    price = (y0 / y1) * (1 - (1 + y1 / 2) ** -n) + (1 + y1 / 2) ** -n
    data["stocks"] = data["Mkt-RF"] + data["RF"]
    data["cash"] = data["RF"]
    data["bonds"] = price - 1 + y0 / 12
    return data.loc[(data["date"] >= START) & (data["date"] <= END), ["date", "stocks", "bonds", "cash"]].dropna()


def metrics(returns: pd.Series, initial: float) -> dict:
    wealth = (1 + returns).cumprod()
    months = len(returns)
    rolling = (1 + returns).rolling(12).apply(np.prod, raw=True) - 1
    worst_end = rolling.idxmin()
    worst = rolling.loc[worst_end]
    return {"months": months, "cagr": wealth.iloc[-1] ** (12 / months) - 1,
            "volatility": returns.std(ddof=1) * np.sqrt(12),
            "max_drawdown": (wealth / wealth.cummax() - 1).min(),
            "worst_12": worst, "worst_end": worst_end,
            "worst_dollars": initial * worst, "wealth": wealth}


def mix_returns(data: pd.DataFrame, stocks: int, bonds: int, cash: int) -> pd.Series:
    """Build a monthly-rebalanced mix and retain its calendar month index."""
    values = (stocks * data.stocks + bonds * data.bonds + cash * data.cash) / 100
    return pd.Series(values.to_numpy(), index=data.date, name="portfolio")


def largest_safe_stock_share(data: pd.DataFrame, cash_share: int, max_loss: float) -> int | None:
    for stock in range(100 - cash_share, -1, -10):
        bonds = 100 - cash_share - stock
        returns = mix_returns(data, stock, bonds, cash_share)
        if metrics(returns, 1)["worst_12"] >= -max_loss / 100:
            return stock
    return None


st.set_page_config(page_title="Robo-Advisor Guide", layout="wide")
st.title("Robo-Advisor Guide — Client to Portfolio")
with st.sidebar:
    st.header("Client questionnaire")
    age = st.number_input("Age", 18, 100, 35)
    horizon = st.number_input("Time horizon (years)", 1, 60, 20)
    need = st.radio("When may the money be needed?", ["More than 3 years", "Within 3 years"]) == "Within 3 years"
    emergency = st.radio("Emergency fund?", ["Yes", "No"]) == "Yes"
    max_loss = st.slider("Maximum acceptable loss in any 12 months (%)", 5, 50, 20)
    reaction = st.selectbox("Reaction to a 20% market fall", ["Stay the course", "Sell or reduce risk", "Buy more"])
    initial = st.number_input("Initial investment ($)", min_value=100, value=100000, step=1000)

suggested = suggested_allocation(age, horizon, need, emergency, max_loss, reaction)
st.info("Rule: stock starts at 110 − age (20%–90%); horizon, liquidity, emergency savings, loss tolerance, and fall reaction adjust it in 10% steps. Cash is 20% for near-term needs or no emergency fund; bonds receive the balance.")
st.write(f"Suggested allocation: **{suggested[0]}% stocks / {suggested[1]}% bonds / {suggested[2]}% cash**")
override = st.checkbox("Override allocation by hand")
if override:
    cols = st.columns(3)
    stocks = cols[0].number_input("Stocks (%)", 0, 100, suggested[0], 10)
    bonds = cols[1].number_input("Bonds (%)", 0, 100, suggested[1], 10)
    cash = cols[2].number_input("Cash (%)", 0, 100, suggested[2], 10)
else:
    stocks, bonds, cash = suggested
if stocks + bonds + cash != 100:
    st.error("Allocation must sum to 100%.")
    st.stop()

try:
    data = load_returns()
except Exception as error:
    st.error(f"Live data could not be loaded: {error}")
    st.stop()
portfolio = mix_returns(data, stocks, bonds, cash)
result = metrics(portfolio, initial)
st.caption(f"{result['months']} months used: {data.date.iloc[0]:%B %Y} to {data.date.iloc[-1]:%B %Y}")
cols = st.columns(4)
cols[0].metric("CAGR", f"{result['cagr']:.2%}")
cols[1].metric("Volatility", f"{result['volatility']:.2%}")
cols[2].metric("Max drawdown", f"{result['max_drawdown']:.2%}")
cols[3].metric("Worst 12 months", f"{result['worst_12']:.2%}", f"${result['worst_dollars']:,.0f}; ended {result['worst_end']:%b %Y}")
if result["worst_12"] < -max_loss / 100:
    st.error("Red flag: the historical worst 12 months exceeded this client's maximum acceptable loss.")
safe = largest_safe_stock_share(data, cash, max_loss)
st.write("Largest stock share within this client's max loss: " + (f"**{safe}%** (cash fixed at {cash}%; bonds take the rest)." if safe is not None else "**no stock/bond mix passes**."))
growth = pd.DataFrame({"Stocks": (1 + data.stocks).cumprod(), "Bonds": (1 + data.bonds).cumprod(), "Cash": (1 + data.cash).cumprod(), "Portfolio": result["wealth"]}, index=data.date)
st.line_chart(growth)
st.divider()
st.caption("Design after matvix90/ai-robo-advisor (MIT). Data: Ken French Data Library; FRED, Federal Reserve Bank of St. Louis. Education, not investment advice.")
