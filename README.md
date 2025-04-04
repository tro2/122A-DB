# 122A-DB
Final Project for CS 122A
## Setup Instructions
To create the environment that roughly matches the Gradescope testing environment, install these:
1. [MySQL Server Community Edition](https://dev.mysql.com/downloads/mysql/)
2. [mysql-connector python package](https://pypi.org/project/mysql-connector-python/)

*Note: If you  would like to use an environment other than MYSQL Server, that's probably fine, just make sure you set up the database name and 'test' account credentials properly*

Once installed and MySQL Server is running, execute `mysql -u root -p` in a terminal.

Then run the following commands:
```sql
CREATE DATABASE cs122a;
CREATE USER 'test'@'localhost'
  IDENTIFIED BY 'password';
GRANT ALL
  ON cs122a.*
  TO 'test'@'localhost';
USE cs122a;
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
CREATE TABLE Producers (
    uid INT,
    bio TEXT,
    company TEXT,
    PRIMARY KEY (uid),
    FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE
);
CREATE TABLE Viewers (
    uid INT,
    subscription ENUM('free', 'monthly', 'yearly'),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    PRIMARY KEY (uid),
    FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE
);
CREATE TABLE Releases (
    rid INT,
    producer_uid INT NOT NULL,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    release_date DATE NOT NULL,
    PRIMARY KEY (rid),
    FOREIGN KEY (producer_uid) REFERENCES Producers(uid) ON DELETE CASCADE
);
CREATE TABLE Movies (
    rid INT,
    website_url TEXT,
    PRIMARY KEY (rid),
    FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
);
CREATE TABLE Series (
    rid INT,
    introduction TEXT,
    PRIMARY KEY (rid),
    FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
);
CREATE TABLE Videos (
    rid INT,
    ep_num INT NOT NULL,
    title TEXT NOT NULL,
    length INT NOT NULL,
    PRIMARY KEY (rid, ep_num),
    FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
);
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
```

This will ensure a user account and database will be created that have the same login credentials as the Gradescope environment.

From here, you can run `project.py` to ensure things are working.

More tutorials on using MySQL Server can be found [here](https://dev.mysql.com/doc/mysql-getting-started/en/#mysql-getting-started-installing).

## Reinitializing the database
If you would like to get back to a fresh, clean database, there is a backup called `schemas.sql` that can be used to overwrite the database.

On Windows Powershell, you can load it with
```shell
Get-Content src/schemas.sql | mysql -u root -p cs122a
```