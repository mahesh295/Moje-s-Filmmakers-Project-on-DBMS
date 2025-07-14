-- Create and use the database
CREATE DATABASE mojies;
USE mojies;

-- Table 1: DirectorInfo
CREATE TABLE DirectorInfo (
    director_id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    awards INT,
    total_movies INT
);

-- Table 2: MovieDetails
CREATE TABLE MovieDetails (
    movie_id INT PRIMARY KEY,
    title VARCHAR(100),
    director_id INT,
    release_year YEAR,
    FOREIGN KEY (director_id) REFERENCES DirectorInfo(director_id)
);

-- Table 3: CastInfo
CREATE TABLE CastInfo (
    cast_id INT PRIMARY KEY,
    movie_id INT,
    hero VARCHAR(100),
    heroine VARCHAR(100),
    FOREIGN KEY (movie_id) REFERENCES MovieDetails(movie_id)
);

-- Table 4: MovieCollections
CREATE TABLE MovieCollections (
    collection_id INT PRIMARY KEY,
    movie_id INT,
    box_office BIGINT,
    FOREIGN KEY (movie_id) REFERENCES MovieDetails(movie_id)
);
