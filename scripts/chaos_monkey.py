import docker
import random

def run_chaos():
    print("🚀 Iniciando el agente de caos...")
    try:
        # Intenta conectar con el motor de Docker
        client = docker.from_env()
        print("✅ Conectado al socket de Docker exitosamente.")
        
        # Busca los contenedores vivos
        containers = client.containers.list(filters={"status": "running"})
        print(f"📦 Se encontraron {len(containers)} contenedores corriendo en total.")
        
        # Filtro de seguridad
        targets = [c for c in containers if "watchtower" not in c.name and "tunnel" not in c.name]
        
        if not targets:
            print("🛡️ No hay víctimas disponibles. Todo está demasiado seguro...")
            return

        # El golpe
        victim = random.choice(targets)
        print(f"🔥 CAOS: Eligiendo víctima... {victim.name}")
        victim.exec_run("sh -c 'kill -9 1'", detach=True)
        print(f"💀 {victim.name} ha sido asesinado. Verificando resiliencia...")
        
    except docker.errors.APIError:
        print(f"💀 {victim.name} colapsó tan rápido que cortó la conexión. ¡Éxito!")
    except Exception as e:
        print(f"❌ Error fatal inesperado: {e}")

if __name__ == "__main__":
    run_chaos()