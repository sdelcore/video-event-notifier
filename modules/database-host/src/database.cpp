#include <database.h>

Database::Database(YAML::Node *config) {
    char *zErrMsg = 0;
    int rc;
    this->config = config;
    string db = (*this->config)["Host"]["database"].as<string>();
    rc = sqlite3_open(db.c_str(), &this->database);

    if( rc ) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(this->database));
    } else {
        //fprintf(stderr, "Opened database successfully\n");
    }

    this->addMovieTable();
}

Database::~Database() {
    sqlite3_close(this->database);
}

int Database::addMovieTable() {
    /* Create SQL statement */
    int rc;
    char *zErrMsg = 0;  
    string sql;
    sql = "CREATE TABLE IF NOT EXISTS Movies ("  \
        "ID INTEGER PRIMARY KEY     NOT NULL," \
        "MOVIE          TEXT    NOT NULL," \
        "TIME           INT     NOT NULL," \
        "EVENTS         INT     NOT NULL," \
        "UNIQUE(MOVIE, TIME, EVENTS) );";

    /* Execute SQL statement */
    rc = sqlite3_exec(this->database, sql.c_str(), NULL, 0, &zErrMsg);

    if( rc != SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        //fprintf(stdout, "Table created successfully\n");
    }

    return 0;
}

int Database::insertTime(const char* movie, int time, int events) {
   char *zErrMsg = 0;
   int rc;
   string sql;


   /* Create SQL statement */
   sql = "INSERT INTO Movies (MOVIE,TIME,EVENTS) VALUES (\"";
   sql += movie;
   sql += "\",";
   sql += to_string(time);
   sql += ",";
   sql += to_string(events);
   sql += ");";

   /* Execute SQL statement */
   rc = sqlite3_exec(this->database, sql.c_str(), NULL, 0, &zErrMsg);
   
   if( rc != SQLITE_OK ){
      fprintf(stderr, "SQL error: %s\n", zErrMsg);
      sqlite3_free(zErrMsg);
   } else {
      //fprintf(stdout, "Records created successfully\n");
   }
   
   return 0;
}

int Database::getEvents(const char* movie, int time) {
    char *zErrMsg = 0;
    int rc;
    string sql;
    const char* data = "Callback function called";

    /* Create SQL statement */
    sql = "SELECT EVENTS from Movies WHERE MOVIE=\"";
    sql += movie;
    sql += "\" AND TIME=";
    sql += to_string(time);
    sql += ";";

    int events = 0;

    vector<vector<string> > result = this->query(sql.c_str());
    for(vector<vector<string> >::iterator it = result.begin(); it < result.end(); ++it)
    {
        vector<string> row = *it;
        events = stoi(row.at(0));
    }

    return events;
}

vector<vector<string>> Database::query(const char* query)
{
	sqlite3_stmt *statement;
	vector<vector<string> > results;

	if(sqlite3_prepare_v2(database, query, -1, &statement, 0) == SQLITE_OK)
	{
		int cols = sqlite3_column_count(statement);
		int result = 0;
		while(true)
		{
			result = sqlite3_step(statement);
			
			if(result == SQLITE_ROW)
			{
				vector<string> values;
				for(int col = 0; col < cols; col++)
				{
					values.push_back((char*)sqlite3_column_text(statement, col));
				}
				results.push_back(values);
			}
			else
			{
				break;   
			}
		}
	   
		sqlite3_finalize(statement);
	}
	
	string error = sqlite3_errmsg(database);
	if(error != "not an error") cout << query << " " << error << endl;
	
	return results;  
}