# Powered by CodeByTushu | Developed by Tushpendra Kumar | https://codebytushu.com
# app.py

from flask import Flask, render_template
import subprocess

app = Flask(__name__)

# Function to run a Linux command and return the output
def run_linux_command(command):
    try:
        # shell=True is needed to run shell commands directly
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        # We process the output to split into lines for HTML display
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        return [f"Error running command: {e.stderr.strip()}"]
    except FileNotFoundError:
        return ["Error: Command not found or Linux not detected."]

@app.route('/')
def dashboard():
    # Run a simple Linux command (Disk Free - Human readable)
    disk_data_lines = run_linux_command("df -h")
    
    # Extract headers and rows
    if disk_data_lines and "Filesystem" in disk_data_lines[0]:
        headers = disk_data_lines[0].split()
        data_rows = [line.split() for line in disk_data_lines[1:] if line.strip()]
    else:
        headers = ["Status"]
        data_rows = [[disk_data_lines[0]]] if disk_data_lines else [["No data."]]

    return render_template('index.html', headers=headers, data_rows=data_rows)

if __name__ == '__main__':
    # Run the Flask app
    # host='0.0.0.0' allows access from network, perfect for testing
    app.run(debug=True, host='0.0.0.0', port=5000)