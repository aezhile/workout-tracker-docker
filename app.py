import streamlit as st
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
st.title("My Workout Tracker")

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="postgres",
    user="postgres", password=os.getenv("DB_PASSWORD")
)
cur = conn.cursor()

# Step 1: Pick the workout type (outside any form, so it reacts immediately)
cur.execute("SELECT id, name FROM types ORDER BY name;")
types_data = cur.fetchall()
type_names = [row[1] for row in types_data]

st.header("1. Start a Session")
selected_type = st.selectbox("What are you training today?", type_names)
type_id = [row[0] for row in types_data if row[1] == selected_type][0]

if st.button("Start / Continue Session"):
    cur.execute("""
        SELECT id FROM sessions
        WHERE type_id = %s AND session_date = CURRENT_DATE;
    """, (type_id,))
    existing = cur.fetchone()

    if existing:
        st.session_state.session_id = existing[0]
    else:
        cur.execute("""
            INSERT INTO sessions (type_id, session_date)
            VALUES (%s, CURRENT_DATE) RETURNING id;
        """, (type_id,))
        st.session_state.session_id = cur.fetchone()[0]
        conn.commit()

    st.session_state.current_type = selected_type

# Step 2: Only show the logging form once a session has started
if "session_id" in st.session_state:
    st.success(f"Session active: {st.session_state.current_type} (Session ID: {st.session_state.session_id})")

    st.header("2. Log an Exercise")

    # Filtered exercises based on the selected type
    cur.execute("""
        SELECT e.id, e.name
        FROM exercises e
        JOIN exercise_types et ON e.id = et.exercise_id
        JOIN types t ON et.type_id = t.id
        WHERE t.name = %s
        ORDER BY e.name;
    """, (st.session_state.current_type,))
    filtered_exercises = cur.fetchall()
    filtered_names = [row[1] for row in filtered_exercises]

    with st.form("log_form", clear_on_submit=True):
        selected_exercise = st.selectbox("Exercise:", filtered_names)
        sets = st.number_input("Sets", min_value=1, max_value=20, value=3)
        reps = st.number_input("Reps", min_value=1, max_value=50, value=10)
        weight = st.number_input("Weight (kg)", min_value=0.0, value=20.0, step=2.5)
        energy = st.slider("Energy level (1-10)", 1, 10, 5)
        submitted = st.form_submit_button("Add to Session")

    if submitted:
        exercise_id = [row[0] for row in filtered_exercises if row[1] == selected_exercise][0]
        cur.execute("""
            INSERT INTO workout_logs (session_id, exercise_id, sets, reps, weight_kg, energy_level)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (st.session_state.session_id, exercise_id, sets, reps, weight, energy))
        conn.commit()
        st.success(f"Added {selected_exercise} to today's session!")

    # Show everything logged in this session so far
    st.header("3. Today's Progress by Muscle")
    cur.execute("""
        SELECT mu.name AS muscle, e.name AS exercise, wl.sets, wl.reps, wl.weight_kg
        FROM workout_logs wl
        JOIN exercises e ON wl.exercise_id = e.id
        JOIN exercise_muscles em ON e.id = em.exercise_id
        JOIN muscles mu ON em.muscle_id = mu.id
        WHERE wl.session_id = %s
        ORDER BY mu.name, e.name;
    """, (st.session_state.session_id,))
    muscle_rows = cur.fetchall()

    # Group rows by muscle name
    muscles_done = {}
    for muscle, exercise, sets, reps, weight in muscle_rows:
        if muscle not in muscles_done:
            muscles_done[muscle] = []
        muscles_done[muscle].append(f"{exercise} ({sets}x{reps} @ {weight}kg)")

    for muscle, exercise_list in muscles_done.items():
        st.subheader(muscle)
        for item in exercise_list:
            st.write(f"- {item}")

    st.header("4. Muscles Not Yet Hit Today")
    cur.execute("""
        SELECT DISTINCT mu.name
        FROM exercises e
        JOIN exercise_types et ON e.id = et.exercise_id
        JOIN types t ON et.type_id = t.id
        JOIN exercise_muscles em ON e.id = em.exercise_id
        JOIN muscles mu ON em.muscle_id = mu.id
        WHERE t.name = %s

        EXCEPT

        SELECT DISTINCT mu.name
        FROM workout_logs wl
        JOIN exercise_muscles em ON wl.exercise_id = em.exercise_id
        JOIN muscles mu ON em.muscle_id = mu.id
        WHERE wl.session_id = %s;
    """, (st.session_state.current_type, st.session_state.session_id))

    remaining_muscles = cur.fetchall()

    if remaining_muscles:
        for row in remaining_muscles:
            st.write(f"- {row[0]}")
    else:
        st.write("You've hit every muscle available for this type today!")


cur.close()
conn.close()