import os
import subprocess

def kill_all_docker_containers():
    try:
        # Obtenir la liste des conteneurs actifs
        result = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True)
        container_ids = result.stdout.strip().split("\n")

        if not container_ids or container_ids == ['']:
            print("Aucun conteneur en cours d'exécution.")
            return

        # Supprimer tous les conteneurs
        subprocess.run(["docker", "rm", "-f"] + container_ids)
        print("Tous les conteneurs ont été arrêtés et supprimés avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")


# List of Dockerfiles and corresponding image names and IP addresses
services = {
    'app1': ('application.Dockerfile'),
    'app2': ('application.Dockerfile'),
    'app3': ('application.Dockerfile'),
    'server': ('server.Dockerfile'),
    'gateway_intermediaire': ('gateway_intermediate.Dockerfile'),
    'gateway_final1': ('gateway_final.Dockerfile'),
    'dev1_gf1': ('device.Dockerfile'),
    'dev2_gf1': ('device.Dockerfile'),
    'dev3_gf1': ('device.Dockerfile'),
    'gateway_final2': ('gateway_final.Dockerfile'),
    'dev1_gf2': ('device.Dockerfile'),
    'dev2_gf2': ('device.Dockerfile'),
    'dev3_gf2': ('device.Dockerfile'),
    'gateway_final3': ('gateway_final.Dockerfile'),
    'dev1_gf3': ('device.Dockerfile'),
    'dev2_gf3': ('device.Dockerfile'),
    'dev3_gf3': ('device.Dockerfile'),
    'vnf_monitoring': ('vnf_monitoring.Dockerfile'),
}

# Base directory for Dockerfiles
base_dir = './'

# Create a custom Docker network
network_name = 'custom_net'

# Function to clean up existing Docker containers and images
def cleanup_docker():
    print("Cleaning up existing Docker containers...")
    for service in services.keys():
        container_name = f'{service}-container'
        subprocess.run(['docker', 'rm', '-f', container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Cleanup complete.")

# Function to build Docker images and run containers
def build_and_run_images():
    # Ensure the custom network exists
    subprocess.run(['docker', 'network', 'create', '--subnet=172.18.0.0/16', network_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for service, (dockerfile) in services.items():
        dockerfile_path = os.path.join(base_dir, dockerfile)
        image_name = f'{service}-image'

        # Determine the build argument name based on the service
        build_arg_name = ''
        if 'app' in service:
            build_arg_name = 'APP_DEVICE_NAME'
        elif 'device' in service:
            build_arg_name = 'DEVICE_NAME'
        elif 'gateway_final' in service:
            build_arg_name = 'GWF_NAME'
        elif 'gateway_intermediaire' in service:
            build_arg_name = 'GWI_NAME'
        elif 'server' in service:
            build_arg_name = 'SRV_NAME'
        elif 'monitoring_vnf' in service:
            build_arg_name = 'VNF_MONITORING_NAME'

        # Build the Docker image
        print(f'Building {image_name} from {dockerfile_path} with {build_arg_name}={service}')
        subprocess.run([
            'docker', 'build', '-t', image_name,
            '--build-arg', f'{build_arg_name}={service}',
            '-f', dockerfile_path, base_dir
        ], check=True)

        # Run the Docker container with a specific IP address
        # container_name = f'{service}-container'
        # print(f'Running {container_name} with IP {ip_address}')
        # subprocess.run([
        #     'docker', 'run', '-d', '--name', container_name,
        #     '--network', network_name, '--ip', ip_address,
        #     image_name
        # ], check=True)

if __name__ == "__main__":
    kill_all_docker_containers()
    cleanup_docker()
    build_and_run_images()
