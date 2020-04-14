#ifndef DATABASE_H
#define DATABASE_H

#include <iostream> // header in standard library
#include <stdio.h>
#include <sqlite3.h> 
#include <vector>
#include "yaml-cpp/yaml.h"


using namespace std;

class Database
{
    public:
        Database(YAML::Node *config);
        ~Database();
        int addMovieTable();
        int insertTime(const char* movie, int time, int events);
        int getEvents(const char* movie, int time);
        vector<vector<string>> query(const char* query);

    private:
        sqlite3* database;
        YAML::Node *config;
};

#endif //DATABASE_H

//https://www.tutorialspoint.com/sqlite/sqlite_c_cpp.htm
// https://www.dreamincode.net/forums/topic/122300-sqlite-in-c/