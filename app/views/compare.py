from pathlib import Path

import streamlit as st

from data_loader import DASHBOARD_YEARS


# =========================================================
# PATHS
# =========================================================

COMPARE_CSS_PATH = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    / "compare.css"
)


# =========================================================
# LOAD COMPARE CSS
# =========================================================

def load_compare_css():

    with open(
        COMPARE_CSS_PATH,
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
# COMPARE PAGE
# =========================================================

def render_compare_page(budget):

    load_compare_css()


    # =====================================================
    # PAGE INTRO
    # =====================================================

    st.html(
        """
        <section class="compare-page">

            <div class="compare-intro">

                <div class="compare-label">
                    Compare
                </div>

                <div class="compare-title">
                    How has funding changed?
                </div>

                <div class="compare-description">

                    Follow Seattle Central's S&A allocations
                    across three fiscal years and see how the
                    overall budget and individual programs
                    changed over time.

                </div>

            </div>

        </section>
        """
    )


    # =====================================================
    # PREPARE ALLOCATION DATA
    # =====================================================

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


    allocation_totals = (
        allocation_totals[
            allocation_totals[
                "fiscal_year"
            ]
            .isin(
                DASHBOARD_YEARS
            )
        ]
        .copy()
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


    # =====================================================
    # THREE-YEAR SNAPSHOT INTRO
    # =====================================================

    st.html(
        """
        <section class="compare-section-intro">

            <div class="compare-section-title">
                Three-year snapshot
            </div>

            <div class="compare-section-description">

                See how the total S&A allocation changed
                from FY2023–24 through FY2025–26.

            </div>

        </section>
        """
    )


    # =====================================================
    # THREE-YEAR SNAPSHOT CARDS
    # =====================================================

    with st.container(
        key="compare_snapshot_cards"
    ):

        cols = st.columns(
            3,
            gap="medium",
        )


        for index, (
            col,
            (_, row),
        ) in enumerate(
            zip(
                cols,
                allocation_totals.iterrows(),
            )
        ):

            fiscal_year = row[
                "fiscal_year"
            ]

            amount = row[
                "amount"
            ]


            # ---------------------------------------------
            # CHANGE FROM PREVIOUS YEAR
            # ---------------------------------------------

            if index == 0:

                change_text = (
                    "Starting year"
                )

            else:

                previous_amount = (
                    allocation_totals
                    .iloc[
                        index - 1
                    ]
                    ["amount"]
                )

                change_pct = (
                    (
                        amount
                        - previous_amount
                    )
                    / previous_amount
                    * 100
                )

                change_text = (
                    f"+{change_pct:.1f}% "
                    "from prior year"
                )


            # ---------------------------------------------
            # CARD
            # ---------------------------------------------

            with col:

                st.html(
                    f"""
                    <div class="compare-year-card">

                        <div class="compare-year">
                            FY{fiscal_year}
                        </div>

                        <div class="compare-year-value">
                            ${amount / 1_000_000:.2f}M
                        </div>

                        <div class="compare-year-note">
                            Total allocation
                        </div>

                        <div class="compare-year-change">
                            {change_text}
                        </div>

                    </div>
                    """
                )


    # =====================================================
    # PERIOD SUMMARY
    # =====================================================

    start_total = (
        allocation_totals
        .iloc[0]
        ["amount"]
    )

    latest_total = (
        allocation_totals
        .iloc[-1]
        ["amount"]
    )


    total_change = (
        latest_total
        - start_total
    )


    total_change_pct = (
        total_change
        / start_total
        * 100
    )


    st.html(
        f"""
        <section class="compare-summary">

            <div class="compare-summary-label">
                Across the three-year view
            </div>

            <div class="compare-summary-text">

                Total S&A allocation increased by

                <strong>
                    ${total_change:,.0f}
                </strong>

                from FY2023–24 to FY2025–26,
                a

                <strong>
                    {total_change_pct:.1f}%
                </strong>

                increase.

            </div>

        </section>
        """
    )


        # =====================================================
    # BIGGEST PROGRAM INCREASES
    # =====================================================

    start_year = "2023-24"
    end_year = "2025-26"


    program_allocations = (
        allocations[
            allocations[
                "fiscal_year"
            ]
            .isin(
                [
                    start_year,
                    end_year,
                ]
            )
        ]
        .pivot_table(
            index="program_name_standardized",
            columns="fiscal_year",
            values="amount",
            aggfunc="sum",
        )
        .reset_index()
    )


    # Keep only programs with numeric allocations
    # in both endpoint years.
    comparable_programs = (
        program_allocations
        .dropna(
            subset=[
                start_year,
                end_year,
            ]
        )
        .copy()
    )


    comparable_programs[
        "change"
    ] = (
        comparable_programs[
            end_year
        ]
        - comparable_programs[
            start_year
        ]
    )


    biggest_increases = (
        comparable_programs[
            comparable_programs[
                "change"
            ]
            > 0
        ]
        .sort_values(
            "change",
            ascending=False,
        )
        .head(5)
        .reset_index(
            drop=True
        )
    )


    # =====================================================
    # SECTION INTRO
    # =====================================================

    st.html(
        """
        <section class="compare-movers-intro">

            <div class="compare-section-title">
                Biggest funding increases
            </div>

            <div class="compare-section-description">

                Programs with the largest allocation increases
                from FY2023–24 to FY2025–26 among programs
                with comparable allocations in both years.

            </div>

        </section>
        """
    )


    # =====================================================
    # TOP 5 INCREASES
    # =====================================================

    with st.container(
        key="compare_increases"
    ):

        for rank, row in (
            biggest_increases
            .iterrows()
        ):

            program = row[
                "program_name_standardized"
            ]

            start_amount = row[
                start_year
            ]

            end_amount = row[
                end_year
            ]

            change = row[
                "change"
            ]


            st.html(
                f"""
                <div class="increase-row">

                    <div class="increase-rank">
                        {rank + 1}
                    </div>


                    <div class="increase-main">

                        <div class="increase-program">
                            {program}
                        </div>

                        <div class="increase-years">

                            FY2023–24
                            <strong>
                                ${start_amount:,.0f}
                            </strong>

                            <span class="increase-arrow">
                                →
                            </span>

                            FY2025–26
                            <strong>
                                ${end_amount:,.0f}
                            </strong>

                        </div>

                    </div>


                    <div class="increase-change">
                        +${change:,.0f}
                    </div>

                </div>
                """
            )