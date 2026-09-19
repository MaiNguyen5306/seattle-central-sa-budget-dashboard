from pathlib import Path

import streamlit as st

from data_loader import (
    DASHBOARD_YEARS,
    load_budget_data,
)

from charts import (
    build_allocation_trend,
    build_program_ranking,
)


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Seattle Central S&A Budget",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# PATHS + CSS
# ---------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent

css_path = APP_DIR / "styles.css"

with open(
    css_path,
    "r",
    encoding="utf-8",
) as css_file:
    st.html(
        f"<style>{css_file.read()}</style>"
    )


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def render_metric_card(
    label,
    value,
    note,
):
    st.html(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                {label}
            </div>

            <div class="metric-value">
                {value}
            </div>

            <div class="metric-note">
                {note}
            </div>
        </div>
        """
    )


def render_page_header(
    title,
    description,
):
    st.html(
        """
        <div class="eyebrow">
            S&A Budget Explorer
        </div>
        """
    )

    st.html(
        f"""
        <div class="page-title">
            {title}
        </div>
        """
    )

    st.html(
        f"""
        <div class="page-description">
            {description}
        </div>
        """
    )


def render_section_header(
    title,
    description,
):
    st.html(
        f"""
        <div class="section-title">
            {title}
        </div>

        <div class="section-description">
            {description}
        </div>
        """
    )


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

budget = load_budget_data()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.html(
        """
        <div style="
            font-size:1.35rem;
            font-weight:750;
            margin-bottom:0.2rem;
            color:#FFFFFF;
        ">
            S&A Budget
        </div>

        <div style="
            font-size:0.82rem;
            color:#B9C0CC;
            margin-bottom:1.6rem;
        ">
            Seattle Central College
        </div>
        """
    )

    selected_page = st.radio(
        "Explore",
        [
            "Budget Overview",
            "Compare Across Years",
            "Request vs Allocation",
            "Program Explorer",
            "Data & Methodology",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.caption(
        "Historical S&A budget research dashboard."
    )


# ---------------------------------------------------------
# BUDGET OVERVIEW
# ---------------------------------------------------------

if selected_page == "Budget Overview":

    render_page_header(
        title="Where does student activity funding go?",
        description=(
            "Explore Seattle Central College's Services and "
            "Activities fee allocations across three fiscal "
            "years, from FY2023–24 through FY2025–26."
        ),
    )


    # -----------------------------------------------------
    # ALLOCATIONS
    # -----------------------------------------------------

    allocations = budget[
        (
            budget["metric_type"]
            == "allocation"
        )
        &
        (
            budget["amount"].notna()
        )
    ].copy()


    allocation_totals = (
        allocations
        .groupby(
            "fiscal_year",
            as_index=False,
        )
        ["amount"]
        .sum()
    )


    fiscal_order = {
        year: index
        for index, year
        in enumerate(DASHBOARD_YEARS)
    }

    allocation_totals["year_order"] = (
        allocation_totals[
            "fiscal_year"
        ].map(fiscal_order)
    )

    allocation_totals = (
        allocation_totals
        .sort_values("year_order")
        .drop(columns="year_order")
        .reset_index(drop=True)
    )


    start_year = "2023-24"
    latest_year = "2025-26"

    start_total = allocation_totals.loc[
        allocation_totals["fiscal_year"]
        == start_year,
        "amount",
    ].iloc[0]

    latest_total = allocation_totals.loc[
        allocation_totals["fiscal_year"]
        == latest_year,
        "amount",
    ].iloc[0]


    period_growth = (
        (
            latest_total
            - start_total
        )
        / start_total
        * 100
    )


    latest_programs = allocations[
        allocations["fiscal_year"]
        == latest_year
    ].copy()


    funded_programs = (
        latest_programs[
            latest_programs["amount"] > 0
        ]
        ["program_name_standardized"]
        .nunique()
    )


    largest_program = (
        latest_programs[
            latest_programs["amount"] > 0
        ]
        .sort_values(
            "amount",
            ascending=False,
        )
        .iloc[0]
    )


    largest_share = (
        largest_program["amount"]
        / latest_total
        * 100
    )


    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(
        4,
        gap="medium",
    )

    with col1:
        render_metric_card(
            label="FY2025–26 Allocation",
            value=f"${latest_total / 1_000_000:.2f}M",
            note="Total S&A allocation",
        )

    with col2:
        render_metric_card(
            label="Change Since FY2023–24",
            value=f"+{period_growth:.1f}%",
            note=(
                f"+${latest_total - start_total:,.0f} "
                "across the three-year view"
            ),
        )

    with col3:
        render_metric_card(
            label="Funded Programs",
            value=str(funded_programs),
            note=(
                "Programs with a positive "
                "FY2025–26 allocation"
            ),
        )

    with col4:
        render_metric_card(
            label="Largest Allocation",
            value=(
                f"${largest_program['amount'] / 1000:.1f}K"
            ),
            note=(
                f"{largest_program['program_name_standardized']}"
                f" · {largest_share:.1f}% of budget"
            ),
        )


    # -----------------------------------------------------
    # TREND
    # -----------------------------------------------------

    render_section_header(
        title="Total allocation over time",
        description=(
            "Overall S&A allocation from FY2023–24 "
            "through FY2025–26."
        ),
    )

    trend_fig = build_allocation_trend(
        allocation_totals
    )

    st.plotly_chart(
        trend_fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


    # -----------------------------------------------------
    # PROGRAM RANKING
    # -----------------------------------------------------

    render_section_header(
        title="Where the money goes",
        description=(
            "The ten largest program allocations "
            "for the selected fiscal year."
        ),
    )


    selected_year = st.selectbox(
        "Fiscal year",
        DASHBOARD_YEARS,
        index=2,
    )


    selected_year_data = allocations[
        allocations["fiscal_year"]
        == selected_year
    ].copy()


    ranking_fig = build_program_ranking(
        selected_year_data
    )


    st.plotly_chart(
        ranking_fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# ---------------------------------------------------------
# PLACEHOLDER PAGES
# ---------------------------------------------------------

else:

    render_page_header(
        title=selected_page,
        description=(
            "This section will be built after the "
            "Budget Overview design is finalized."
        ),
    )

    st.info(
        "Draft page — coming next."
    )