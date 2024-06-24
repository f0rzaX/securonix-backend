import os
import pickle
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
import numpy as np
import pandas as pd
from flask import current_app as app


data_bp = Blueprint("data", __name__)


# let user upload a file
@data_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    email = get_jwt_identity()
    user_folder = os.path.join(app.config["UPLOAD_FOLDER"], email)

    # create dir if it doesn't exist
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # filename is based on the email
    file_extension = os.path.splitext(file.filename)[1]
    new_filename = email + file_extension
    file_path = os.path.join(user_folder, new_filename)

    # make pandas DataFrame and save it as a pickle
    df = pd.read_excel(file)
    pickle_path = os.path.splitext(file_path)[0] + ".pkl"
    with open(pickle_path, "wb") as f:
        pickle.dump(df, f)

    return jsonify({"message": "File uploaded and processed successfully"})


@data_bp.route("/data", methods=["GET", "POST"])
@jwt_required()
def get_data():
    request_data = request.get_json() or {}
    current_page = request_data.get("page", 1)
    search = request_data.get("query", "")
    filters = request_data.get("filters", {})

    email = get_jwt_identity()

    # construct pickle file path using email
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], email, f"{email}.pkl")

    if not os.path.exists(file_path):
        return jsonify({"error": "DataFrame not found"}), 404

    # get back the pandas DataFrame from the pickle file
    with open(file_path, "rb") as f:
        df = pickle.load(f)

    # apply filters
    for column, filter_value in filters.items():

        # case where the column is of string type
        if isinstance(filter_value, list) and filter_value:
            df = df[df[column].isin(filter_value)]

        # case where the column is of numeric type
        elif isinstance(filter_value, dict):
            min_val = float(filter_value.get("min"))
            max_val = float(filter_value.get("max"))
            if min_val is not None:
                df = df[df[column] >= min_val]
            if max_val is not None:
                df = df[df[column] <= max_val]

    # helper function to check if a string is numeric
    def is_numeric(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    # support search
    if search:
        search_term_is_numeric = is_numeric(search)

        # case where the search term is numeric
        if search_term_is_numeric:
            search = float(search)
            numeric_df = df.select_dtypes(include=[np.number])
            search_query = numeric_df.apply(lambda x: x == search).any(axis=1)

        # case where the search term is a string
        else:
            search = search.lower()
            # convert all columns to string, concatenate them, and do a case insensitive search
            all_columns = (
                df.astype(str).apply(lambda x: " ".join(x), axis=1).str.lower()
            )
            search_query = all_columns.str.contains(search)

        df = df[search_query]

    # replace NaN with None
    df = df.replace({np.nan: None})

    rows_per_page = app.config["ROWS_PER_PAGE"]
    start_row = (current_page - 1) * rows_per_page
    end_row = min(start_row + rows_per_page, len(df))
    total_rows = len(df)
    total_pages = (total_rows + rows_per_page - 1) // rows_per_page
    data = df.iloc[start_row:end_row].to_dict(orient="records")

    columns = [
        {
            "name": col,
            "type": "number" if pd.api.types.is_numeric_dtype(df[col]) else "string",
        }
        for col in df.columns
    ]

    # consists of columns, their data, and pagination info
    response = {
        "columns": columns,
        "data": data,
        "pagination": {
            "current_page": current_page,
            "total_pages": total_pages,
            "rows_per_page": rows_per_page,
            "total_rows": total_rows,
            "end_row": end_row,
        },
    }

    return jsonify(response)


# give user all available filters
@data_bp.route("/filters", methods=["GET"])
@jwt_required()
def filters():
    # construct pickle file path using email
    email = get_jwt_identity()
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], email, f"{email}.pkl")

    if not os.path.exists(file_path):
        return jsonify({"error": "DataFrame not found"}), 404

    # get back the pandas DataFrame from the pickle file
    with open(file_path, "rb") as f:
        df = pickle.load(f)

    filters = {}

    for column in df.columns:
        if df[column].dtype == "object":
            # Column is of string type
            filters[column] = {"type": "string", "values": df[column].unique().tolist()}
        elif pd.api.types.is_numeric_dtype(df[column]):
            # Column is of numeric type
            filters[column] = {
                "type": "number",
                "min": df[column].min().item(),
                "max": df[column].max().item(),
            }

    return jsonify(filters), 200
