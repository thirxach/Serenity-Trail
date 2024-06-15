from flask import Flask, Response, render_template_string
import subprocess
import threading

app = Flask(__name__)
lock = threading.Lock()
process = None
output_history = []  # store the history of output

@app.route('/')
def index():
    return render_template_string('''
    <html>
        <body>
            <h1>Manual deployment</h1>
            <h3>Deploy should be started automatically when a new commit is pushed to the repository</h3>
            <h3>Click the "Get Last Deployment Log" button to see the last output of the deployment</h3>
            <button onclick="startCommand()">Start deploy</button>
            <button onclick="getLastOutput()">Get Last Deployment Log</button>
            <button onclick="getDockerLogs()">Get Docker Log</button>
            <script>
                function getDockerLogs() {
                    var xhr = new XMLHttpRequest();
                    xhr.open("GET", "/docker_logs", true);
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState == 4 && xhr.status == 200) {
                            document.getElementById('output').textContent = xhr.responseText;
                        }
                    }
                    xhr.send();
                }
            </script>
            <pre id="output">Click 'Start Command' to execute command...</pre>
            <script>
                function startCommand() {
                    var xhr = new XMLHttpRequest();
                    xhr.open("GET", "/start", true);
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState == 4 && xhr.status == 200) {
                            var source = new EventSource("/stream");
                            source.onmessage = function(event) {
                                document.getElementById('output').textContent += event.data + '\\n';
                            }
                        }
                    }
                    xhr.send();
                }

                function getLastOutput() {
                    var xhr = new XMLHttpRequest();
                    xhr.open("GET", "/last_output", true);
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState == 4 && xhr.status == 200) {
                            document.getElementById('output').textContent = xhr.responseText;
                        }
                    }
                    xhr.send();
                }
            </script>
        </body>
    </html>
    ''')

@app.route('/start')
def start():
    global process, output_history
    with lock:
        if process is None or process.poll() is not None:
            output_history = [] # clear the history of output
            process = subprocess.Popen(["tcping", "1.1.1.1"], stdout=subprocess.PIPE, text=True)
            return "Command started"
        else:
            return "Command is already running"

@app.route('/stream')
def stream():
    def generate():
        global process
        if process:
            for line in iter(process.stdout.readline, ''):
                output_history.append(line)  # save the output to history
                yield f"data: {line}\n\n"
            process.stdout.close()
    return Response(generate(), mimetype='text/event-stream')

@app.route('/last_output')
def last_output():
    return "".join(output_history)  # return the history of output

@app.route('/docker_logs')
def docker_logs():
    result = subprocess.run(['docker', 'logs', 'serenity'], stdout=subprocess.PIPE, text=True)
    # result = subprocess.run(['whoami'], stdout=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return "Failed to retrieve logs"

if __name__ == '__main__':
    app.run(debug=True)
