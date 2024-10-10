-- Table for storing user information
CREATE TABLE "User" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing nationality information
CREATE TABLE Nationality (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Table for storing competition information
CREATE TABLE Competition (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL
);

-- Table for storing team information
CREATE TABLE Team (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Table for storing player information
CREATE TABLE Player (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    nationality_id INTEGER REFERENCES Nationality(id),
    team_id INTEGER REFERENCES Team(id),
    market_value DECIMAL(15, 2) NOT NULL,
    position VARCHAR(50) NOT NULL,
    alternate_position VARCHAR(50)
);

-- Table for storing team and competition relationships
CREATE TABLE Team_Competition (
    team_id INTEGER REFERENCES Team(id),
    competition_id INTEGER REFERENCES Competition(id),
    PRIMARY KEY (team_id, competition_id)
);

-- Table for storing formation information
CREATE TABLE Formation (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

-- Table for storing squad information
CREATE TABLE Squad (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "User"(id),
    formation_id INTEGER REFERENCES Formation(id),
    competition_id INTEGER REFERENCES Competition(id),
    budget DECIMAL(15, 2) NOT NULL,
    nationality_id INTEGER REFERENCES Nationality(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for linking players to squads
CREATE TABLE Squad_Player (
    id SERIAL PRIMARY KEY,
    squad_id INTEGER REFERENCES Squad(id),
    player_id INTEGER REFERENCES Player(id),
    position_in_squad VARCHAR(50) NOT NULL
);

-- Table for storing ratings given to squads by users
CREATE TABLE Rating (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "User"(id),
    squad_id INTEGER REFERENCES Squad(id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create views
CREATE VIEW SquadDetails AS
SELECT
    s.id AS squad_id,
    u.username,
    f.name AS formation_name,
    n.name AS nationality_name,
    c.name AS competition_name,
    l.budget,
    s.created_at
FROM
    Squad s
    JOIN "User" u ON s.user_id = u.id
    JOIN Formation f ON s.formation_id = f.id
    JOIN Limitation l ON s.id = l.squad_id
    LEFT JOIN Competition c ON l.competition_id = c.id
    LEFT JOIN Nationality n ON l.nationality_id = n.id;

CREATE VIEW SquadPlayers AS
SELECT
    sp.squad_id,
    p.name AS player_name,
    p.position,
    p.alternate_position,
    sp.position_in_squad
FROM
    Squad_Player sp
    JOIN Player p ON sp.player_id = p.id;

CREATE VIEW SquadRatings AS
SELECT
    r.squad_id,
    u.username,
    r.rating,
    r.comment,
    r.created_at
FROM
    Rating r
    JOIN "User" u ON r.user_id = u.id;

CREATE VIEW Squad_Average_Rating AS
SELECT
    s.id AS squad_id,
    u.username,
    AVG(r.rating) AS average_rating
FROM
    Squad s
    JOIN Rating r ON s.id = r.squad_id
    JOIN "User" u ON s.user_id = u.id
GROUP BY
    s.id,
    u.username;

-- Create indexes
CREATE INDEX idx_player_name_position ON Player (name, position);
CREATE INDEX idx_rating_squad ON Rating (squad_id);
