import plotly.express as px
import plotly.graph_objects as go


ALLOCATION_COLOR = "#168C8C"
REQUEST_COLOR = "#7257D6"

TEXT_COLOR = "#172033"
MUTED_TEXT = "#6B7280"

GRID_COLOR = "#E8E6E1"
CARD_COLOR = "#FFFFFF"
BACKGROUND_COLOR = "#F7F6F2"


def apply_chart_theme(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial, sans-serif",
            color=TEXT_COLOR,
            size=13,
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#D9D6CF",
            font=dict(
                color=TEXT_COLOR,
                size=13,
            ),
        ),
    )

    return fig


def build_allocation_trend(allocation_totals):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=allocation_totals["fiscal_year"],
            y=allocation_totals["amount"],
            mode="lines+markers+text",
            line=dict(
                color=ALLOCATION_COLOR,
                width=4,
            ),
            marker=dict(
                size=11,
                color=ALLOCATION_COLOR,
                line=dict(
                    color="#FFFFFF",
                    width=2,
                ),
            ),
            text=[
                f"${value / 1_000_000:.2f}M"
                for value in allocation_totals["amount"]
            ],
            textposition="top center",
            textfont=dict(
                color=TEXT_COLOR,
                size=12,
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Allocation: $%{y:,.2f}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        height=360,
        margin=dict(
            l=15,
            r=20,
            t=45,
            b=20,
        ),
        showlegend=False,
    )

    fig.update_xaxes(
        title=None,
        showgrid=False,
        tickfont=dict(
            color=TEXT_COLOR,
        ),
        linecolor="#D9D6CF",
    )

    fig.update_yaxes(
        title=None,
        gridcolor=GRID_COLOR,
        zeroline=False,
        tickprefix="$",
        tickformat=".2s",
        tickfont=dict(
            color=MUTED_TEXT,
        ),
    )

    return apply_chart_theme(fig)


def build_program_ranking(year_data):
    chart_data = (
        year_data[
            year_data["amount"] > 0
        ]
        .sort_values(
            "amount",
            ascending=False,
        )
        .head(10)
        .sort_values(
            "amount",
            ascending=True,
        )
        .copy()
    )

    fig = px.bar(
        chart_data,
        x="amount",
        y="program_name_standardized",
        orientation="h",
    )

    fig.update_traces(
        marker_color=ALLOCATION_COLOR,
        marker_line_width=0,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Allocation: $%{x:,.2f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        height=500,
        margin=dict(
            l=15,
            r=20,
            t=15,
            b=25,
        ),
        showlegend=False,
    )

    fig.update_xaxes(
        title=None,
        gridcolor=GRID_COLOR,
        zeroline=False,
        tickprefix="$",
        tickformat=".2s",
        tickfont=dict(
            color=MUTED_TEXT,
        ),
    )

    fig.update_yaxes(
        title=None,
        tickfont=dict(
            color=TEXT_COLOR,
            size=12,
        ),
    )

    return apply_chart_theme(fig)