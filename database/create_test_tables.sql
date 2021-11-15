CREATE SEQUENCE actor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE movie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE IF NOT EXISTS "Gender" (
    id INT PRIMARY KEY,
    name VARCHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS "Actor" (
    id INT PRIMARY KEY DEFAULT nextval('actor_id_seq'),
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender_id INT,
    CONSTRAINT gender_id
        FOREIGN KEY(gender_id)
            REFERENCES "Gender"(id)
);

CREATE TABLE IF NOT EXISTS "Movie" (
    id INT PRIMARY KEY DEFAULT nextval('movie_id_seq'),
    title VARCHAR(100) NOT NULL,
    release_date TIMESTAMP NOT NULL
);


CREATE TABLE IF NOT EXISTS actors_movies (
    actor_id INT,
    movie_id INT,
    FOREIGN KEY(actor_id)
        REFERENCES "Actor"(id)
            ON DELETE CASCADE,
    FOREIGN KEY(movie_id)
        REFERENCES "Movie"(id)
            ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS gender_actors (
    gender_id INT,
    actor_id INT,
    FOREIGN KEY(actor_id)
        REFERENCES "Actor"(id)
            ON DELETE CASCADE,
    FOREIGN KEY(gender_id)
        REFERENCES "Gender"(id)
            ON DELETE CASCADE
);
