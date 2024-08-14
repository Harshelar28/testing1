from flask import Flask, request, jsonify, render_template
import platform
import psutil 
import socket
import os

app = Flask(__name__)

output_folder = 'C:/Users/HarshShelar'
output_file = 'test.txt'
output_path = os.path.join(output_folder, output_file)

def get_cpu_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"CPU usage is currently at {cpu_usage}%."

def get_ip_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return f"IP Address: {ip_address}"

def get_host_info():
    hostname = socket.gethostname()
    return f"Hostname: {hostname}"

def get_os_info():
    os_name = platform.system()
    version = platform.version()
    return f"Operating System: {os_name}, OS Version: {version}"

def get_architecture_info():
    architecture = platform.machine()
    return f"Architecture: {architecture}"

def get_system_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_name = platform.system()
    os_version = platform.version()
    architecture = platform.machine()
    return f"Hostname: {hostname}, IP Address: {ip_address}, Operating System: {os_name}, Version: {os_version}, Architecture: {architecture}"

def get_overall_memory_info():
    memory = psutil.virtual_memory()
    return f"Total Memory: {memory.total // (1024**3)} GB, Available Memory: {memory.available // (1024**3)} GB, Memory Usage: {memory.percent}%."

def get_overall_disk_info():
    disk = psutil.disk_usage('/')
    return f"Total Disk Space: {disk.total // (1024**3)} GB, Used Disk Space: {disk.used // (1024**3)} GB, Disk Usage: {disk.percent}%."

def chatbot_response(user_input):
    user_input = user_input.lower()
    if "cpu" in user_input:
        return get_cpu_info()
    elif "ip" in user_input:
        return get_ip_info()
    elif "hostname" in user_input or "host" in user_input:
        return get_host_info()
    elif "os" in user_input:
        return get_os_info()
    elif "architecture" in user_input or "amd" in user_input:
        return get_architecture_info()
    elif "memory" in user_input:
        return get_overall_memory_info()
    elif "disk" in user_input:
        return get_overall_disk_info()
    elif "system info" in user_input:
        return get_system_info()
    else:
        return "I'm sorry, I didn't understand that. You can ask me about CPU/ memory/ disk/ ip/ hostname/ host/ version/ os/ architecture/ system info."

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    response_message = chatbot_response(user_input)
    return jsonify({'response': response_message})

def main():
    os.makedirs(output_folder, exist_ok=True)
    with open(output_path, 'w') as file:
        file.write("Hello! I am your system info chatbot. I will provide you all detailed information about your system. How can I help you today?\n")
        while True:
            user_input = input()
            if user_input.lower() in ["exit", "quit", "bye"]:
                file.write("Goodbye!\n")
                break
            response = chatbot_response(user_input)
            file.write(f"You:- {user_input}\n")
            file.write(f"System Chatbot:- {response}\n")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
