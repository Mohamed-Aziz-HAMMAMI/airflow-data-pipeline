import pandas as pd
from sqlalchemy import text
from database import engine


def _destination_clause(destination: str | None = None):
    """
    Returns a (where_sql, params) pair. When destination is empty/None,
    where_sql is "" and the query runs unfiltered.
    Matches against departure/arrival airport name and IATA code.
    """
    if not destination:
        return "", {}

    where_sql = """
        WHERE (
            departure_airport ILIKE :dest
            OR arrival_airport ILIKE :dest
            OR departure_iata ILIKE :dest
            OR arrival_iata ILIKE :dest
        )
    """
    return where_sql, {"dest": f"%{destination.strip()}%"}


def get_total_flights(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    query = text(f"""
        SELECT COUNT(*) AS total
        FROM flights_data
        {where_sql};
    """)
    return pd.read_sql(query, engine, params=params)


def get_total_airlines(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    query = text(f"""
        SELECT COUNT(DISTINCT airline_name) AS total
        FROM flights_data
        {where_sql};
    """)
    return pd.read_sql(query, engine, params=params)


def get_total_departure_airports(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    query = text(f"""
        SELECT COUNT(DISTINCT departure_iata) AS total
        FROM flights_data
        {where_sql};
    """)
    return pd.read_sql(query, engine, params=params)


def get_average_departure_delay(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    base_condition = "departure_delay IS NOT NULL"
    connector = "AND" if where_sql else "WHERE"
    query = text(f"""
        SELECT ROUND(AVG(departure_delay), 2) AS avg_delay
        FROM flights_data
        {where_sql}
        {connector} {base_condition};
    """)
    return pd.read_sql(query, engine, params=params)


def get_flights_by_airline(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    query = text(f"""
        SELECT
            airline_name,
            COUNT(*) AS flights
        FROM flights_data
        {where_sql}
        GROUP BY airline_name
        ORDER BY flights DESC;
    """)
    return pd.read_sql(query, engine, params=params)


def get_flight_status(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    query = text(f"""
        SELECT
            flight_status,
            COUNT(*) AS flights
        FROM flights_data
        {where_sql}
        GROUP BY flight_status
        ORDER BY flights DESC;
    """)
    return pd.read_sql(query, engine, params=params)


def get_departure_airports(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    query = text(f"""
        SELECT
            departure_iata,
            COUNT(*) AS flights
        FROM flights_data
        {where_sql}
        GROUP BY departure_iata
        ORDER BY flights DESC
        LIMIT 10;
    """)
    return pd.read_sql(query, engine, params=params)


def get_arrival_airports(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    query = text(f"""
        SELECT
            arrival_iata,
            COUNT(*) AS flights
        FROM flights_data
        {where_sql}
        GROUP BY arrival_iata
        ORDER BY flights DESC
        LIMIT 10;
    """)
    return pd.read_sql(query, engine, params=params)


def get_departure_delay(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    base_condition = "departure_delay IS NOT NULL"
    connector = "AND" if where_sql else "WHERE"
    query = text(f"""
        SELECT
            airline_name,
            ROUND(AVG(departure_delay), 2) AS avg_delay
        FROM flights_data
        {where_sql}
        {connector} {base_condition}
        GROUP BY airline_name
        ORDER BY avg_delay DESC;
    """)
    return pd.read_sql(query, engine, params=params)


def get_arrival_delay(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    base_condition = "arrival_delay IS NOT NULL"
    connector = "AND" if where_sql else "WHERE"
    query = text(f"""
        SELECT
            airline_name,
            ROUND(AVG(arrival_delay), 2) AS avg_delay
        FROM flights_data
        {where_sql}
        {connector} {base_condition}
        GROUP BY airline_name
        ORDER BY avg_delay DESC;
    """)
    return pd.read_sql(query, engine, params=params)


def get_aircraft_distribution(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    base_condition = "aircraft IS NOT NULL"
    connector = "AND" if where_sql else "WHERE"
    query = text(f"""
        SELECT
            aircraft,
            COUNT(*) AS flights
        FROM flights_data
        {where_sql}
        {connector} {base_condition}
        GROUP BY aircraft
        ORDER BY flights DESC
        LIMIT 10;
    """)
    return pd.read_sql(query, engine, params=params)


def get_delay_scatter(destination: str | None = None):
    where_sql, params = _destination_clause(destination)
    base_condition = "departure_delay IS NOT NULL AND arrival_delay IS NOT NULL"
    connector = "AND" if where_sql else "WHERE"
    query = text(f"""
        SELECT
            departure_delay,
            arrival_delay
        FROM flights_data
        {where_sql}
        {connector} {base_condition};
    """)
    return pd.read_sql(query, engine, params=params)