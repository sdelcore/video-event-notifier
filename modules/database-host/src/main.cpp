#include <nowplaying.h>
#include <movieupdater.h>
#include "yaml-cpp/yaml.h"

using namespace std;

int main() {
    printf("MAIN: starting program\n");
    YAML::Node config = YAML::LoadFile("../../config.yml");
    
    Database db(&config);
    MovieUpdater updater(&config, &db);
    NowPlaying player(&config, &db);

    while(1){}

    return 0;
}