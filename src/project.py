import mysql.connector
import sys
import os
import csv

# 1) import data
import mysql.connector
 import sys
 import os
 
 # 1) import data
 def import_data(conn, cursor):
     names = ["users", "producers", "viewers", "releases", "movies", "series", "videos", "sessions", "reviews"]
     folder_name = sys.argv[2]
 
     try:
         # drop tables in reverse to avoid foreign key issues
         for table in names[::-1]:
             cursor.execute(f"DROP TABLE IF EXISTS {table}")
 
         cursor.execute("CREATE TABLE users (uid INT, email TEXT NOT NULL, joined_date DATE NOT NULL, nickname TEXT NOT NULL, street TEXT, city TEXT, state TEXT, zip TEXT, genres TEXT, PRIMARY KEY(uid));")
         cursor.execute("CREATE TABLE producers (uid INT, bio TEXT, company TEXT, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE);")
         cursor.execute("CREATE TABLE viewers (uid INT, subscription ENUM('free', 'monthly', 'yearly'), first_name TEXT NOT NULL, last_name TEXT NOT NULL, PRIMARY KEY (uid), FOREIGN KEY(uid) REFERENCES users(uid) ON DELETE CASCADE);")
         cursor.execute("CREATE TABLE releases (rid INT, producer_uid INT NOT NULL, title TEXT NOT NULL, genre TEXT NOT NULL, release_date DATE NOT NULL, PRIMARY KEY (rid), FOREIGN KEY (producer_uid) REFERENCES producers (uid) ON DELETE CASCADE);")
         cursor.execute("CREATE TABLE movies(rid INT, website_url TEXT, PRIMARY KEY (rid), FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE);")
         cursor.execute("CREATE TABLE series(rid INT, introduction TEXT, PRIMARY KEY (rid), FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE);")
         cursor.execute("CREATE TABLE videos(rid INT, ep_num INT NOT NULL, title TEXT NOT NULL, length INT NOT NULL, PRIMARY KEY (rid, ep_num), FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE);")
         cursor.execute("CREATE TABLE sessions(sid INT, uid INT NOT NULL, rid INT NOT NULL, ep_num INT NOT NULL, initiate_at DATETIME NOT NULL, leave_at DATETIME NOT NULL, quality ENUM('480p', '720p', '1080p'), device ENUM('mobile', 'desktop'), PRIMARY KEY (sid), FOREIGN KEY (uid) REFERENCES viewers(uid) ON DELETE CASCADE, FOREIGN KEY (rid, ep_num) REFERENCES videos(rid, ep_num) ON DELETE CASCADE);")
         cursor.execute("CREATE TABLE reviews(rvid INT, uid INT NOT NULL, rid INT NOT NULL, rating DECIMAL(2, 1) NOT NULL CHECK (rating BETWEEN 0 AND 5), body TEXT, posted_at DATETIME NOT NULL, PRIMARY KEY (rvid), FOREIGN KEY (uid) REFERENCES viewers(uid) ON DELETE CASCADE, FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE);")
 
         for table in names:
             file_path = f"{folder_name}/{table}.csv"
             cursor.execute(f"LOAD DATA LOCAL INFILE '{file_path}' into table {table} FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\n' IGNORE 1 ROWS;")
 
         conn.commit()
         return True
 
     except: return False

# 2) insert viewer
def insertViewer(conn, cursor):
    uid = sys.argv[2]
    email = sys.argv[3]
    nickname = sys.argv[4]
    street = sys.argv[5]
    city = sys.argv[6]
    state = sys.argv[7]
    zipc = sys.argv[8]
    genres = sys.argv[9]
    joined = sys.argv[10]
    first = sys.argv[11]
    last = sys.argv[12]
    sub = sys.argv[13]
    
    try:
        cursor.execute(f"INSERT INTO users (uid,email,joined_date,nickname,street,city,state,zip,genres) VALUES ({uid}, '{email}', '{joined}', '{nickname}', '{street}', '{city}', '{state}', {zipc}, '{genres}');")
        cursor.execute(f"INSERT INTO viewers (uid,subscription,first_name,last_name) VALUES ({uid}, '{sub}', '{first}', '{last}');")

        conn.commit()
        return True

    except: return False

# 3) insert genre
def insertGenre(conn, cursor):
    uid = sys.argv[2]
    genre = sys.argv[3]

    # get existing genres and add genre if not already there
    try:
        cursor.execute(f"SELECT genres FROM users WHERE uid = {uid}")
        prev = cursor.fetchone()[0]
        if genre not in prev: prev += f";{genre}"

        cursor.execute(f"UPDATE users SET genres = '{prev}' WHERE uid = {uid}")
        
        conn.commit()
        return True

    except: return False

# 4) delete viewer
def deleteViewer(conn, cursor):
    uid = sys.argv[2]

    # deleting from viewers will cascade
    try:
        cursor.execute(f"DELETE FROM viewers WHERE uid = {uid}")
        conn.commit()
        return True
    
    except: return False

# 5) insert movie
def insertMovie(conn, cursor):
    rid = sys.argv[2]
    web = sys.argv[3]

    # assumes release already exists
    try:
        cursor.execute(f"INSERT INTO movies (rid,website_url) VALUES ({rid}, '{web}')")
        conn.commit()
        return True
    
    except: return False

# 6) insert session
def insertSession(conn, cursor):
    sid = sys.argv[2]
    uid = sys.argv[3]
    rid = sys.argv[4]
    ep_num = sys.argv[5]
    init = sys.argv[6]
    leave = sys.argv[7]
    quality = sys.argv[8]
    device = sys.argv[9]

    try:
        cursor.execute(f"INSERT INTO sessions (sid,uid,rid,ep_num,initiate_at,leave_at,quality,device) VALUES ({sid}, {uid}, {rid}, {ep_num}, '{init}', '{leave}', '{quality}', '{device}')")
        conn.commit()
        return True
    
    except: return False

# 7) update release
def updateRelease(conn, cursor):
    rid = sys.argv[2]
    title = sys.argv[3]

    try:
        cursor.execute(f"UPDATE releases SET title = '{title}' WHERE rid = {rid}")
        conn.commit()
        return True

    except: return False

# 8) list releases
def listReleases(conn, cursor):
    uid = sys.argv[2]

    try:
        cursor.execute(f"SELECT DISTINCT rl.rid, rl.genre, rl.title FROM Reviews rv JOIN Releases rl ON rv.rid = rl.rid WHERE rv.uid = {uid} ORDER BY rl.title ASC")
        return (cursor.column_names, cursor.fetchall())

    except: return False

# 9) popular release
def popularRelease(conn, cursor):
    num = sys.argv[2]
    
    try:
        cursor.execute(f"SELECT rl.rid, rl.title, COUNT(*) as reviewCount FROM reviews rv JOIN releases rl ON rv.rid = rl.rid GROUP BY rl.rid ORDER BY reviewCount DESC LIMIT {num}")
        return (cursor.column_names, cursor.fetchall())
    
    except: return False

# 10) title of release
def releaseTitle(conn, cursor):
    sid = sys.argv[2]
    
    try:
        cursor.execute(f"SELECT r.rid, r.title, r.genre, v.title, v.ep_num, v.length FROM (sessions s JOIN videos v ON s.rid = v.rid AND s.ep_num = v.ep_num) JOIN releases r ON r.rid = v.rid WHERE s.sid = {sid} ORDER BY r.title ASC")
        return (cursor.column_names, cursor.fetchall())

    except: return False

# 11) active viewers
def activeViewer(conn, cursor):
    # parse arg
    num = sys.argv[2]
    start = sys.argv[3]
    end = sys.argv[4]
    
    try:
        cursor.execute(f"SELECT v.uid, v.first_name, v.last_name FROM viewers v JOIN (SELECT uid, COUNT(*) as numSessions FROM sessions WHERE STR_TO_DATE('{start}', '%Y-%m-%d %H:%i%s') < initiate_at AND initiate_at < STR_TO_DATE('{end}', '%Y-%m-%d %H:%i%s') GROUP BY uid) AS n ON v.uid = n.uid WHERE n.numSessions >= {num}")
        return (cursor.column_names, cursor.fetchall())

    except: return False

# 12) videos viewed
# WIP, currently errors out and unsure why
def videosViewed(conn, cursor):
    rid = sys.argv[2]

    # Given a Video rid, count the number of unique viewers that have started a session on it. Videos that are not streamed by any viewer should have a count of 0 instead of NULL. Return video information along with the count in DESCENDING order by rid.
    try:
        cursor.execute(f"SELECT v.rid, v.ep_num, v.title, v.length, COUNT(DISTINCT s.uid) as numViewers FROM videos v LEFT JOIN sessions s ON v.rid = s.rid AND v.ep_num = s.ep_num WHERE v.rid = {rid} GROUP BY v.rid, v.ep_num, v.title, v.length ORDER BY v.rid DESC")
        return (cursor.column_names, cursor.fetchall())
    
    except: return False

# main handler
def main():
    conn = mysql.connector.connect(user="test", password="password", database="cs122a", allow_local_infile=True)
    cursor = conn.cursor()
    
    match sys.argv[1]:
        case "import": ret = import_data(conn, cursor)
        case "insertViewer": ret = insertViewer(conn, cursor)
        case "addGenre": ret = insertGenre(conn, cursor)
        case "deleteViewer": ret = deleteViewer(conn, cursor)
        case "insertMovie": ret = insertMovie(conn, cursor)
        case "insertSession": ret = insertSession(conn, cursor)
        case "updateRelease": ret = updateRelease(conn, cursor)
        case "listReleases": ret = listReleases(conn, cursor)
        case "popularRelease": ret = popularRelease(conn, cursor)
        case "releaseTitle": ret = releaseTitle(conn, cursor)
        case "activeViewer": ret = activeViewer(conn, cursor)
        case "videosViewed": ret = videosViewed(conn, cursor)
        case _: print("Unknown Command"); ret = False

    if isinstance(ret, bool):
        if ret: print("Success")
        else: print("Fail")
    else:
        names, rows = ret
        rows.insert(0, names)
        for row in rows: print(", ".join(map(str, row)))

    cursor.close()
    conn.close()

# calls main function when script is run
if __name__ == "__main__":
    main()
