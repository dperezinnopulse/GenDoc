import socket

def check_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('localhost', 8080))
        sock.close()
        
        if result == 0:
            print("✅ Puerto 8080 está abierto y respondiendo")
            return True
        else:
            print("❌ Puerto 8080 no responde")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Verificando servidor en puerto 8080...")
    check_server()
