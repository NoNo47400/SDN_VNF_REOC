from flask import Flask, render_template
import subprocess
import os

app = Flask(__name__,
            template_folder=os.getcwd(),  # Répertoire des templates (HTML)
            static_folder=os.getcwd())   # Répertoire des fichiers statiques (CSS)

# Route pour servir la page HTML principale
@app.route('/')
def index():
    return render_template('index.html')

# Route pour exécuter test.py
@app.route('/launch-vnf-monitoring', methods=['GET'])
def launch_vnf_monitoring():
    try:
        result = subprocess.check_output(['python3', '../sdn/launch_vnf_monitoring.py'], text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Erreur : {e.output}", 500

# Route pour exécuter test2.py
@app.route('/launch-vnf-gi/<dscp>', methods=['GET'])
def launch_vnf_gi(dscp):
    try:
        result = subprocess.check_output(['python3', '../sdn/launch_vnf_gi.py', dscp], text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Erreur : {e.output}", 500

# Route pour la requête CURL
@app.route('/get-bitrate', methods=['GET'])
def run_curl():
    try:
        result = subprocess.check_output(['curl', '-X', 'GET', 'http://172.17.0.19:8181/bitrate'], text=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output, 500

# Route pour les logs Docker
@app.route('/docker-logs/service', methods=['GET'])
def docker_logs_service():
    try:
        result = subprocess.check_output(['docker', 'logs', 'mn.service', '--tail', '30'], text=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output, 500
    
# Route pour les logs Docker
@app.route('/docker-logs/gi', methods=['GET'])
def docker_logs_gi():
    try:
        result = subprocess.check_output(['docker', 'logs', 'mn.gI', '--tail', '30'], text=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output, 500

# Route pour les logs Docker
@app.route('/docker-logs/gi-vnf', methods=['GET'])
def docker_logs_gi_vnf():
    try:
        result = subprocess.check_output(['docker', 'logs', 'mn.vnf_gI', '--tail', '30'], text=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output, 500
    
# Route pour les logs Docker
@app.route('/docker-logs/vnf-monitoring', methods=['GET'])
def docker_logs_vnf_monitoring():
    try:
        result = subprocess.check_output(['docker', 'logs', 'mn.vnf_monitoring', '--tail', '30'], text=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output, 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1234)



