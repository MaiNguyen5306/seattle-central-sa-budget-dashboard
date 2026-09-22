from pathlib import Path
import base64

import streamlit as st

from data_loader import (
    DASHBOARD_YEARS,
    load_budget_data,
)

from charts import (
    build_allocation_trend,
    build_program_ranking,
)
from views.compare import render_compare_page

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Seattle Central S&A Budget",
    page_icon="🐯",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# PATHS
# =========================================================

APP_DIR = Path(__file__).resolve().parent

CSS_PATH = APP_DIR / "styles.css"

MASCOT_PATH = (
    APP_DIR
    / "assets"
    / "tiger_mascot.png"
)


# =========================================================
# LOAD CSS
# =========================================================

with open(
    CSS_PATH,
    "r",
    encoding="utf-8",
) as css_file:

    st.html(
        f"""
        <style>
        {css_file.read()}
        </style>
        """
    )


# =========================================================
# IMAGE HELPER
# =========================================================

def image_to_base64(path):

    return base64.b64encode(
        path.read_bytes()
    ).decode()


mascot_base64 = image_to_base64(
    MASCOT_PATH
)


# =========================================================
# LOAD DATA
# =========================================================

budget = load_budget_data()


# =========================================================
# PAGE ROUTING
# =========================================================

VALID_SECTIONS = {
    "home",
    "compare",
    "requests",
    "programs",
    "about",
}


section = st.query_params.get(
    "section",
    "home",
)


if isinstance(section, list):
    section = section[0]


if section not in VALID_SECTIONS:
    section = "home"


# =========================================================
# NAVIGATION
# =========================================================

def go_to_section(section_name):

    st.query_params["section"] = section_name

    st.rerun()


def render_navigation():

    with st.container(
        key="top_nav"
    ):

        (
            brand_col,
            compare_col,
            requests_col,
            programs_col,
            about_col,
        ) = st.columns(
            [
                7.2,
                1,
                1,
                1,
                1,
            ],
            vertical_alignment="center",
        )


        with brand_col:

            if st.button(
                "S&A BUDGET EXPLORER",
                key="nav_home",
                type="tertiary",
            ):

                go_to_section(
                    "home"
                )


        with compare_col:

            if st.button(
                "COMPARE",
                key="nav_compare",
                type=(
                    "primary"
                    if section == "compare"
                    else "secondary"
                ),
                use_container_width=True,
            ):

                go_to_section(
                    "compare"
                )


        with requests_col:

            if st.button(
                "REQUESTS",
                key="nav_requests",
                type=(
                    "primary"
                    if section == "requests"
                    else "secondary"
                ),
                use_container_width=True,
            ):

                go_to_section(
                    "requests"
                )


        with programs_col:

            if st.button(
                "PROGRAMS",
                key="nav_programs",
                type=(
                    "primary"
                    if section == "programs"
                    else "secondary"
                ),
                use_container_width=True,
            ):

                go_to_section(
                    "programs"
                )


        with about_col:

            if st.button(
                "ABOUT",
                key="nav_about",
                type=(
                    "primary"
                    if section == "about"
                    else "secondary"
                ),
                use_container_width=True,
            ):

                go_to_section(
                    "about"
                )


# =========================================================
# HELPERS
# =========================================================

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


# =========================================================
# HOME PAGE
# =========================================================

def render_home():

    # -----------------------------------------------------
    # LANDING HERO
    # -----------------------------------------------------

    st.html(
        f"""
        <section class="hero-shell">

            <img
                class="hero-mascot-corner"
                src="data:image/png;base64,{mascot_base64}"
                alt="Student-designed tiger mascot"
            >


            <div class="hero-main">

                <div class="hero-copy">

                    <div class="hero-college">
                        Seattle Central College
                    </div>


                    <div class="hero-title">
                        Where does student activity funding go?
                    </div>


                    <div class="hero-description">

                        Explore Seattle Central College's
                        Services and Activities fee allocations
                        across three fiscal years, from
                        FY2023–24 through FY2025–26.

                    </div>


                    <div class="hero-credit">

                        A student-created S&A Fee Committee
                        research dashboard.

                    </div>


                    <a
                        href="#overview"
                        class="hero-cta"
                    >
                        Let's Explore
                    </a>

                </div>

            </div>

        </section>
        """
    )


    # -----------------------------------------------------
    # OVERVIEW ANCHOR
    # -----------------------------------------------------

    st.html(
        """
        <div id="overview"></div>
        """
    )


    # -----------------------------------------------------
    # ALLOCATION DATA
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
        in enumerate(
            DASHBOARD_YEARS
        )
    }


    allocation_totals[
        "year_order"
    ] = (
        allocation_totals[
            "fiscal_year"
        ]
        .map(
            fiscal_order
        )
    )


    allocation_totals = (
        allocation_totals
        .sort_values(
            "year_order"
        )
        .drop(
            columns="year_order"
        )
        .reset_index(
            drop=True
        )
    )


    start_year = "2023-24"
    latest_year = "2025-26"


    start_total = (
        allocation_totals.loc[
            allocation_totals[
                "fiscal_year"
            ]
            == start_year,
            "amount",
        ]
        .iloc[0]
    )


    latest_total = (
        allocation_totals.loc[
            allocation_totals[
                "fiscal_year"
            ]
            == latest_year,
            "amount",
        ]
        .iloc[0]
    )


    period_growth = (
        (
            latest_total
            - start_total
        )
        / start_total
        * 100
    )


    latest_programs = allocations[
        allocations[
            "fiscal_year"
        ]
        == latest_year
    ].copy()


    funded_programs = (
        latest_programs[
            latest_programs[
                "amount"
            ] > 0
        ]
        [
            "program_name_standardized"
        ]
        .nunique()
    )


    largest_program = (
        latest_programs[
            latest_programs[
                "amount"
            ] > 0
        ]
        .sort_values(
            "amount",
            ascending=False,
        )
        .iloc[0]
    )


    largest_share = (
        largest_program[
            "amount"
        ]
        / latest_total
        * 100
    )


    # -----------------------------------------------------
    # MAIN OVERVIEW WIDTH
    # -----------------------------------------------------

    (
        left_space,
        main_content,
        right_space,
    ) = st.columns(
        [
            0.07,
            0.86,
            0.07,
        ]
    )


    with main_content:

        # -------------------------------------------------
        # OVERVIEW INTRO
        # -------------------------------------------------

        st.html(
            """
            <div class="overview-intro">

                <div class="overview-eyebrow">
                    Budget Overview
                </div>

                <div class="overview-title">
                    Three years of S&A funding
                </div>

                <div class="overview-description">

                    Start with the overall size of the budget,
                    then explore which programs received the
                    largest allocations.

                </div>

            </div>
            """
        )


        # -------------------------------------------------
        # KPI CARDS
        # -------------------------------------------------

        col1, col2, col3, col4 = (
            st.columns(
                4,
                gap="medium",
            )
        )


        with col1:

            render_metric_card(
                label="FY2025–26 Allocation",
                value=(
                    f"${latest_total / 1_000_000:.2f}M"
                ),
                note="Total S&A allocation",
            )


        with col2:

            render_metric_card(
                label="Change Since FY2023–24",
                value=(
                    f"+{period_growth:.1f}%"
                ),
                note=(
                    f"+${latest_total - start_total:,.0f} "
                    "across the three-year view"
                ),
            )


        with col3:

            render_metric_card(
                label="Funded Programs",
                value=str(
                    funded_programs
                ),
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


        # -------------------------------------------------
        # TOTAL ALLOCATION TREND
        # -------------------------------------------------

        render_section_header(
            title="Total allocation over time",
            description=(
                "Overall S&A allocation from "
                "FY2023–24 through FY2025–26."
            ),
        )


        trend_fig = (
            build_allocation_trend(
                allocation_totals
            )
        )


        st.plotly_chart(
            trend_fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
        )


        # -------------------------------------------------
        # WHERE THE MONEY GOES
        # -------------------------------------------------

        render_section_header(
            title="Where the money goes",
            description=(
                "The ten largest program allocations "
                "for the selected fiscal year."
            ),
        )


        selected_year = (
            st.selectbox(
                "Fiscal year",
                DASHBOARD_YEARS,
                index=2,
            )
        )


        selected_year_data = (
            allocations[
                allocations[
                    "fiscal_year"
                ]
                == selected_year
            ]
            .copy()
        )


        ranking_fig = (
            build_program_ranking(
                selected_year_data
            )
        )


        st.plotly_chart(
            ranking_fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
        )


    st.html(
        """
        <div class="page-footer-space"></div>
        """
    )


# =========================================================
# PLACEHOLDER SUBPAGE
# =========================================================

def render_placeholder_page(
    label,
    title,
    description,
):

    st.html(
        f"""
        <main class="subpage-shell">

            <div class="subpage-label">
                {label}
            </div>

            <div class="subpage-title">
                {title}
            </div>

            <div class="subpage-description">
                {description}
            </div>

            <div class="subpage-placeholder">
                This section will be designed and built next.
            </div>

        </main>
        """
    )


# =========================================================
# RENDER CURRENT PAGE
# =========================================================

render_navigation()


if section == "home":

    render_home()


elif section == "compare":

    render_compare_page(
        budget
    )

elif section == "requests":

    render_placeholder_page(
        label="Requests",
        title="What was requested — and what was allocated?",
        description=(
            "Explore program funding requests, final allocations, "
            "funding gaps, and decision-year outcomes."
        ),
    )


elif section == "programs":

    render_placeholder_page(
        label="Programs",
        title="Explore one program at a time",
        description=(
            "Follow individual programs across years and understand "
            "their allocations, requests, budget share, and "
            "organizational changes."
        ),
    )


elif section == "about":

    render_placeholder_page(
        label="About",
        title="Why this project exists",
        description=(
            "Learn about the project's inspiration, data sources, "
            "methodology, limitations, and the questions behind "
            "this student-created research dashboard."
        ),
    )