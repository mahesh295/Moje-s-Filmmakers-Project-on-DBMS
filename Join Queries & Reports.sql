-- 1. All Movies with Director Names
SELECT m.title AS Movie_Title, d.name AS Director_Name, m.release_year
FROM MovieDetails m
JOIN DirectorInfo d ON m.director_id = d.director_id
ORDER BY d.name;

-- 2. Movies by S. S. Rajamouli
SELECT m.title, m.release_year
FROM MovieDetails m
JOIN DirectorInfo d ON m.director_id = d.director_id
WHERE d.name = 'S. S. Rajamouli';

-- 3. Full Movie Info (Title, Hero, Heroine, Director, Collection)
SELECT 
    m.title AS Movie,
    c.hero AS Hero,
    c.heroine AS Heroine,
    d.name AS Director,
    mc.box_office AS Box_Office_INR_Cr
FROM MovieDetails m
JOIN CastInfo c ON m.movie_id = c.movie_id
JOIN DirectorInfo d ON m.director_id = d.director_id
JOIN MovieCollections mc ON m.movie_id = mc.movie_id
ORDER BY mc.box_office DESC;

-- 4. Top 5 Highest Grossing Movies
SELECT m.title, d.name AS Director, mc.box_office
FROM MovieDetails m
JOIN DirectorInfo d ON m.director_id = d.director_id
JOIN MovieCollections mc ON m.movie_id = mc.movie_id
ORDER BY mc.box_office DESC
LIMIT 5;

-- 5. Movies Count by Each Director
SELECT d.name AS Director, COUNT(m.movie_id) AS Movie_Count
FROM DirectorInfo d
JOIN MovieDetails m ON d.director_id = m.director_id
GROUP BY d.name
ORDER BY Movie_Count DESC;

-- 6. Directors with >2 Movies
SELECT d.name AS Director, COUNT(m.movie_id) AS Total_Movies
FROM DirectorInfo d
JOIN MovieDetails m ON d.director_id = m.director_id
GROUP BY d.name
HAVING COUNT(m.movie_id) > 2;

-- 7. All Movies of Mahesh Babu
SELECT m.title, m.release_year, d.name AS Director
FROM MovieDetails m
JOIN CastInfo c ON m.movie_id = c.movie_id
JOIN DirectorInfo d ON m.director_id = d.director_id
WHERE c.hero = 'Mahesh Babu';

-- 8. Total Box Office by Director
SELECT d.name AS Director, SUM(mc.box_office) AS Total_Box_Office
FROM DirectorInfo d
JOIN MovieDetails m ON d.director_id = m.director_id
JOIN MovieCollections mc ON m.movie_id = mc.movie_id
GROUP BY d.name
ORDER BY Total_Box_Office DESC;

-- 9. Movies Released After 2015 with Collections > ₹200 Cr
SELECT m.title, m.release_year, mc.box_office
FROM MovieDetails m
JOIN MovieCollections mc ON m.movie_id = mc.movie_id
WHERE m.release_year > 2015 AND mc.box_office > 200;

-- 10. Multi-Movie Directors (Group Query)
SELECT d.name AS Director, m.title AS Movie, m.release_year
FROM MovieDetails m
JOIN DirectorInfo d ON m.director_id = d.director_id
WHERE d.director_id IN (
    SELECT director_id
    FROM MovieDetails
    GROUP BY director_id
    HAVING COUNT(*) > 1
)
ORDER BY d.name, m.release_year;

-- 11. LEFT JOIN Example
SELECT mc.movie_id, m.title, mc.box_office
FROM MovieCollections mc
LEFT JOIN MovieDetails m ON m.movie_id = mc.movie_id;
