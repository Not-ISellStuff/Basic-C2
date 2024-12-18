import socket, os, json

class Builder:
    def __init__(self):
        pass

    def ePORT(self, path, value):
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.strip().startswith('const int port ='):
                lines[i] = f'const int port = {value};\n' 
                break

        with open(path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

    def eSERVER(self, path, value):
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.strip().startswith('const char* server ='):
                lines[i] = f'const char* server = "{value}";\n' 
                break

        with open(path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

    def compile(self):
        dir = os.getcwd()

        try:
            os.remove("Output/main.exe")
        except:
            pass

        os.system(f'g++ {dir}\\client.cpp -o Output/main -lws2_32')

    def buildLOCAL(self, port):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        self.ePORT("client.cpp", port)
        self.eSERVER("client.cpp", ip_address)

        with open("settings.json", "r") as f:
            data = json.load(f)

        data['server'] = ip_address
        data['port'] = port

        with open("settings.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        self.compile()

    def build(self, server, port):
        self.ePORT("client.cpp", port)
        self.eSERVER("client.cpp", server)
        
        with open("settings.json", "r") as f:
            data = json.load(f)

        data['server'] = server
        data['port'] = port

        with open("settings.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        self.compile()
