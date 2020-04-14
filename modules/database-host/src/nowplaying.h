#ifndef NOW_PLAYING_H
#define NOW_PLAYING_H

#include <mosquittopp.h>
#include <iostream>
#include <thread>
#include <chrono>
#include <atomic>
#include <string.h>
#include <json.hpp>
#include <database.h>
#include "yaml-cpp/yaml.h"

using json = nlohmann::json;
using namespace std;

class NowPlaying : public mosqpp::mosquittopp
{
    private:
        int keepalive;
        Database *db;
        YAML::Node *config;
        int time = 0;
        json data;
        atomic<bool> clear{false};

        void on_connect(int rc);
        void on_message(const struct mosquitto_message *message);
        void handle_message(bool new_msg=false);
        void on_subscribe(int mid, int qos_count, const int *granted_qos);

        void setTimeout(int delay);
        void stop();
    public:
        NowPlaying(YAML::Node *config, Database *db);
        ~NowPlaying();
        bool send_message(const char * _topic, const char * _message, bool retain = false);
};

#endif