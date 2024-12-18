#include <iostream>
#include <cstring>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <string>

const int port = 0;
const char* server = "";

struct TheHackz {
    std::string greet() {
        return "Hello Fella.";
    }
};

int main() {
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        return 1;
    }

    SOCKET cs = socket(AF_INET, SOCK_STREAM, 0);
    if (cs == INVALID_SOCKET) {
        WSACleanup();
        return 1;
    }

    sockaddr_in SA;
    SA.sin_family = AF_INET;
    SA.sin_port = htons(port);
    SA.sin_addr.s_addr = inet_addr(server); 

    if (connect(cs, (sockaddr*)&SA, sizeof(SA)) == SOCKET_ERROR) {
        closesocket(cs);
        WSACleanup();
        return 1;
    }

    TheHackz hackz;

    while (true) {
        char buffer[1024] = {0};
        int brec = recv(cs, buffer, sizeof(buffer) - 1, 0);
        if (brec > 0) {
            buffer[brec] = '\0';

            if (strcmp(buffer, "./greet") == 0) { 
                std::string greet = hackz.greet();
                send(cs, greet.c_str(), greet.length(), 0);
            }

        } else if (brec == 0) {
            break; 
        } else {
            break; 
        }
    }

    closesocket(cs);
    WSACleanup();
    return 0;
}
