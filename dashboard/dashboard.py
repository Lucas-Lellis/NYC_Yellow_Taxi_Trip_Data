from pathlib import Path

import pandas as pd
import streamlit as st

PAYMENT_LABELS = {
    "Credit Card": "Cartao de Credito",
    "Cash": "Dinheiro",
    "No Charge": "Sem Cobranca",
    "Dispute": "Disputa",
    "Unknown": "Desconhecido",
    "Voided Trip": "Viagem Cancelada",
}

DAY_LABELS = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terca-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sabado",
    "Sunday": "Domingo",
}

DAY_ORDER = [
    "Segunda-feira",
    "Terca-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sabado",
    "Domingo",
]

PARQUET_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "output"
    / "yellow_tripdata_2016-03_cleaned.parquet"
)


@st.cache_data(show_spinner="Lendo dados do Parquet...")
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df["payment_type"] = df["payment_type"].astype(str)
    df["payment_label"] = df["payment_type"].map(PAYMENT_LABELS).fillna("Outro")
    df["day_of_week"] = df["day_of_week"].replace(DAY_LABELS)
    return df


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar.expander("Filtros", expanded=False):
        hour_range = st.slider("Faixa de hora", 0, 23, (0, 23))

        vendor_options = sorted(df["VendorID"].unique().tolist())
        selected_vendors = st.multiselect(
            "Fornecedores",
            options=vendor_options,
            default=vendor_options,
        )

        payment_options = sorted(df["payment_label"].unique().tolist())
        selected_payments = st.multiselect(
            "Tipo de pagamento",
            options=payment_options,
            default=payment_options,
        )

    return df[
        df["hour_of_day"].between(hour_range[0], hour_range[1])
        & df["VendorID"].isin(selected_vendors)
        & df["payment_label"].isin(selected_payments)
    ]


def format_currency(value: float) -> str:
    value_str = f"{value:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
    return f"US$ {value_str}"


def format_currency_short(value: float) -> str:
    abs_value = abs(value)
    if abs_value >= 1_000_000_000:
        return f"US$ {value / 1_000_000_000:.1f}B"
    if abs_value >= 1_000_000:
        return f"US$ {value / 1_000_000:.1f}M"
    if abs_value >= 1_000:
        return f"US$ {value / 1_000:.1f}K"
    return format_currency(value)


def format_int(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def main() -> None:
    st.set_page_config(
        page_title="NYC Yellow Taxi - Painel ETL",
        page_icon="🚕",
        layout="wide",
    )

    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] { background: #fbfbfa; }
        [data-testid="stSidebar"] {
            background: #ffb511;
            min-width: 220px;
            max-width: 220px;
        }
        [data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }
        [data-testid="stSidebar"] .block-container { padding: 0.8rem 0.75rem; }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] label { color: #161616; }
        .taxi-logo { font-size: 3rem; text-align: center; margin: 0.3rem 0 1.2rem; }
        .page-title { color: #161616; font-size: 1.55rem; font-weight: 700; margin-bottom: 1.4rem; }
        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e6e6e6;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 3px rgba(0, 0, 0, 0.12);
            min-height: 106px;
        }
        [data-testid="stMetricLabel"] { color: #555555; }
        [data-testid="stMetricValue"] { color: #161616; font-size: 1.35rem; }
        .section-title { color: #161616; font-size: 1.05rem; font-weight: 700; margin: 1.5rem 0 0.55rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown('<div class="taxi-logo">🚕</div>', unsafe_allow_html=True)
    section = st.sidebar.radio(
        "Navegação",
        ["Hora", "Fornecedor", "Pagamento", "Dia da Semana"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="page-title">Dashboard - NYC Yellow Taxi</div>', unsafe_allow_html=True)

    df = load_data(PARQUET_PATH)
    filtered_df = filter_data(df)

    if filtered_df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        st.stop()

    col1, col2, col3, col4, col5 = st.columns(5)

    total_trips = len(filtered_df)
    total_revenue = float(filtered_df["total_amount"].sum())
    avg_fare = float(filtered_df["fare_amount"].mean())
    avg_distance = float(filtered_df["trip_distance"].mean())
    avg_tip_pct = float(filtered_df["tip_pct"].mean())

    col1.metric("Viagens", format_int(total_trips))
    col2.metric("Receita total", format_currency_short(total_revenue))
    col3.metric("Tarifa média", format_currency(avg_fare))
    col4.metric("Distância média", f"{avg_distance:.2f} mi")
    col5.metric("Gorjeta média", f"{avg_tip_pct:.2f}%")

    if section == "Hora":
        st.markdown('<div class="section-title">Viagens e tarifa por hora</div>', unsafe_allow_html=True)
        hourly = (
            filtered_df.groupby("hour_of_day", as_index=True)
            .agg(
                total_trips=("hour_of_day", "size"),
                avg_distance=("trip_distance", "mean"),
                avg_fare=("fare_amount", "mean"),
                avg_duration=("trip_duration_min", "mean"),
                avg_speed=("trip_speed_mph", "mean"),
                avg_tip_pct=("tip_pct", "mean"),
            )
            .sort_index()
            .round(2)
            .rename(
                columns={
                    "total_trips": "Total de viagens",
                    "avg_distance": "Distancia media (mi)",
                    "avg_fare": "Tarifa media (US$)",
                    "avg_duration": "Duracao media (min)",
                    "avg_speed": "Velocidade media (mph)",
                    "avg_tip_pct": "Gorjeta media (%)",
                }
            )
        )

        st.line_chart(hourly["Total de viagens"], use_container_width=True)
        st.markdown('<div class="section-title">Detalhamento por hora</div>', unsafe_allow_html=True)
        st.dataframe(hourly, use_container_width=True)

    elif section == "Fornecedor":
        st.markdown('<div class="section-title">Viagens por fornecedor</div>', unsafe_allow_html=True)
        vendor = (
            filtered_df.groupby("VendorID", as_index=True)
            .agg(
                total_trips=("VendorID", "size"),
                avg_distance=("trip_distance", "mean"),
                avg_fare=("fare_amount", "mean"),
                total_revenue=("total_amount", "sum"),
                avg_tip_pct=("tip_pct", "mean"),
                avg_speed=("trip_speed_mph", "mean"),
            )
            .round(2)
            .rename(
                columns={
                    "total_trips": "Total de viagens",
                    "avg_distance": "Distancia media (mi)",
                    "avg_fare": "Tarifa media (US$)",
                    "total_revenue": "Receita total (US$)",
                    "avg_tip_pct": "Gorjeta media (%)",
                    "avg_speed": "Velocidade media (mph)",
                }
            )
        )

        st.bar_chart(vendor["Total de viagens"], use_container_width=True)
        st.markdown('<div class="section-title">Detalhamento por fornecedor</div>', unsafe_allow_html=True)
        st.dataframe(vendor, use_container_width=True)

    elif section == "Pagamento":
        st.markdown('<div class="section-title">Viagens por tipo de pagamento</div>', unsafe_allow_html=True)
        payment = (
            filtered_df.groupby("payment_label", as_index=True)
            .agg(
                total_trips=("payment_label", "size"),
                avg_fare=("fare_amount", "mean"),
                avg_tip=("tip_amount", "mean"),
                avg_tip_pct=("tip_pct", "mean"),
                total_revenue=("total_amount", "sum"),
            )
            .round(2)
            .rename(
                columns={
                    "total_trips": "Total de viagens",
                    "avg_fare": "Tarifa media (US$)",
                    "avg_tip": "Gorjeta media (US$)",
                    "avg_tip_pct": "Gorjeta media (%)",
                    "total_revenue": "Receita total (US$)",
                }
            )
        )
        payment["% de viagens"] = (
            (payment["Total de viagens"] / payment["Total de viagens"].sum()) * 100
        ).round(2)

        st.bar_chart(payment["Total de viagens"], use_container_width=True)
        st.markdown('<div class="section-title">Detalhamento por pagamento</div>', unsafe_allow_html=True)
        st.dataframe(payment, use_container_width=True)

    else:
        st.markdown('<div class="section-title">Viagens por dia da semana</div>', unsafe_allow_html=True)
        weekday = (
            filtered_df.groupby("day_of_week", as_index=True)
            .agg(
                total_trips=("day_of_week", "size"),
                avg_distance=("trip_distance", "mean"),
                avg_fare=("fare_amount", "mean"),
                avg_duration=("trip_duration_min", "mean"),
                avg_tip_pct=("tip_pct", "mean"),
            )
            .round(2)
            .rename(
                columns={
                    "total_trips": "Total de viagens",
                    "avg_distance": "Distancia media (mi)",
                    "avg_fare": "Tarifa media (US$)",
                    "avg_duration": "Duracao media (min)",
                    "avg_tip_pct": "Gorjeta media (%)",
                }
            )
        )
        weekday = weekday.reindex(DAY_ORDER)

        st.bar_chart(weekday["Total de viagens"], use_container_width=True)
        st.markdown('<div class="section-title">Detalhamento por dia</div>', unsafe_allow_html=True)
        st.dataframe(weekday, use_container_width=True)


if __name__ == "__main__":
    main()