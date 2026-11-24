"""Lab 17 — FRED/ALFRED point-in-time rates audit.

Run with: streamlit run asof_app.py
"""

from datetime import date
from io import StringIO

import pandas as pd
import requests
import streamlit as st


FRED_GRAPH_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
ALFRED_GRAPH_URL = (
    "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}"
    "&vintage_date={vintage_date}"
)
SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}


@st.cache_data(show_spinner=False, ttl=3600)
def download_current(series_id):
    """Download the latest FRED vintage for one series, without an API key."""
    response = requests.get(FRED_GRAPH_URL.format(series_id=series_id), timeout=30)
    response.raise_for_status()
    return read_fred_csv(response.text, series_id)


@st.cache_data(show_spinner=False, ttl=3600)
def download_as_known_on(series_id, vintage_date):
    """Download ALFRED observations available at the requested vintage date."""
    response = requests.get(
        ALFRED_GRAPH_URL.format(series_id=series_id, vintage_date=vintage_date), timeout=30
    )
    response.raise_for_status()
    return read_fred_csv(response.text, series_id)


def read_fred_csv(text, series_id):
    """Parse a public graph CSV and turn FRED's '.' missing marker into NaN."""
    frame = pd.read_csv(StringIO(text))
    if frame.shape[1] < 2 or "observation_date" not in frame.columns:
        raise ValueError(f"FRED did not return data for '{series_id}'. Check the series ID.")
    value_column = frame.columns[-1]
    frame = frame[["observation_date", value_column]].rename(
        columns={"observation_date": "date", value_column: "value"}
    )
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["value"] = pd.to_numeric(frame["value"].replace(".", pd.NA), errors="coerce")
    return frame.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)


def fred_link(series_id):
    return f"https://fred.stlouisfed.org/series/{series_id}"


def format_value(value):
    return "—" if pd.isna(value) else f"{value:,.3f}".rstrip("0").rstrip(".")


def audit_series(series_id, start_date, vintage_date):
    """Return one table row and the current chart data for a series."""
    current = download_current(series_id).dropna(subset=["value"])
    vintage = download_as_known_on(series_id, vintage_date.isoformat()).dropna(subset=["value"])
    start = pd.Timestamp(start_date)
    current_chart = current[current["date"] >= start].copy()
    vintage_chart = vintage[vintage["date"] >= start].copy()
    if vintage_chart.empty:
        raise ValueError(f"No non-missing {series_id} observations were known on {vintage_date:%Y-%m-%d}.")

    last_known = vintage_chart.iloc[-1]
    same_date_today = current.loc[current["date"] == last_known["date"], "value"]
    today_value = same_date_today.iloc[-1] if not same_date_today.empty else pd.NA
    late_count = int((current_chart["date"] > last_known["date"]).sum())
    paired = vintage_chart.merge(current, on="date", how="inner", suffixes=("_then", "_today"))
    revised_count = int((paired["value_then"].round(10) != paired["value_today"].round(10)).sum())
    row = {
        "Series": series_id,
        "Last date measured": last_known["date"].date(),
        "Value as known then": format_value(last_known["value"]),
        "Value today": format_value(today_value),
        "Values published later": late_count,
        "Values revised": revised_count,
    }
    return row, current_chart, last_known


def main():
    st.set_page_config(page_title="Point-in-Time Rates Audit", layout="wide")
    st.title("Point-in-Time Rates Audit")
    st.caption(
        "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded "
        f"{date.today():%d %B %Y}; built with AI help, a learning demonstration, not investment advice."
    )

    st.sidebar.header("Audit settings")
    selected = st.sidebar.multiselect(
        "Series", options=list(SERIES), default=list(SERIES), format_func=lambda item: f"{item} — {SERIES[item]}"
    )
    extra = st.sidebar.text_input("Add another FRED series ID", placeholder="Example: DGS3MO").strip().upper()
    if extra and extra not in selected:
        selected.append(extra)
    start_date = st.sidebar.date_input("Start date", value=date(2020, 1, 1))
    vintage_date = st.sidebar.date_input("As known on", value=date.today())

    if not selected:
        st.info("Choose at least one series ID.")
        return

    rows = []
    for series_id in selected:
        try:
            row, chart_data, last_known = audit_series(series_id, start_date, vintage_date)
        except (requests.RequestException, ValueError, pd.errors.ParserError) as error:
            st.error(f"{series_id}: {error}")
            continue
        label = SERIES.get(series_id, "Added FRED series")
        st.subheader(f"{series_id} — {label}")
        st.line_chart(chart_data.set_index("date")["value"], use_container_width=True)
        st.caption(
            f"Last date in the data known on {vintage_date:%d %B %Y}: "
            f"{last_known['date']:%d %B %Y} ({format_value(last_known['value'])})."
        )
        rows.append(row)

    if rows:
        table = pd.DataFrame(rows)
        table["Series"] = table["Series"].map(lambda item: f"[{item}]({fred_link(item)})")
        st.subheader("As-known audit table")
        st.markdown(table.to_markdown(index=False), unsafe_allow_html=True)
        st.caption(
            "Values published later counts non-missing latest-vintage observations after the last date known then. "
            "Values revised compares the ALFRED vintage with today's FRED values on the same observation dates."
        )


if __name__ == "__main__":
    main()
