import os
import hashlib
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'evidence_vault'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>HS Forensic Dashboard</title>
    <style>
        body { font-family: sans-serif; background: #1a1a1a; color: #00ff00; padding: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #333; padding: 10px; text-align: left; }
        th { background: #333; }
        a { color: #00ff00; text-decoration: none; border: 1px solid #00ff00; padding: 5px; }
        .header { border-bottom: 2px solid #00ff00; padding-bottom: 10px; }
    </style>
</head>
<body>
    <div class="header"><h1>[CONFIDENTIAL] Homeland Security Evidence Vault</h1></div>
    <table>
        <tr><th>Filename</th><th>SHA-256 Hash (Integrity)</th><th>Action</th></tr>
        {% for file in files %}
        <tr>
            <td>{{ file.name }}</td>
            <td><code>{{ file.hash }}</code></td>
            <td><a href="/download/{{ file.name }}">DOWNLOAD EVIDENCE</a></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def get_sha256(filename):
    sha256_hash = hashlib.sha256()
    with open(os.path.join(UPLOAD_FOLDER, filename), "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@app.route('/')
def index():
    files_info = []
    for filename in os.listdir(UPLOAD_FOLDER):
        files_info.append({'name': filename, 'hash': get_sha256(filename)})
    return render_template_string(DASHBOARD_HTML, files=files_info)

@app.route('/upload', methods=['POST'])
def upload_file():
    filename = "shadow.txt"
    with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
        f.write(request.data)
    print(f"\n[+] ALERT: Evidence received and hashed.")
    return "Evidence Locked", 200

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
