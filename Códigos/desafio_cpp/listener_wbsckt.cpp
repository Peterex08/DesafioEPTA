#include <iostream>
#include <thread>
#include <mutex>
#include <map>
#include <string>
#include <vector>
#include <websocketpp/config/asio_no_tls_client.hpp>
#include <websocketpp/client.hpp>
#include <jsoncpp/json/json.h>

using namespace std;

typedef websocketpp::client<websocketpp::config::asio_client> client;
typedef websocketpp::connection_hdl connection_hdl;

mutex data_mutex;


map<string, vector<float>> sensor_data;
map<string, string> gps_data;

void handle_sensor_message(const string& message) {
    lock_guard<mutex> lock(data_mutex);

    Json::Value jsonData;
    Json::Reader reader;
    if (!reader.parse(message, jsonData)) {
        cerr << "Erro ao parsear mensagem de sensor." << endl;
        return;
    }

    string type = jsonData["type"].asString();
    vector<float> values;
    for (const auto& val : jsonData["values"]) {
        values.push_back(val.asFloat());
    }

    sensor_data[type] = values;
}


void handle_gps_message(const string& message) {
    lock_guard<mutex> lock(data_mutex);

    Json::Value jsonData;
    Json::Reader reader;
    if (!reader.parse(message, jsonData)) {
        cerr << "Erro ao parsear mensagem de GPS." << endl;
        return;
    }

    gps_data["latitude"] = to_string(jsonData["latitude"].asFloat());
    gps_data["longitude"] = to_string(jsonData["longitude"].asFloat());
    gps_data["altitude"] = to_string(jsonData["altitude"].asFloat());
    gps_data["speed"] = to_string(jsonData["speed"].asFloat());
}


void sensor_thread(const string& uri) {
    client c;

    c.init_asio();
    c.set_message_handler([&](connection_hdl, client::message_ptr msg) {
        handle_sensor_message(msg->get_payload());
    });

    websocketpp::lib::error_code ec;
    auto con = c.get_connection(uri, ec);
    if (ec) {
        cerr << "Erro ao conectar aos sensores: " << ec.message() << endl;
        return;
    }

    c.connect(con);
    c.run();
}


void gps_thread(const string& uri) {
    client c;

    c.init_asio();
    c.set_message_handler([&](connection_hdl, client::message_ptr msg) {
        handle_gps_message(msg->get_payload());
    });

    websocketpp::lib::error_code ec;
    auto con = c.get_connection(uri, ec);
    if (ec) {
        cerr << "Erro ao conectar ao GPS: " << ec.message() << endl;
        return;
    }

    c.connect(con);
    c.run();
}


void print_data() {
    while (true) {
        lock_guard<mutex> lock(data_mutex);

        cout << "Sensores: " << endl;
        for (const auto& [type, values] : sensor_data) {
            cout << type << ": ";
            for (const auto& v : values) {
                cout << v << " ";
            }
            cout << endl;
        }

        cout << "GPS: ";
        for (const auto& [key, value] : gps_data) {
            cout << key << ": " << value << " ";
        }
        cout << endl;

        this_thread::sleep_for(chrono::milliseconds(500));
    }
}

int main() {
    string sensor_uri = "ws://192.168.1.10:8080/sensors/connect?types=[\"android.sensor.accelerometer\",\"android.sensor.gyroscope\",\"android.sensor.magnetic_field\"]";
    string gps_uri = "ws://192.168.1.10:8080/gps";

    thread sensor_thread_instance(sensor_thread, sensor_uri);
    thread gps_thread_instance(gps_thread, gps_uri);

    print_data();

    sensor_thread_instance.join();
    gps_thread_instance.join();

    return 0;
}
