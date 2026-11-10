import os
from contextlib import closing

import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def connect_db():
    credential_dir = os.environ["CREDENTIALS_DIRECTORY"]
    with open(os.path.join(credential_dir, "pgpass"), encoding="utf-8") as credential:
        password = credential.read().strip().rsplit(":", 1)[1]
    return psycopg2.connect(
        host="10.20.3.4",
        port=5432,
        dbname="notesdb",
        user="notes_app",
        password=password,
        sslmode="require",
        connect_timeout=5,
    )


@app.get("/notes")
def read_notes():
    with closing(connect_db()) as db:
        with db.cursor() as cursor:
            cursor.execute("SELECT id, body FROM public.notes ORDER BY id")
            notes = [{"id": row[0], "body": row[1]} for row in cursor.fetchall()]
    return jsonify(notes)


@app.post("/notes")
def save_note():
    data = request.get_json(silent=True)
    body = data.get("body") if isinstance(data, dict) else None
    if not isinstance(body, str) or not body.strip():
        return jsonify(error="Enter some note text"), 400

    body = body.strip()
    with closing(connect_db()) as db:
        with db, db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO public.notes (body) VALUES (%s) RETURNING id",
                (body,),
            )
            note_id = cursor.fetchone()[0]
    return jsonify(id=note_id, body=body), 201
