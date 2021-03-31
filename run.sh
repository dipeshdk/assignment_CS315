#! /bin/bash

sqlite3 sqliteDB$1 << EOF
.timer ON
.output sql_query_result$1.txt
.read queries.sql
EOF