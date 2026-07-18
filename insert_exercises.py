import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password=os.getenv("DB_PASSWORD")
)
cur = conn.cursor()

# Each exercise: name, category, list of day-types, list of muscles, list of equipment
# Equipment names match your existing equipment table exactly.
# "Barbell" -> "Olympic Barbell", "Bodyweight" -> "Body Weight" (already in your table)

exercises_data = [
    {"name": "Bench Press", "category": "Compound", "types": ["Push", "Upper"], "muscles": ["Chest", "Shoulders", "Triceps"], "equipment": ["Olympic Barbell"]},
    {"name": "Incline Bench Press", "category": "Compound", "types": ["Push", "Upper"], "muscles": ["Chest", "Shoulders", "Triceps"], "equipment": ["Plate-Loaded Incline Chest Press"]},
    {"name": "Chest Press", "category": "Compound", "types": ["Push", "Upper"], "muscles": ["Chest", "Shoulders", "Triceps"], "equipment": ["Plate-Loaded Chest Press"]},
    {"name": "Pec Deck Fly", "category": "Isolation", "types": ["Push", "Upper"], "muscles": ["Chest"], "equipment": ["Pec Deck"]},
    {"name": "Push-up", "category": "Compound", "types": ["Push", "Upper"], "muscles": ["Chest", "Shoulders", "Triceps"], "equipment": ["Body Weight"]},
    {"name": "Shoulder Press", "category": "Compound", "types": ["Push", "Upper"], "muscles": ["Shoulders", "Triceps"], "equipment": ["Plate-Loaded Shoulder Press"]},
    {"name": "Dumbbell Shoulder Press", "category": "Compound", "types": ["Push", "Upper"], "muscles": ["Shoulders", "Triceps"], "equipment": ["Dumbbells"]},
    {"name": "Lateral Raise", "category": "Isolation", "types": ["Push", "Upper"], "muscles": ["Shoulders"], "equipment": ["Dumbbells"]},
    {"name": "Front Raise", "category": "Isolation", "types": ["Push", "Upper"], "muscles": ["Shoulders"], "equipment": ["Dumbbells"]},
    {"name": "Rear Delt Fly", "category": "Isolation", "types": ["Pull", "Upper"], "muscles": ["Shoulders", "Middle Back"], "equipment": ["Dumbbells"]},
    {"name": "Upright Row", "category": "Compound", "types": ["Pull", "Upper"], "muscles": ["Shoulders", "Traps"], "equipment": ["EZ Curl Bar"]},
    {"name": "Shrug", "category": "Isolation", "types": ["Pull", "Upper"], "muscles": ["Traps"], "equipment": ["Dumbbells"]},
    {"name": "Lat Pulldown", "category": "Compound", "types": ["Pull", "Upper"], "muscles": ["Lats", "Biceps"], "equipment": ["Lat Pulldown / Seated Cable Row Combo"]},
    {"name": "Plate-Loaded Lat Pulldown", "category": "Compound", "types": ["Pull", "Upper"], "muscles": ["Lats", "Biceps"], "equipment": ["Plate-Loaded Lat Pulldown"]},
    {"name": "Seated Cable Row", "category": "Compound", "types": ["Pull", "Upper"], "muscles": ["Middle Back", "Lats", "Biceps"], "equipment": ["Lat Pulldown / Seated Cable Row Combo"]},
    {"name": "Chest-Supported Row", "category": "Compound", "types": ["Pull", "Upper"], "muscles": ["Middle Back", "Lats", "Biceps"], "equipment": ["Plate-Loaded Chest-Supported Row"]},
    {"name": "Barbell Row", "category": "Compound", "types": ["Pull", "Upper"], "muscles": ["Middle Back", "Lats", "Biceps"], "equipment": ["Olympic Barbell"]},
    {"name": "Pull-up", "category": "Compound", "types": ["Pull", "Upper"], "muscles": ["Lats", "Biceps"], "equipment": ["Pull-Up Bar"]},
    {"name": "Assisted Pull-up", "category": "Compound", "types": ["Pull", "Upper"], "muscles": ["Lats", "Biceps"], "equipment": ["Assisted Pull-Up / Dip Machine"]},
    {"name": "Face Pull", "category": "Isolation", "types": ["Pull", "Upper"], "muscles": ["Shoulders", "Traps", "Middle Back"], "equipment": ["Functional Trainer"]},
    {"name": "Straight Arm Pulldown", "category": "Isolation", "types": ["Pull", "Upper"], "muscles": ["Lats"], "equipment": ["Functional Trainer"]},
    {"name": "Deadlift", "category": "Compound", "types": ["Legs", "Full Body"], "muscles": ["Hamstrings", "Glutes", "Lower Back", "Traps"], "equipment": ["Olympic Barbell"]},
    {"name": "Romanian Deadlift", "category": "Compound", "types": ["Legs", "Lower"], "muscles": ["Hamstrings", "Glutes", "Lower Back"], "equipment": ["Olympic Barbell"]},
    {"name": "Back Extension", "category": "Isolation", "types": ["Legs", "Lower"], "muscles": ["Lower Back", "Glutes", "Hamstrings"], "equipment": ["Back Extension"]},
    {"name": "Squat", "category": "Compound", "types": ["Legs", "Lower"], "muscles": ["Quadriceps", "Glutes", "Hamstrings"], "equipment": ["Olympic Barbell"]},
    {"name": "Smith Machine Squat", "category": "Compound", "types": ["Legs", "Lower"], "muscles": ["Quadriceps", "Glutes", "Hamstrings"], "equipment": ["Smith Machine"]},
    {"name": "Leg Press", "category": "Compound", "types": ["Legs", "Lower"], "muscles": ["Quadriceps", "Glutes", "Hamstrings"], "equipment": ["Leg Press"]},
    {"name": "Leg Extension", "category": "Isolation", "types": ["Legs", "Lower"], "muscles": ["Quadriceps"], "equipment": ["Leg Extension"]},
    {"name": "Lying Leg Curl", "category": "Isolation", "types": ["Legs", "Lower"], "muscles": ["Hamstrings"], "equipment": ["Lying Leg Curl"]},
    {"name": "Seated Leg Curl", "category": "Isolation", "types": ["Legs", "Lower"], "muscles": ["Hamstrings"], "equipment": ["Seated Leg Curl"]},
    {"name": "Hip Thrust", "category": "Compound", "types": ["Legs", "Lower"], "muscles": ["Glutes", "Hamstrings"], "equipment": ["Hip Thrust Machine"]},
    {"name": "Hip Abduction", "category": "Isolation", "types": ["Legs", "Lower"], "muscles": ["Abductors", "Glutes"], "equipment": ["Hip Abductor"]},
    {"name": "Hip Adduction", "category": "Isolation", "types": ["Legs", "Lower"], "muscles": ["Adductors"], "equipment": ["Hip Adductor"]},
    {"name": "Standing Calf Raise", "category": "Isolation", "types": ["Legs", "Lower"], "muscles": ["Calves"], "equipment": ["Body Weight"]},
    {"name": "Seated Calf Raise", "category": "Isolation", "types": ["Legs", "Lower"], "muscles": ["Calves"], "equipment": ["Leg Press"]},
    {"name": "Barbell Curl", "category": "Isolation", "types": ["Pull", "Upper"], "muscles": ["Biceps", "Forearms"], "equipment": ["Olympic Barbell"]},
    {"name": "EZ Bar Curl", "category": "Isolation", "types": ["Pull", "Upper"], "muscles": ["Biceps", "Forearms"], "equipment": ["EZ Curl Bar"]},
    {"name": "Preacher Curl", "category": "Isolation", "types": ["Pull", "Upper"], "muscles": ["Biceps"], "equipment": ["Preacher Curl Bench"]},
    {"name": "Hammer Curl", "category": "Isolation", "types": ["Pull", "Upper"], "muscles": ["Biceps", "Forearms"], "equipment": ["Dumbbells"]},
    {"name": "Concentration Curl", "category": "Isolation", "types": ["Pull", "Upper"], "muscles": ["Biceps"], "equipment": ["Dumbbells"]},
    {"name": "Cable Curl", "category": "Isolation", "types": ["Pull", "Upper"], "muscles": ["Biceps"], "equipment": ["Functional Trainer"]},
    {"name": "Triceps Pushdown", "category": "Isolation", "types": ["Push", "Upper"], "muscles": ["Triceps"], "equipment": ["Functional Trainer"]},
    {"name": "Overhead Triceps Extension", "category": "Isolation", "types": ["Push", "Upper"], "muscles": ["Triceps"], "equipment": ["Functional Trainer"]},
    {"name": "Skull Crusher", "category": "Isolation", "types": ["Push", "Upper"], "muscles": ["Triceps"], "equipment": ["EZ Curl Bar"]},
    {"name": "Bench Dip", "category": "Compound", "types": ["Push", "Upper"], "muscles": ["Triceps", "Chest"], "equipment": ["Flat Bench"]},
    {"name": "Assisted Dip", "category": "Compound", "types": ["Push", "Upper"], "muscles": ["Triceps", "Chest", "Shoulders"], "equipment": ["Assisted Pull-Up / Dip Machine"]},
    {"name": "Cable Crunch", "category": "Isolation", "types": ["Full Body"], "muscles": ["Abdominals"], "equipment": ["Functional Trainer"]},
    {"name": "Hanging Leg Raise", "category": "Isolation", "types": ["Full Body"], "muscles": ["Abdominals"], "equipment": ["Pull-Up Bar"]},
    {"name": "Plank", "category": "Isometric", "types": ["Full Body"], "muscles": ["Abdominals"], "equipment": ["Exercise Mat"]},
    {"name": "Russian Twist", "category": "Isolation", "types": ["Full Body"], "muscles": ["Abdominals"], "equipment": ["Exercise Mat"]},
    {"name": "Farmer's Carry", "category": "Compound", "types": ["Full Body"], "muscles": ["Forearms", "Traps"], "equipment": ["Dumbbells"]},
    {"name": "Treadmill Run", "category": "Cardio", "types": ["Full Body"], "muscles": ["Calves", "Quadriceps"], "equipment": ["Treadmill"]},
    {"name": "Jump Rope", "category": "Cardio", "types": ["Full Body"], "muscles": ["Calves"], "equipment": ["Jump Rope"]},
]

for ex in exercises_data:
    # Insert the exercise itself, linking to its category by name via subquery
    cur.execute("""
        INSERT INTO exercises (name, category_id)
        SELECT %s, id FROM categories WHERE name = %s
        ON CONFLICT (name) DO NOTHING;
    """, (ex["name"], ex["category"]))

    # Link to day-type(s)
    for t in ex["types"]:
        cur.execute("""
            INSERT INTO exercise_types (exercise_id, type_id)
            SELECT e.id, t.id FROM exercises e, types t
            WHERE e.name = %s AND t.name = %s;
        """, (ex["name"], t))

    # Link to muscle(s)
    for m in ex["muscles"]:
        cur.execute("""
            INSERT INTO exercise_muscles (exercise_id, muscle_id)
            SELECT e.id, mu.id FROM exercises e, muscles mu
            WHERE e.name = %s AND mu.name = %s;
        """, (ex["name"], m))

    # Link to equipment
    for eq in ex["equipment"]:
        cur.execute("""
            INSERT INTO exercise_equipment (exercise_id, equipment_id)
            SELECT e.id, eq.id FROM exercises e, equipment eq
            WHERE e.name = %s AND eq.name = %s;
        """, (ex["name"], eq))

conn.commit()
print(f"Inserted {len(exercises_data)} exercises with category, type, muscle, and equipment links.")

cur.close()
conn.close()