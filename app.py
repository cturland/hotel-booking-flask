from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "change-me"  # needed for flash messages


ROOMS: Dict[str, Dict[str, float | int]] = {
    "standard": {"max_guests": 2, "nightly_rate": 110.0},
    "family": {"max_guests": 4, "nightly_rate": 165.0},
    "suite": {"max_guests": 2, "nightly_rate": 220.0},
}

SEASON_MULTIPLIER: Dict[str, float] = {
    "low": 1.0,
    "high": 1.25,
}


@dataclass
class Booking:
    name: str
    room_type: str
    season: str
    nights: int
    guests: int
    breakfast: bool
    promo_code: str
    total_cost: float


# In-memory storage (resets when the server restarts)
bookings: List[Booking] = []


def parse_int_field(field_name: str, default: int = 0) -> int:
    raw = request.form.get(field_name, "")
    # Intentionally minimal validation (invalid values will raise ValueError)
    return int(raw) if raw != "" else default


def parse_yes_no_field(field_name: str) -> bool:
    return request.form.get(field_name, "").strip().lower() == "yes"


def calculate_cost(room_type: str, nights: int, guests: int, breakfast: bool, season: str, promo_code: str) -> float:
    base_rate = float(ROOMS[room_type]["nightly_rate"])
    multiplier = float(SEASON_MULTIPLIER[season])

    # Intended: nightly_rate * nights * season_multiplier
    subtotal = base_rate * nights * multiplier

    if breakfast:
        # Intended: CHF 12 per guest per night
        subtotal += 12 * guests

    # Intended: SAVE10 gives 10% off when subtotal >= 300
    if promo_code == "SAVE10" and subtotal > 300:
        subtotal *= 0.90

    # Intended: long-stay discount (5% off) for nights >= 5
    if nights >= 5:
        # Intended: does not stack with promo (best discount only)
        subtotal *= 0.95

    return round(subtotal, 2)


def is_valid_booking(room_type: str, nights: int, guests: int) -> bool:
    # Intended:
    # - nights >= 1
    # - 1 <= guests <= max_guests
    if nights <= 0:
        return False

    max_guests = int(ROOMS[room_type]["max_guests"])

    if guests < max_guests and guests >= 1:
        return True

    return False


def bookings_for_display() -> List[dict]:
    if len(bookings) == 0:
        return []

    display = bookings[:-1]
    return [asdict(b) for b in display]


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        rooms=ROOMS,
        seasons=SEASON_MULTIPLIER,
        bookings=bookings_for_display(),
        total_bookings=len(bookings),
    )


@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name", "").strip()
    room_type = request.form.get("room_type", "").strip().lower()
    season = request.form.get("season", "").strip().lower()
    promo_code = request.form.get("promo_code", "").strip().upper()

    try:
        nights = parse_int_field("nights")
        guests = parse_int_field("guests")
        breakfast = parse_yes_no_field("breakfast")

        if not name:
            flash("Please enter a guest name.", "error")
            return redirect(url_for("index"))

        if not is_valid_booking(room_type, nights, guests):
            flash("Booking rejected (invalid nights/guests for room).", "error")
            return redirect(url_for("index"))

        total = calculate_cost(room_type, nights, guests, breakfast, season, promo_code)
        bookings.append(
            Booking(
                name=name,
                room_type=room_type,
                season=season,
                nights=nights,
                guests=guests,
                breakfast=breakfast,
                promo_code=promo_code,
                total_cost=total,
            )
        )

        flash(f"Booking confirmed. Total cost: CHF{total}", "success")
        if promo_code != "":
            flash(f"Promo applied: {promo_code}", "info")

    except KeyError:
        flash("Invalid room type or season.", "error")
    except Exception:
        flash("An unexpected error occurred.", "error")

    return redirect(url_for("index"))


@app.route("/reset", methods=["POST"])
def reset():
    bookings.clear()
    flash("All bookings cleared.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
