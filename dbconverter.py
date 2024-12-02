import sqlite3

sqlite_conn = sqlite3.connect('db.sqlite3')

# Open a file to write the SQL dump
with open('sqlite_dump.sql', 'w') as dump_file:
    for line in sqlite_conn.iterdump():
        dump_file.write('%s\n' % line)

# Close the connection
sqlite_conn.close()

print("SQLite dump file generated successfully!")
