import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

plt.style.use("seaborn-v0_8-whitegrid")

COLOR = "#2E86AB"
ACCENT = "#E63946"


def airline_chart(df: pd.DataFrame, top_n: int = 15):
    d = df.dropna(subset=["airline_name", "flights"]).copy()
    d["airline_name"] = d["airline_name"].astype(str)
    d = d.sort_values(by="flights", ascending=False).head(top_n)
    d = d.sort_values(by="flights", ascending=True)

    fig, ax = plt.subplots(figsize=(8, max(4, 0.4 * len(d))))
    ax.barh(d["airline_name"], d["flights"], color=COLOR)
    ax.set_title(f"Top {len(d)} Airlines by Flights", fontsize=14, fontweight="bold")
    ax.set_xlabel("Flights")
    ax.tick_params(axis="y", labelsize=9)
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    fig.tight_layout()
    return fig


def status_chart(df: pd.DataFrame):
    d = df.dropna(subset=["flight_status", "flights"]).sort_values(by="flights", ascending=False)

    fig, ax = plt.subplots(figsize=(6, 5))
    cmap = plt.get_cmap("Set2")
    colors = [cmap(i / max(len(d) - 1, 1)) for i in range(len(d))]
    ax.pie(
        d["flights"].tolist(),
        labels=d["flight_status"].astype(str).tolist(),
        autopct="%1.0f%%",
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.45, edgecolor="white"),
    )
    ax.set_title("Flight Status Breakdown", fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig


def departure_airport_chart(df: pd.DataFrame):
    return _airport_chart(df, "departure_iata", "Top Departure Airports")


def arrival_airport_chart(df: pd.DataFrame):
    return _airport_chart(df, "arrival_iata", "Top Arrival Airports")


def _airport_chart(df: pd.DataFrame, col: str, title: str):
    d = df.dropna(subset=[col, "flights"]).copy()
    d[col] = d[col].astype(str)
    d = d.sort_values(by="flights", ascending=True)

    fig, ax = plt.subplots(figsize=(8, max(4, 0.4 * len(d))))
    ax.barh(d[col], d["flights"], color=COLOR)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Flights")
    ax.tick_params(axis="y", labelsize=9)
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    fig.tight_layout()
    return fig


def departure_delay_chart(df: pd.DataFrame, top_n: int = 15):
    return _delay_chart(df, "Average Departure Delay", top_n)


def arrival_delay_chart(df: pd.DataFrame, top_n: int = 15):
    return _delay_chart(df, "Average Arrival Delay", top_n)


def _delay_chart(df: pd.DataFrame, title: str, top_n: int = 15):
    d = df.dropna(subset=["airline_name", "avg_delay"]).copy()
    d["airline_name"] = d["airline_name"].astype(str)
    d = d.reindex(d["avg_delay"].abs().sort_values(ascending=False).index).head(top_n)
    d = d.sort_values(by="avg_delay", ascending=True)
    colors = [ACCENT if v >= 0 else COLOR for v in d["avg_delay"]]

    fig, ax = plt.subplots(figsize=(8, max(4, 0.4 * len(d))))
    ax.barh(d["airline_name"], d["avg_delay"], color=colors)
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.set_title(f"{title} (Top {len(d)} by Magnitude)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Minutes")
    ax.tick_params(axis="y", labelsize=9)
    fig.tight_layout()
    return fig


def delay_scatter(df: pd.DataFrame):
    d = df.dropna(subset=["departure_delay", "arrival_delay"])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(d["departure_delay"], d["arrival_delay"], alpha=0.5, color=COLOR, edgecolor="white", linewidth=0.3)
    ax.axhline(0, color="#999999", linewidth=0.8)
    ax.axvline(0, color="#999999", linewidth=0.8)
    ax.set_title("Departure Delay vs Arrival Delay", fontsize=14, fontweight="bold")
    ax.set_xlabel("Departure delay (min)")
    ax.set_ylabel("Arrival delay (min)")
    fig.tight_layout()
    return fig