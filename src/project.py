import mysql.connector
import sys
import load

# Open connection
conn = mysql.connector.connect(user='test', password='password', database='cs122a')
cur = conn.cursor()

# Arg processing
command, *args = sys.argv[1:]

match command:
    case 'import':
        load.exec(cur)
        print('import')
    case 'insertViewer':
        print('insertViewer')
    case 'addGenre':
        print('addGenre')
    case 'deleteViewer':
        print('deleteviewer')
    case 'insertMovie':
        print('insertMovie')
    case 'insertSession':
        print('insertSession')
    case 'updateRelease':
        print('updateRelease')
    case 'listReleases':
        print('listReleases')
    case 'popularRelease':
        print('popularRelease')
    case 'releaseTitle':
        print('releaseTitle')
    case 'activeViewers':
        print('activeViewers')
    case 'videosViewed':
        print('videosViewed')
    case _:
        print("Error, unrecognized command")

# Clean up connection
cur.close()
conn.close()