#! /bin/bash

sqlite3 /home/dipesh/Desktop/CS315A/assignment_CS315/sqliteDB$1 << EOF
.timer ON
.output output$1.txt
.read /home/dipesh/Desktop/CS315A/assignment_CS315/queries.sql
EOF