-- SQLite
WITH totals AS (
    SELECT
        team,
        CAST(SUM(h) AS REAL) as h,
        CAST(SUM(bb) AS REAL) as bb,
        CAST(SUM(so) AS REAL) as so,
        CAST(SUM(hbp) AS REAL) as hbp,
        CAST(SUM(ab) AS REAL) as ab,
        CAST(SUM(pa) AS REAL) as pa,
        CAST(SUM(sf) AS REAL) as sf,
        CAST(SUM('1b') AS REAL) as _1b,
        CAST(SUM('2b') AS REAL) as _2b,
        CAST(SUM('3b') AS REAL) as _3b,
        CAST(SUM(hr) AS REAL) as hr
    FROM
        bronze_std_batting
    GROUP BY
        team
),
LEVEL1 AS (
    SELECT
        team,
        h / ab as avg,
        (h + bb + hbp) / (ab + bb + hbp + sf) as obp,
        (_1b + 2 * _2b + 3 * _3b + 4 * hr) / ab as slg,
        bb / pa as bb_rate,
        so / pa as k_rate,
        bb / so as bb_per_k,
        (h - hr) / (ab - so - hr + sf) as babip
    FROM
        totals
    GROUP BY
        team
),
LEVEL2 AS (
    SELECT 
        *,
        obp + slg as ops
    FROM
        LEVEL1
),
RANKS AS (
    SELECT
        team AS Team,
        RANK() OVER (ORDER BY avg desc) AS Avg,
        RANK() OVER (ORDER BY obp desc) AS OBP,
        RANK() OVER (ORDER BY slg desc) AS SLG,
        RANK() OVER (ORDER BY bb_rate desc) AS 'BB%',
        RANK() OVER (ORDER BY k_rate asc) AS 'K%',
        RANK() OVER (ORDER BY bb_per_k desc) AS 'BB/K',
        RANK() OVER (ORDER BY babip desc) AS BABIP,
        RANK() OVER (ORDER BY ops desc) AS OPS
    FROM
        LEVEL2
)
SELECT
    R.team,
    R.AVG,
    L.avg,
    R.SLG,
    L.slg,
    R.OBP,
    L.obp
FROM
    RANKS as R
LEFT JOIN
    LEVEL2 as L ON (L.team = R.team)
WHERE
    R.team IN ("CLEM", "CLEM_2026");


-- SELECT * FROM bronze_std_batting WHERE team = 'CLEM_2026';

-- SELECT COUNT(DISTINCT team) FROM bronze_std_batting;

-- INSERT INTO bronze_std_batting (name, team, age, g, ab, pa, h, '1b', '2b', '3b', hr, r, rbi, bb, so, hbp, sf, sh, gdp, sb, cs, avg, alt_name, id)
-- SELECT
--     name,
-- 	'CLEM_2026',
-- 	age,
-- 	g,
-- 	ab,
-- 	pa,
-- 	h,
-- 	'1b',
-- 	'2b',
-- 	'3b',
-- 	hr,
-- 	r,
-- 	rbi,
-- 	bb,
-- 	so,
-- 	hbp,
-- 	sf,
-- 	sh,
-- 	gdp,
-- 	sb,
-- 	cs,
-- 	avg,
-- 	alt_name,
-- 	id
-- FROM
--     bronze_std_batting
-- WHERE
--     name IN (
--         'Jacob Jarrell',
--         'Luke Gaffney',
--         'Jarren Purify',
--         'Josh Castellani',
--         'Tryston McCladdie',
--         'Jack Crighton',
--         'Tyler Lichtenberger',
--         'Ty Dalley',
--         'Ryan Wideman',
--         'Nate Savoie',
--         'Collin Priest'
--     )