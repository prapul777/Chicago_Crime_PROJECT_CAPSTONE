"""
Police District Management - Chicago Crime Capstone

GET    : Retrieve a specific record by its unique identifier.
POST   : Create a new district record.
PUT    : Update all editable fields of an existing district.
PATCH  : Update selected fields without modifying remaining fields.
DELETE : Remove a specific district using its unique identifier.
SEARCH : Retrieve records matching the specified search criteria.
"""

import sqlite3
from contextlib import closing
from flask import Blueprint, flash, jsonify, redirect
from flask import render_template, request, url_for
from config import DATABASE_PATH


district_bp = Blueprint("districts", __name__)


# Fields permitted for creation and modification.
EDITABLE_FIELDS = (
    "district_name", "address", "city",
    "state", "zip", "phone"
)


# Original database columns and their display labels.
DISTRICT_FIELDS = {
    "district_code": "District Code",
    "district_name": "District Name",
    "address": "Address",
    "city": "City",
    "state": "State",
    "zip": "ZIP Code",
    "website": "Website",
    "phone": "Phone Number",
    "fax": "Fax Number",
    "tty": "TTY",
    "x_coordinate": "X Coordinate",
    "y_coordinate": "Y Coordinate",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "location": "Location"
}


# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

def get_connection():
    """Connect to SQLite and enable foreign key protection."""

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# ============================================================
# 2. COMMON FUNCTIONS
# ============================================================

def get_district_record(district_code):
    """Retrieve a specific district using its unique primary key."""

    with closing(get_connection()) as conn:

        row = conn.execute(
            """
            SELECT *
            FROM police_districts
            WHERE district_code = ?
            """,
            (district_code,)
        ).fetchone()

    return dict(row) if row else None


def get_input_data():
    """Accept JSON requests or HTML form values."""

    if request.is_json:
        data = request.get_json(silent=True)
        return data if isinstance(data, dict) else {}

    return request.form.to_dict()


def clean_fields(data):
    """Restrict modifications to permitted fields."""

    return {
        field: str(data[field]).strip()
        for field in EDITABLE_FIELDS
        if field in data and data[field] is not None
    }


def api_response(message, status, district_code):
    """Return JSON results with appropriate HTTP status codes."""

    if status >= 400:
        return jsonify({"error": message}), status

    return jsonify({
        "message": message,
        "district_code": district_code
    }), status


def browser_response(message, status,
                     endpoint="districts.list_districts", **kwargs):
    """Display feedback and redirect browser users."""

    flash(message, "success" if status < 400 else "error")

    return redirect(url_for(endpoint, **kwargs))


def render_district_page(mode="create", selected=None):
    """Display police districts with optional search filtering."""

    search = request.args.get("search", "").strip()

    with closing(get_connection()) as conn:

        if search:
            keyword = f"%{search}%"

            # Search records across multiple district fields.
            districts = conn.execute("""
                SELECT *
                FROM police_districts
                WHERE CAST(district_code AS TEXT) LIKE ?
                   OR district_name LIKE ?
                   OR address LIKE ?
                   OR city LIKE ?
                   OR CAST(zip AS TEXT) LIKE ?
                ORDER BY district_code
            """, (keyword,) * 5).fetchall()

        else:
            # Display all districts when no keyword is entered.
            districts = conn.execute("""
                SELECT *
                FROM police_districts
                ORDER BY district_code
            """).fetchall()

    return render_template(
        "districts.html",
        districts=districts,
        mode=mode,
        selected=selected,
        district_fields=DISTRICT_FIELDS,
        editable_fields=EDITABLE_FIELDS,
        search=search
    )


def show_district(district_code, mode):
    """Load a specific district for the selected operation."""

    district = get_district_record(district_code)

    if district is None:
        return browser_response("District not found.", 404)

    return render_district_page(mode, district)


# ============================================================
# 3. GET - RETRIEVE DISTRICT RECORDS
# ============================================================

# Display all districts and support keyword-based searching.
@district_bp.route("/districts", methods=["GET"])
def list_districts():

    return render_district_page()


# GET: Retrieve a district using a manually entered unique identifier.
@district_bp.route("/districts/get", methods=["GET"])
def retrieve_district():

    # Read the district code entered in the GET form.
    district_code = request.args.get("district_code", type=int)

    # Validate the entered unique identifier.
    if district_code is None or district_code <= 0:

        return browser_response(
            "Please enter a valid district code.",
            400
        )

    # Retrieve the exact record using its primary key.
    return show_district(district_code, "view")


# GET: Retrieve a district directly from the existing records table.
@district_bp.route("/districts/<int:district_code>",
                   methods=["GET"])
def district_details(district_code):

    return show_district(district_code, "view")


# GET API: Retrieve a specific district in JSON format.
@district_bp.route("/api/districts/<int:district_code>",
                   methods=["GET"])
def get_district(district_code):

    district = get_district_record(district_code)

    if district is None:
        return jsonify({"error": "District not found."}), 404

    return jsonify(district)


# ============================================================
# 4. POST - CREATE A NEW DISTRICT
# ============================================================

@district_bp.route("/districts", methods=["POST"])
def create_district():

    data = get_input_data()
    fields = clean_fields(data)

    # Validate the unique district code.
    try:
        district_code = int(
            str(data.get("district_code", "")).strip()
        )

    except (TypeError, ValueError):
        district_code = 0

    # Validate mandatory fields.
    if district_code <= 0 or not fields.get("district_name"):

        message, status = (
            "Valid district code and name are required.",
            400
        )

    else:
        try:
            # Parameterized insertion prevents SQL injection.
            with closing(get_connection()) as conn, conn:

                conn.execute("""
                    INSERT INTO police_districts
                    (district_code, district_name, address,
                     city, state, zip, phone)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    district_code,
                    *[
                        fields.get(field, "")
                        for field in EDITABLE_FIELDS
                    ]
                ))

            message, status = (
                "POST: District created successfully.",
                201
            )

        except sqlite3.IntegrityError:

            message, status = (
                "District code already exists or data is invalid.",
                409
            )

        except sqlite3.Error:

            message, status = (
                "Unable to create district.",
                500
            )

    if request.is_json:
        return api_response(message, status, district_code)

    return browser_response(message, status)


# ============================================================
# 5. COMMON UPDATE FUNCTION FOR PUT AND PATCH
# ============================================================

def modify_district(district_code, fields, full_update=False):
    """Update permitted columns while preserving other details."""

    # PUT requires all editable fields.
    # PATCH accepts selected editable fields.
    if full_update and not all(
        field in fields for field in EDITABLE_FIELDS
    ):
        return "All editable fields are required.", 400

    if not fields:
        return "No valid fields provided.", 400

    if "district_name" in fields and not fields["district_name"]:
        return "District name cannot be empty.", 400

    # Build SQL assignments using permitted column names.
    assignments = ", ".join(
        f"{field} = ?" for field in fields
    )

    values = list(fields.values()) + [district_code]

    try:
        with closing(get_connection()) as conn, conn:

            cursor = conn.execute(
                f"""
                UPDATE police_districts
                SET {assignments}
                WHERE district_code = ?
                """,
                values
            )

            if cursor.rowcount == 0:
                return "District not found.", 404

        return "District updated successfully.", 200

    except sqlite3.IntegrityError:

        return "Invalid district information.", 409

    except sqlite3.Error:

        return "Unable to update district.", 500


# ============================================================
# 6. PUT - FULL UPDATE OF EDITABLE FIELDS
# ============================================================

# Display the PUT form for the selected district.
@district_bp.route("/districts/<int:district_code>/edit",
                   methods=["GET"])
def edit_district_form(district_code):

    return show_district(district_code, "edit")


# Process the full-update HTML form without JavaScript.
@district_bp.route("/districts/<int:district_code>/edit",
                   methods=["POST"])
def save_district_edit(district_code):

    fields = clean_fields(get_input_data())

    message, status = modify_district(
        district_code,
        fields,
        full_update=True
    )

    if status != 200:

        return browser_response(
            message,
            status,
            "districts.edit_district_form",
            district_code=district_code
        )

    return browser_response(
        "PUT operation: All editable fields updated successfully.",
        status
    )


# PUT API: Update all editable fields using the unique identifier.
@district_bp.route("/api/districts/<int:district_code>",
                   methods=["PUT"])
def update_district(district_code):

    fields = clean_fields(get_input_data())

    message, status = modify_district(
        district_code,
        fields,
        full_update=True
    )

    if status == 200:

        message = (
            "PUT: All editable fields updated successfully."
        )

    return api_response(message, status, district_code)


# ============================================================
# 7. PATCH - PARTIAL UPDATE OF SELECTED FIELDS
# ============================================================

# Display the PATCH form for the selected district.
@district_bp.route("/districts/<int:district_code>/patch",
                   methods=["GET"])
def patch_district_form(district_code):

    return show_district(district_code, "patch")


# Process only modified fields from the HTML form.
@district_bp.route("/districts/<int:district_code>/patch",
                   methods=["POST"])
def save_district_patch(district_code):

    existing = get_district_record(district_code)

    if existing is None:

        return browser_response(
            "District not found.",
            404
        )

    fields = clean_fields(get_input_data())

    # Compare submitted values with existing database values.
    # Include only changed fields in the partial update.
    changed_fields = {
        field: value
        for field, value in fields.items()
        if value != (
            str(existing[field]).strip()
            if existing.get(field) is not None else ""
        )
    }

    if not changed_fields:

        return browser_response(
            "No changes detected.",
            400,
            "districts.patch_district_form",
            district_code=district_code
        )

    message, status = modify_district(
        district_code,
        changed_fields,
        full_update=False
    )

    if status != 200:

        return browser_response(
            message,
            status,
            "districts.patch_district_form",
            district_code=district_code
        )

    # Display the names of modified fields.
    updated_fields = ", ".join(
        DISTRICT_FIELDS[field]
        for field in changed_fields
    )

    return browser_response(
        f"PATCH operation: Updated {updated_fields} successfully.",
        status
    )


# PATCH API: Update only the supplied editable fields.
@district_bp.route("/api/districts/<int:district_code>",
                   methods=["PATCH"])
def patch_district(district_code):

    fields = clean_fields(get_input_data())

    message, status = modify_district(
        district_code,
        fields,
        full_update=False
    )

    if status == 200:

        updated_fields = ", ".join(
            DISTRICT_FIELDS[field]
            for field in fields
        )

        message = (
            f"PATCH: Updated {updated_fields} successfully."
        )

    return api_response(message, status, district_code)


# ============================================================
# 8. DELETE - REMOVE A SPECIFIC DISTRICT
# ============================================================

def remove_district(district_code):
    """Delete a district only when no crime records reference it."""

    try:
        with closing(get_connection()) as conn, conn:

            # Prevent concurrent writes during reference checking.
            conn.execute("BEGIN IMMEDIATE")

            # Verify that the district exists.
            existing = conn.execute(
                """
                SELECT 1
                FROM police_districts
                WHERE district_code = ?
                """,
                (district_code,)
            ).fetchone()

            if existing is None:

                return "District not found.", 404

            # Identify the district reference column.
            columns = {
                row["name"]
                for row in conn.execute(
                    "PRAGMA table_info(crime_records)"
                )
            }

            if "district_code" in columns:

                district_column = "district_code"

            elif "district" in columns:

                district_column = "district"

            else:

                return "Unable to verify crime references.", 409

            # Protect existing crime records before deletion.
            linked = conn.execute(
                f"""
                SELECT 1
                FROM crime_records
                WHERE {district_column} = ?
                LIMIT 1
                """,
                (district_code,)
            ).fetchone()

            if linked:

                return (
                    "Cannot delete a district linked to crime records.",
                    409
                )

            # Delete the unreferenced district using its unique identifier.
            conn.execute(
                """
                DELETE FROM police_districts
                WHERE district_code = ?
                """,
                (district_code,)
            )

        return "District deleted successfully.", 200

    except sqlite3.IntegrityError:

        return "Cannot delete a referenced district.", 409

    except sqlite3.Error:

        return "Unable to delete district.", 500


# Display the DELETE confirmation form.
@district_bp.route("/districts/<int:district_code>/delete",
                   methods=["GET"])
def delete_district_form(district_code):

    return show_district(district_code, "delete")


# Process deletion through an HTML confirmation form.
@district_bp.route("/districts/<int:district_code>/delete",
                   methods=["POST"])
def confirm_district_delete(district_code):

    message, status = remove_district(district_code)

    if status == 200:

        message = (
            "DELETE operation: District deleted successfully."
        )

    return browser_response(message, status)


# DELETE API: Remove a district using its unique identifier.
@district_bp.route("/api/districts/<int:district_code>",
                   methods=["DELETE"])
def delete_district(district_code):

    message, status = remove_district(district_code)

    if status == 200:

        message = "DELETE: District deleted successfully."

    return api_response(message, status, district_code)