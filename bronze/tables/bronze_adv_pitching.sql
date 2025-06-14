CREATE TABLE IF NOT EXISTS bronze_adv_pitching (
    name TEXT,
    team TEXT,
    age INT,
    ip REAL,
    k_per_nine REAL,
    bb_per_nine REAL,
    k_per_bb REAL,
    hr_per_nine REAL,
    k_rate REAL,
    bb_rate REAL,
    k_minus_bb_rate REAL,
    avg REAL,
    whip REAL,
    babip REAL,
    lob_rate REAL,
    era REAL,
    fip REAL,
    e_minus_f REAL,
    alt_name TEXT,
    id TEXT PRIMARY KEY
)