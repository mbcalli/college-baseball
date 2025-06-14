CREATE TABLE IF NOT EXISTS silver_adv_batting (
    id TEXT PRIMARY KEY,
    name TEXT,
    team TEXT,
    pa_percentile INT,
    bb_rate_percentile INT,
    k_rate_percentile INT,
    bb_per_k_percentile INT,
    avg_percentile INT,
    obp_percentile INT,
    slg_percentile INT,
    ops_percentile INT,
    iso_percentile INT,
    spd_percentile INT,
    babip_percentile INT,
    wsb_percentile INT,
    wrc_percentile INT,
    wraa_percentile INT,
    woba_percentile INT,
    wrc_plus_percentile INT
)