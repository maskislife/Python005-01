
--seventh
SELECT DISTINCT player_id, player_name, count(*) as num 

-- first
FROM player JOIN team ON player.team_id = team.team_id 

-- second
WHERE height > 1.80 

-- third
GROUP BY player.team_id 

-- forth
HAVING num > 2 

-- fifth
ORDER BY num DESC 

-- sixth
LIMIT 2
