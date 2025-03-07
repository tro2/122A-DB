USE cs122a;

SET FOREIGN_KEY_CHECKS=0;
SET UNIQUE_CHECKS=0;

DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    uid INT,
    email TEXT NOT NULL,
    joined_date DATE NOT NULL,
    nickname TEXT NOT NULL,
    street TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    genres TEXT,
    PRIMARY KEY (uid)
);

DROP TABLE IF EXISTS Producers;
CREATE TABLE Producers (
    uid INT,
    bio TEXT,
    company TEXT,
    PRIMARY KEY (uid),
    FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Viewers;
CREATE TABLE Viewers (
    uid INT,
    subscription ENUM('free', 'monthly', 'yearly'),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    PRIMARY KEY (uid),
    FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Releases;
CREATE TABLE Releases (
    rid INT,
    producer_uid INT NOT NULL,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    release_date DATE NOT NULL,
    PRIMARY KEY (rid),
    FOREIGN KEY (producer_uid) REFERENCES Producers(uid) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Movies;
CREATE TABLE Movies (
    rid INT,
    website_url TEXT,
    PRIMARY KEY (rid),
    FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Series;
CREATE TABLE Series (
    rid INT,
    introduction TEXT,
    PRIMARY KEY (rid),
    FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Videos;
CREATE TABLE Videos (
    rid INT,
    ep_num INT NOT NULL,
    title TEXT NOT NULL,
    length INT NOT NULL,
    PRIMARY KEY (rid, ep_num),
    FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Sessions;
CREATE TABLE Sessions (
    sid INT,
    uid INT NOT NULL,
    rid INT NOT NULL,
    ep_num INT NOT NULL,
    initiate_at DATETIME NOT NULL,
    leave_at DATETIME NOT NULL,
    quality ENUM('480p', '720p', '1080p'),
    device ENUM('mobile', 'desktop'),
    PRIMARY KEY (sid),
    FOREIGN KEY (uid) REFERENCES Viewers(uid) ON DELETE CASCADE,
    FOREIGN KEY (rid, ep_num) REFERENCES Videos(rid, ep_num) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Reviews;
CREATE TABLE Reviews (
    rvid INT,
    uid INT NOT NULL,
    rid INT NOT NULL,
    rating DECIMAL(2, 1) NOT NULL CHECK (rating BETWEEN 0 AND 5),
    body TEXT,
    posted_at DATETIME NOT NULL,
    PRIMARY KEY (rvid),
    FOREIGN KEY (uid) REFERENCES Viewers(uid) ON DELETE CASCADE,
    FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
);

SET FOREIGN_KEY_CHECKS=1;
SET UNIQUE_CHECKS=1;