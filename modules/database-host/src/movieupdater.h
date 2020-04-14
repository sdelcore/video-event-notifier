#ifndef MOVIE_UPDATER_H
#define MOVIE_UPDATER_H

#include <mosquittopp.h>
#include <iostream>
#include <string.h>
#include <json.hpp>
#include <database.h>
#include "yaml-cpp/yaml.h"

using json = nlohmann::json;
using namespace std;

class MovieUpdater : public mosqpp::mosquittopp
{
    private:
        int keepalive;
        Database *db;
        YAML::Node *config;

        void on_connect(int rc);
        void on_message(const struct mosquitto_message *message);
        void on_subscribe(int mid, int qos_count, const int *granted_qos);
    public:
        MovieUpdater(YAML::Node *config, Database *db);
        ~MovieUpdater();
};

#endif