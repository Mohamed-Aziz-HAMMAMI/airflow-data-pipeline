import streamlit as st

from queries import *
from charts import *

st.set_page_config(page_title="Flight Analytics Dashboard", layout="wide", page_icon="✈️")

st.title("✈️ Flight Analytics Dashboard")


st.markdown("### Filter")
destination_filter = st.text_input(
    "Airport or IATA code",
    placeholder="e.g. Singapore, JFK",
    help="Filters every chart and KPI below by departure or arrival airport."
)
if destination_filter:
    st.caption(f"Showing results matching **{destination_filter}**")

# KPIs
c1, c2, c3, c4 = st.columns(4)

c1.metric("Flights", get_total_flights(destination_filter)["total"][0])
c2.metric("Airlines", get_total_airlines(destination_filter)["total"][0])
c3.metric("Departure Airports", get_total_departure_airports(destination_filter)["total"][0])

avg_delay = get_average_departure_delay(destination_filter)["avg_delay"][0]
c4.metric(
    "Avg Departure Delay",
    f"{avg_delay} min" if avg_delay is not None else "N/A"
)

st.divider()

tab_overview, tab_airports, tab_delays = st.tabs(
    ["📊 Overview", "🛫 Airports", "⏱️ Delays"]
)

with tab_overview:
    flights_by_airline = get_flights_by_airline(destination_filter)
    flight_status = get_flight_status(destination_filter)

    if flights_by_airline.empty and flight_status.empty:
        st.info("No flights match this filter yet.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(airline_chart(flights_by_airline))
        with col2:
            st.pyplot(status_chart(flight_status))

with tab_airports:
    departure_airports = get_departure_airports(destination_filter)
    arrival_airports = get_arrival_airports(destination_filter)

    if departure_airports.empty and arrival_airports.empty:
        st.info("No airports match this filter yet.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(departure_airport_chart(departure_airports))
        with col2:
            st.pyplot(arrival_airport_chart(arrival_airports))

with tab_delays:
    departure_delay = get_departure_delay(destination_filter)
    arrival_delay = get_arrival_delay(destination_filter)
    delay_scatter_data = get_delay_scatter(destination_filter)

    if departure_delay.empty and arrival_delay.empty:
        st.info("No delay data matches this filter yet.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(departure_delay_chart(departure_delay))
        with col2:
            st.pyplot(arrival_delay_chart(arrival_delay))

        if not delay_scatter_data.empty:
            st.pyplot(delay_scatter(delay_scatter_data))