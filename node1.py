import socket, json, pickle, logging, logging.config, os

# variables globales
logging.config.fileConfig("/home/noa/tcp/logs/log.conf")
logger = logging.getLogger(__name__)
HOST = "192.168.0.203"
PORT = 1111
BUFFER = 4096
UPLOAD_FOLDER = "/home/dorian/tcp/uploads"  # dossier où stocker les fichiers
NODES = [("192.168.0.203", 1111)]

# fonction pour transférer l'info du nouveau noeud découvert (ip, port) aux autres noeuds du maillage
def send_new_node(new_node):
    global NODES
    for node in NODES:
        if node == new_node or node[0] == HOST:
            continue
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(node)
                message = {"type": "NEW_NODE", "ip": new_node[0], "port": new_node[1]}
                s.sendall(json.dumps(message).encode())
                logger.info(f"Nouveau noeud envoyé à {node}")
        except Exception as e:
            logger.error(f"Erreur pour contacter {node}: {e}")

def main():
    global NODES
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # créer le dossier si inexistant

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logger.info(f"Serveur lancé sur {HOST}:{PORT}")

        try:
            while True:
                conn, addr = s.accept()
                with conn:
                    logger.info(f"Connexion de {addr}")
                    data = conn.recv(BUFFER)

                    if not data:
                        break

                    # ⚡ On essaie de décoder en JSON
                    try:
                        message = json.loads(data.decode())
                    except Exception:
                        logger.error("Impossible de décoder le message JSON")
                        continue

                    # --- Gestion des différents types ---
                    if message["type"] == "HELLO":
                        ip, port = addr[0], message["port"]
                        new_node = (ip, port)
                        if new_node not in NODES:
                            NODES.append(new_node)
                            logger.info(f"Nœud ajouté : {ip}:{port}")
                            logger.debug(f"Liste des nœuds connus : {NODES}")
                            send_new_node(new_node)

                    elif message["type"] == "REQUEST_NODES":
                        logger.info("Envoi de la liste des nœuds")
                        nodes_bytes = pickle.dumps(NODES)
                        conn.sendall(nodes_bytes)

                    elif message["type"] == "UPLOAD_FILE":
                        filename = message["filename"]
                        filesize = message["filesize"]
                        logger.info(f"Réception du fichier {filename} ({filesize} octets)")

                        filepath = os.path.join(UPLOAD_FOLDER, filename)
                        with open(filepath, "wb") as f:
                            remaining = filesize
                            while remaining > 0:
                                chunk = conn.recv(min(BUFFER, remaining))
                                if not chunk:
                                    break
                                f.write(chunk)
                                remaining -= len(chunk)

                        logger.info(f"Fichier stocké dans DFS : {filepath}")
        except KeyboardInterrupt:
            logger.warning("Arrêt du serveur demandé par l'utilisateur.")
        except Exception as e:
            logger.error(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    main()
