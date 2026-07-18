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

# : Insert workout types
cur.execute("""
    INSERT INTO types (name) VALUES
    ('Push'), ('Pull'), ('Legs'), ('Upper'), ('Lower'), ('Full Body')
    ON CONFLICT (name) DO NOTHING;
""")

# Insert muscles
cur.execute("""
    INSERT INTO muscles (name) VALUES
    ('Abdominals'), ('Abductors'), ('Adductors'), 
    ('Biceps'), ('Calves'), ('Chest'), ('Forearms'),
    ('Glutes'), ('Hamstrings'), ('Lats'), ('Lower Back'), ('Middle Back'),
    ('Neck'), ('Quadriceps'), ('Shoulders'), 
    ('Traps'), ('Triceps') ON CONFLICT (name) DO NOTHING;
""")


cur.execute("""
    INSERT INTO equipment (name) VALUES
    ('Power Rack'), ('Smith Machine'), ('Lying Leg Curl'), ('Seated Leg Curl'),
    ('Leg Extension'), ('Leg Press'), ('Hip Abductor'), ('Hip Adductor'),
    ('Hip Thrust Machine'), ('Back Extension'), ('Plate-Loaded Chest Press'),
    ('Plate-Loaded Incline Chest Press'), ('Pec Deck'), ('Plate-Loaded Shoulder Press'),
    ('Lat Pulldown / Seated Cable Row Combo'), ('Plate-Loaded Lat Pulldown'),
    ('Plate-Loaded Chest-Supported Row'), ('Assisted Pull-Up / Dip Machine'),
    ('Functional Trainer'), ('Single Cable Station'), ('Pull-Up Bar'),
    ('Flat Bench'), ('Adjustable Bench'), ('Preacher Curl Bench'),
    ('Olympic Barbell'), ('EZ Curl Bar'), ('Dumbbells'), ('Kettlebells'),
    ('Weight Plates'), ('Rope Attachment'), ('Straight Bar Attachment'),
    ('V-Bar Attachment'), ('D-Handle'), ('Ankle Strap'), ('Treadmill'),
    ('Jump Rope'), ('Resistance Bands'), ('Exercise Mat'), ('Body Weight')
    ON CONFLICT (name) DO NOTHING;
""")

cur.execute("""
    INSERT INTO categories (name, rest_seconds) VALUES
    ('Compound', 180),
    ('Isolation', 150),
    ('Cardio', 60),
    ('Isometric', 120)
    ON CONFLICT (name) DO NOTHING;
""")


conn.commit()
print("Categories inserted.")

conn.commit()
print("Equipment inserted.")

conn.commit()
print("Muscles inserted.")

conn.commit()
print("Types inserted.")

cur.close()
conn.close()