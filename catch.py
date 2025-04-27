from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# Dossier où enregistrer les fichiers reçus
UPLOAD_DIR = "./uploads"

# S'assurer que le dossier existe
os.makedirs(UPLOAD_DIR, exist_ok=True)

class SimplePUTHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        # Récupère le chemin envoyé par le client
        filepath = self.path.lstrip('/')  # Enlever le / au début
        full_path = os.path.join(UPLOAD_DIR, filepath)

        # Créer les sous-dossiers si besoin
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Lire le contenu envoyé
        content_length = int(self.headers['Content-Length'])
        content = self.rfile.read(content_length)

        # Écrire le fichier sur le disque
        with open(full_path, 'wb') as f:
            f.write(content)

        print(f"[+] Fichier reçu : {full_path}")

        # Répondre au client
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    server_address = ('', 8080)  # écoute sur toutes les interfaces, port 8080
    httpd = HTTPServer(server_address, SimplePUTHandler)
    print("[*] Serveur HTTP démarré sur le port 8080...")
    httpd.serve_forever()

