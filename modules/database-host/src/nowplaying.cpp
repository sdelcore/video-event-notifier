#include <nowplaying.h>

NowPlaying::NowPlaying(YAML::Node *config, Database *db) : mosquittopp("host-now-playing"), db(db) {
    mosqpp::lib_init();        // Mandatory initialization for mosquitto library
    this->keepalive = 60;    // Basic configuration setup for myMosq class
    this->config = config;
    string host = (*this->config)["MQTT"]["url"].as<string>();
    int port = (*this->config)["MQTT"]["port"].as<int>();
    connect_async(host.c_str(), port, keepalive);
    loop_start();
};

NowPlaying::~NowPlaying() {
    loop_stop();            // Kill the thread
    mosqpp::lib_cleanup();    // Mosquitto library cleanup
}

void NowPlaying::on_connect(int rc)
{
	if(rc == 0){
        printf("HOST: Now Playing connected to %s\n", (*this->config)["MQTT"]["url"].as<string>().c_str());
        string topic = (*this->config)["MQTT"]["Topics"]["now playing"].as<string>();
        subscribe(NULL, topic.c_str());
    }
}

void NowPlaying::on_subscribe(int mid, int qos_count, const int *granted_qos)
{

}

bool NowPlaying::send_message(const char * _topic, const  char * _message, bool retain)
{
    int ret = publish(NULL,_topic, strlen(_message), _message, 1, retain);
    return ( ret == MOSQ_ERR_SUCCESS );
}

void NowPlaying::handle_message(bool new_msg)
{
    if(this->data["playing"].get<int>() == 0)
    {
        return;
    }

    if(new_msg)
    {
        this->time = this->data["time"].get<int>() + (*this->config)["Host"]["time offset"].as<int>();
    }
    else
    {
        this->time++;
    }

    string movie_topic = (*this->config)["MQTT"]["Topics"]["movies"].as<string>();
    string current_movie_topic = (*this->config)["MQTT"]["Topics"]["now playing"].as<string>();
    string movie = this->data["video"]["title"].get<string>();
    
    send_message(movie_topic.c_str(), movie.c_str(), true);
    current_movie_topic += movie;

    int events = db->getEvents(movie.c_str(), time);

    if(events > 0) 
    {
        printf("Event(s): %s\n", to_string(events).c_str());
        send_message(current_movie_topic.c_str(), to_string(events).c_str());
    }

    printf("HOST: time=%d\n", this->time);

    if(this->data["playing"].get<int>() == 1)
    {
        setTimeout(1000);
    }
}

void NowPlaying::on_message(const struct mosquitto_message *message)
{
    printf("HOST: New message recievied.\n");
    stop();
    string msg = string((char *)message->payload, message->payloadlen);
    this->data = json::parse(msg);
    handle_message(true);
}


void NowPlaying::setTimeout(int delay) {
    this->clear = false;
    thread t([=]() {
        if(this->clear) return;
        int time = 0;
        int inc = 10;
        while(time < delay)
        {
            this_thread::sleep_for(std::chrono::milliseconds(inc));
            if(this->clear) return;
            time+=inc;
        }
        if(this->clear) return;
        handle_message();
    });
    t.detach();
}

void NowPlaying::stop() {
    this->clear = true;
}