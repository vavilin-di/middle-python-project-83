BEGIN;

CREATE TABLE urls (
    id SERIAL NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE TABLE url_checks (
    id SERIAL NOT NULL, 
    url_id INTEGER NOT NULL, 
    status_code INTEGER, 
    h1 TEXT(), 
    title TEXT(), 
    description TEXT(), 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(url_id) REFERENCES urls (id)
);

COMMIT;

