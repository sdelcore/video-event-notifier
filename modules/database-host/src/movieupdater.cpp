#include <movieupdater.h>

MovieUpdater::MovieUpdater(YAML::Node *config, Database *db) : mosquittopp("host-updater"), db(db) {
    mosqpp::lib_init();        // Mandatory initialization for mosquitto library
    this->keepalive = 60;    // Basic configuration setup for myMosq class
    this->config = config;
    string host = (*this->config)["MQTT"]["url"].as<string>();
    int port = (*this->config)["MQTT"]["port"].as<int>();

    connect_async(host.c_str(), port, keepalive);
    loop_start();
};

MovieUpdater::~MovieUpdater() {
    loop_stop();            // Kill the thread
    mosqpp::lib_cleanup();    // Mosquitto library cleanup
}

void MovieUpdater::on_connect(int rc)
{
	if(rc == 0)
    {
        printf("HOST: Updater connected to %s\n", (*this->config)["MQTT"]["url"].as<string>().c_str());
        string topic = (*this->config)["MQTT"]["Topics"]["update"].as<string>();
        subscribe(NULL, topic.c_str());
    }
    
}

void MovieUpdater::on_subscribe(int mid, int qos_count, const int *granted_qos)
{

}

void MovieUpdater::on_message(const struct mosquitto_message *message)
{
    int time;
    int events;
    string msg = string((char *)message->payload, message->payloadlen);
    json data = json::parse(msg);
    string movie = data["video"]["title"].get<string>();

    printf(msg.c_str());
    printf("\n");

    //convert HH:MM:SS to seconds
    if (data["time"].is_string())
    {
        string time_string = data["time"].get<string>();
        int h, m, s= 0;

        if (sscanf(time_string.c_str(), "%d:%d:%d", &h, &m, &s) >= 2)
        {
            time = h *3600 + m*60 + s;
        }

    }
    else
    {
        time = data["time"].get<int>();
    }
    

    events  = data["events"].get<int>();

    db->insertTime(movie.c_str(), time, events);
}