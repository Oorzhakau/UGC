CREATE DATABASE bubbleformation;

CREATE TABLE IF NOT EXISTS movie_likes (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    movie_id uuid NOT NULL,
    rt_value int,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS movie_reviews (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    movie_id uuid NOT NULL,
    review text NOT NULL,
    rating int,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS movie_bookmarks (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    movie_id uuid NOT NULL,
    created timestamp with time zone
);
