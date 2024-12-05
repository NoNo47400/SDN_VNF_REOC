import os
import subprocess

# List of Dockerfiles and corresponding image names
services = {
    'app1': 'application.Dockerfile',
    'app2': 'application.Dockerfile',
    'app3': 'application.Dockerfile',
    'server': 'server.Dockerfile',
    'gateway_intermediaire': 'gateway_intermediate.Dockerfile',
    'gateway_finale1': 'gateway_final.Dockerfile'
}

# Base directory for Dockerfiles
base_dir = './'

# Function to build Docker images
def build_images():
    for service, dockerfile in services.items():
        dockerfile_path = os.path.join(base_dir, dockerfile)
        image_name = f'{service}-image'
        print(f'Building {image_name} from {dockerfile_path}')
        subprocess.run(['docker', 'build', '-t', image_name, '-f', dockerfile_path, base_dir], check=True)

if __name__ == "__main__":
    build_images()
