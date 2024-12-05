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
        # Determine the build argument name based on the service
        build_arg_name = ''
        if 'app' in service:
            build_arg_name = 'APP_DEVICE_NAME'
        elif 'device' in service:
            build_arg_name = 'DEVICE_NAME'
        elif 'gateway_finale' in service:
            build_arg_name = 'GWF_NAME'
        elif 'gateway_intermediaire' in service:
            build_arg_name = 'GWI_NAME'
        elif 'server' in service:
            build_arg_name = 'SRV_NAME'

        print(f'Building {image_name} from {dockerfile_path} with {build_arg_name}={service}')
        subprocess.run([
            'docker', 'build', '-t', image_name,
            '--build-arg', f'{build_arg_name}={service}',
            '-f', dockerfile_path, base_dir
        ], check=True)

if __name__ == "__main__":
    build_images()
