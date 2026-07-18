# Workout Tracker — Dockerized PostgreSQL + Streamlit

A self-built, full-stack workout tracking application, created as a hands-on project to learn Docker, relational database design, Python, and Streamlit from the ground up. Rather than following a tutorial end-to-end, the schema, tooling choices, and features were designed and reasoned through independently — including several iterations after identifying design flaws along the way.

## What it does

- Log workouts (sets, reps, weight, energy level) through a Streamlit web interface
- Data is scoped to real exercises available at a specific gym, tagged with the actual equipment on hand
- Automatically groups a session's logged exercises by muscle group
- Highlights which muscles (for the selected workout type) haven't been trained yet in the current session
- Runs entirely locally, no paid services or subscriptions required

## Why this project

This was built as a practical way to learn concepts that are hard to absorb from documentation alone — containerization, relational schema design (normalization, foreign keys, many-to-many relationships), and building a usable interface on top of a real database. Every design decision below reflects an actual point where the schema was reworked after finding a flaw in the original approach — a deliberate part of the learning process, not an afterthought.

## Tech stack

- **Docker** — runs PostgreSQL in an isolated, disposable container; no local Postgres installation needed
- **PostgreSQL** — relational database
- **Python (psycopg2)** — application logic and database access
- **Streamlit** — interactive web interface, no HTML/CSS/JS required
- **python-dotenv** — keeps database credentials out of source code and version control

## Schema design

The database went through more than one redesign as the data model became clearer:

- Started as a single flat table, then normalized into reference tables once repeated text values (exercise names, workout types) became a data-integrity risk
- **Reference tables** (`types`, `categories`, `muscles`, `equipment`) hold controlled, rarely-changing values — similar in spirit to an Excel dropdown list, but enforced by the database itself
- **Many-to-many relationships** (an exercise can target multiple muscles, use multiple equipment pieces, and belong to multiple workout-day types) are modeled with dedicated bridge tables, rather than cramming multiple values into one column
- Rest time is stored on `categories` (Compound/Isolation/Cardio/Isometric) rather than on individual exercises, after recognizing it was actually determined by movement category, not by the specific exercise — avoiding the same fact being duplicated in two places

**Tables:** `types`, `categories`, `exercises`, `exercise_types`, `muscles`, `exercise_muscles`, `equipment`, `exercise_equipment`, `sessions`, `workout_logs`

## Setup

1. Clone the repo
2. Create a `.env` file in the project root:
   ```
   DB_PASSWORD=your_password_here
   ```
3. Start the database:
   ```
   docker run --name workout-db -e POSTGRES_PASSWORD=your_password_here -p 5432:5432 -d postgres
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the schema and data setup scripts (`setuptable.py`, then `insert_data.py` / `insert_exercises.py`)
6. Launch the app:
   ```
   streamlit run app.py
   ```

## Notes

- The exercise list reflects a real gym's available equipment, not a generic dataset — a deliberate choice to make the tool something actually usable day to day
- `workout_tracker_journal.ipynb` documents the full build process, including the reasoning behind each schema decision, for anyone wanting the "why" behind the code

## Roadmap

- [ ] Add charts (workout-type distribution, muscle training frequency over time)
- [ ] Cross-reference against a larger public exercise dataset for broader coverage
- [ ] Rebuild the analysis layer in a BI tool (Power BI / Tableau) as a companion project
