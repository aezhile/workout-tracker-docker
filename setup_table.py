import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="learning123"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS types (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        rest_seconds INTEGER
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS exercise_types (
        exercise_id INTEGER REFERENCES exercises(id),
        type_id INTEGER REFERENCES types(id)
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id SERIAL PRIMARY KEY,
        type_id INTEGER REFERENCES types(id),
        session_date DATE DEFAULT CURRENT_DATE
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS workout_logs (
        id SERIAL PRIMARY KEY,
        session_id INTEGER REFERENCES sessions(id),
        exercise_id INTEGER REFERENCES exercises(id),
        sets INTEGER,
        reps INTEGER,
        weight_kg NUMERIC,
        energy_level INTEGER,
        logged_at TIMESTAMP DEFAULT NOW()
    );
""")

conn.commit()
print("All tables created successfully.")

cur.close()
conn.close()