"""Simple SQLite helper for storing generated charts."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, Iterable, Optional


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "charts.db"


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS charts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payload TEXT NOT NULL,
                houses TEXT NOT NULL,
                extra TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def insert_chart(payload: Dict[str, Any], houses: Iterable[Dict[str, Any]], extra: Dict[str, Any]) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO charts(payload, houses, extra) VALUES (?, ?, ?)",
            (json.dumps(payload), json.dumps(list(houses)), json.dumps(extra)),
        )
        return int(cursor.lastrowid)


def fetch_chart(chart_id: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT id, payload, houses, extra, created_at FROM charts WHERE id=?",
            (chart_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "payload": json.loads(row[1]),
            "houses": json.loads(row[2]),
            "extra": json.loads(row[3]),
            "created_at": row[4],
        }


def list_charts(limit: int = 20) -> Iterable[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT id, payload, houses, extra, created_at FROM charts ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        for row in cursor.fetchall():
            yield {
                "id": row[0],
                "payload": json.loads(row[1]),
                "houses": json.loads(row[2]),
                "extra": json.loads(row[3]),
                "created_at": row[4],
            }
