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
    h1 VARCHAR(255), 
    title VARCHAR(255), 
    description VARCHAR(255), 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(url_id) REFERENCES urls (id)
);

COMMIT;

