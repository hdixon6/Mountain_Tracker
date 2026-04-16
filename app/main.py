from __future__ import annotations

import os

from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db import Base, SessionLocal, engine
from app.models import Mountain, Review
from app.services import ExternalApiError, country_choices, fetch_mountains_by_country, validate_review

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
Base.metadata.create_all(bind=engine)


def get_or_create_mountain(session, mountain_id: int) -> Mountain | None:
    return session.get(Mountain, mountain_id)


@app.route("/health")
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@app.route("/", methods=["GET", "POST"])
def index():
    countries = country_choices()
    results: list[Mountain] = []
    selected_country = ""
    api_error = None

    if request.method == "POST":
        selected_country = request.form.get("country", "")

        if selected_country:
            try:
                fetched = fetch_mountains_by_country(selected_country, os.getenv("MOUNTAINS_API_KEY"))
                with SessionLocal() as session:
                    for item in fetched:
                        existing = None
                        if item.external_id:
                            existing = session.scalar(select(Mountain).where(Mountain.external_id == item.external_id))
                        if existing is None:
                            existing = session.scalar(
                                select(Mountain).where(
                                    Mountain.name == item.name,
                                    Mountain.country == item.country,
                                )
                            )
                        if existing is None:
                            existing = Mountain(
                                external_id=item.external_id,
                                name=item.name,
                                country=item.country,
                                elevation_m=item.elevation_m,
                            )
                            session.add(existing)
                        else:
                            existing.elevation_m = item.elevation_m
                    session.commit()
                    results = list(
                        session.scalars(
                            select(Mountain)
                            .where(Mountain.country == selected_country)
                            .order_by(Mountain.name.asc())
                        )
                    )
            except ExternalApiError:
                api_error = "Connection error, please try again."
        else:
            flash("Please choose a country.", "error")

    return render_template(
        "index.html",
        countries=countries,
        results=results,
        selected_country=selected_country,
        api_error=api_error,
    )


@app.route("/mountain/<int:mountain_id>")
def mountain_detail(mountain_id: int):
    with SessionLocal() as session:
        mountain = session.get(Mountain, mountain_id)
        if mountain is None:
            flash("Mountain not found.", "error")
            return redirect(url_for("index"))

        reviews = list(
            session.scalars(select(Review).where(Review.mountain_id == mountain_id).order_by(Review.id.desc()))
        )
        return render_template("detail.html", mountain=mountain, reviews=reviews)


@app.route("/mountain/<int:mountain_id>/review", methods=["POST"])
def add_review(mountain_id: int):
    rating = request.form.get("rating", "")
    review_text = request.form.get("review_text", "")
    errors = validate_review(rating, review_text)

    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("mountain_detail", mountain_id=mountain_id))

    with SessionLocal() as session:
        mountain = get_or_create_mountain(session, mountain_id)
        if mountain is None:
            flash("Mountain not found.", "error")
            return redirect(url_for("index"))

        review = Review(mountain_id=mountain_id, rating=int(rating), review_text=review_text.strip())
        session.add(review)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            flash("Could not save your review.", "error")
            return redirect(url_for("mountain_detail", mountain_id=mountain_id))

    flash("Review saved.", "success")
    return redirect(url_for("mountain_detail", mountain_id=mountain_id))
