🛢️ MySQL Commands Reference

Use the following SQL commands to view, manage, or reset your mojies database.

📂 View All Databases

SHOW DATABASES;

📌 Select the Database

USE mojies;

📋 Show All Tables

SHOW TABLES;

📊 Run All Queries (Reports & Joins)

💡 Run all your SELECT queries here to explore relationships, joins, and reports between directors, movies, cast, and collections.

-- Example: Show all movies with their director names
SELECT m.title, d.name AS Director
FROM MovieDetails m
JOIN DirectorInfo d ON m.director_id = d.director_id;

Add your JOIN, FILTER, AGGREGATE, and REPORT queries in this section of your .sql or while working in MySQL Workbench / CLI.

⚠️ Optional: Drop the Database

If you want to start fresh or reset the schema:

DROP DATABASE mojies;

✅ Tip: Save all queries in a database_queries.sql file for easy version control and repeat testing.
