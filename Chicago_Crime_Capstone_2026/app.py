"""
Chicago Crime Capstone - Flask Application

Displays crime statistics, analytical charts
and Police District CRUD operations.
"""

import sqlite3
from contextlib import closing
from flask import Flask, render_template
from config import Config, DATABASE_PATH, validate_project_files
from src.district_routes import district_bp


# 1. INITIALIZE FLASK APPLICATION

app = Flask(__name__)
app.config.from_object(Config)

# Register Police District CRUD routes.
app.register_blueprint(district_bp)


# 2. DATABASE CONNECTION

def get_db_connection():
    """Connect to SQLite and access columns by name."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# 3. DASHBOARD STATISTICS

def get_dashboard_data():
    """Retrieve the statistics required for dashboard KPI cards."""

    with closing(get_db_connection()) as conn:

        # 3A. Count total crime records and recorded arrests.
        totals = conn.execute("""
            SELECT COUNT(*) AS total_crimes,
                   SUM(CASE WHEN arrest = 1 THEN 1 ELSE 0 END)
                       AS total_arrests
            FROM crime_records
        """).fetchone()

        total_crimes = totals["total_crimes"]
        total_arrests = totals["total_arrests"] or 0

        # Calculate arrest percentage and prevent division by zero.
        arrest_rate = (
            round(total_arrests * 100 / total_crimes, 2)
            if total_crimes else 0
        )

        # 3B. Count distinct crime categories using the SQL view.
        category_count = conn.execute("""
            SELECT COUNT(*)
            FROM vw_crime_by_category
        """).fetchone()[0]

        # 3C. Identify the most frequently recorded crime category.
        top_crime = conn.execute("""
            SELECT primary_type, crime_count, percentage
            FROM vw_crime_by_category
            ORDER BY crime_count DESC, primary_type
            LIMIT 1
        """).fetchone()

        # Return only the statistics required by dashboard.html.
        return {
            "total_crimes": total_crimes,
            "total_arrests": total_arrests,
            "arrest_rate": arrest_rate,
            "category_count": category_count,
            "top_crime": dict(top_crime) if top_crime else None
        }


# 4. ANALYTICAL CHARTS

def get_dashboard_charts():
    """Reference the charts generated during the four use cases."""

    charts = [
        ("Yearly Crime Trend", "crime_trend_over_years.png"),

        ("Top 10 Crime Categories", "top_10_crime_categories.png"),

        ("Monthly and Weekday Crime Distribution",
         "crime_month_weekday_heatmap.png"),

        ("Top 10 Community Areas", "top10_communities.png"),

        ("Hourly Crime Distribution", "crime_hourly_distribution.png"),

        ("Community Crime Distribution", "community_crime_boxplot.png"),

        ("Crime Correlation Heatmap", "crime_correlation_heatmap.png"),

        ("SQL Yearly Crime Report", "sql_yearly_crime_report.png"),

        ("SQL Crime Category Report", "sql_crime_category_report.png")
    ]

    # Convert chart titles and filenames into template-friendly dictionaries.
    return [
        {"title": title, "file": filename}
        for title, filename in charts
    ]


# 5. DASHBOARD ROUTE

@app.route("/")
def dashboard():
    """Display crime statistics, charts and individual chart insights."""

    return render_template(
        "dashboard.html",
        data=get_dashboard_data(),
        charts=get_dashboard_charts()
    )


# 6. START FLASK APPLICATION

if __name__ == "__main__":
    validate_project_files()
    app.run(debug=True)