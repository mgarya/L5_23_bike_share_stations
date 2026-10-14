"""Manage stations in a small bike-share network.

This module demonstrates CRUD-style operations using SQLite and safe SQL parameters.
"""

import secrets
import sqlite3

CONNECTION = sqlite3.connect(":memory:")
CONNECTION.execute(
    """
    CREATE TABLE stations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        capacity INTEGER NOT NULL CHECK (capacity > 0),
        bikes INTEGER NOT NULL CHECK (bikes >= 0 AND bikes <= capacity)
    )
    """
)


def add_station(name, capacity, bikes, log=None):
    """Register a station and append its name to a caller-provided log."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Station name must be a non-empty string.")
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
        raise ValueError("Capacity must be a positive integer.")
    if (
        not isinstance(bikes, int)
        or isinstance(bikes, bool)
        or not 0 <= bikes <= capacity
    ):
        raise ValueError("Bikes must be an integer between zero and capacity.")

    CONNECTION.execute(
        "INSERT INTO stations (name, capacity, bikes) VALUES (?, ?, ?)",
        (name.strip(), capacity, bikes),
    )
    if log is None:
        log = []
    log.append(name.strip())
    return log


def rent_bike(station_id):
    """Rent one bike from a station; return True only if a bike was rented."""
    row = CONNECTION.execute(
        "SELECT bikes FROM stations WHERE id = ?", (station_id,)
    ).fetchone()
    if row is None or row[0] <= 0:
        return False

    CONNECTION.execute(
        "UPDATE stations SET bikes = bikes - 1 WHERE id = ?", (station_id,)
    )
    return True


def unlock_pin():
    """Generate a cryptographically strong four-digit PIN."""
    return secrets.randbelow(9000) + 1000


def full_stations():
    """Return names of stations where all bike docks are occupied by bikes."""
    rows = CONNECTION.execute(
        "SELECT name FROM stations WHERE bikes = capacity ORDER BY id"
    ).fetchall()
    return [row[0] for row in rows]


def reset_station(station_id):
    """Reset the bike count for a station; return whether it existed."""
    cursor = CONNECTION.execute(
        "UPDATE stations SET bikes = 0 WHERE id = ?", (station_id,)
    )
    return cursor.rowcount == 1


def has_bikes(station_id):
    """Return True if an existing station has at least one bike."""
    row = CONNECTION.execute(
        "SELECT bikes FROM stations WHERE id = ?", (station_id,)
    ).fetchone()
    return row is not None and row[0] > 0


def main():
    """Run a short demonstration of the station manager."""
    add_station("Central Park", 10, 10)
    add_station("Metro Gate", 8, 2)
    print(rent_bike(2), rent_bike(9))
    print(unlock_pin(), full_stations(), has_bikes(2))
    print("Reset station 1:", reset_station(1))


if __name__ == "__main__":
    main()
