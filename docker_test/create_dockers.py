import os
import subprocess

# List of Dockerfiles and corresponding image names and IP addresses
services = {
    'app1': ('application.Dockerfile', '172.18.0.2'),
    'app2': ('application.Dockerfile', '172.18.0.3'),
    'app3': ('application.Dockerfile', '172.18.0.4'),
    'server': ('server.Dockerfile', '172.18.0.5'),
    'gateway_intermediaire': ('gateway_intermediate.Dockerfile', '172.18.0.6'),
    'gateway_finale1': ('gateway_final.Dockerfile', '172.18.0.7')
}

# Base directory for Dockerfiles
base_dir = './'

# Create a custom Docker network
network_name = 'custom_net'
subprocess.run(['docker', 'network', 'create', '--subnet=172.18.0.0/16', network_name], check=True)

# Function to build Docker images and run containers
def build_and_run_images():
    for service, (dockerfile, ip_address) in services.items():
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

        # Build the Docker image
        print(f'Building {image_name} from {dockerfile_path} with {build_arg_name}={service}')
        subprocess.run([
            'docker', 'build', '-t', image_name,
            '--build-arg', f'{build_arg_name}={service}',
            '-f', dockerfile_path, base_dir
        ], check=True)

        # Run the Docker container with a specific IP address
        container_name = f'{service}-container'
        print(f'Running {container_name} with IP {ip_address}')
        subprocess.run([
            'docker', 'run', '-d', '--name', container_name,
            '--network', network_name, '--ip', ip_address,
            image_name
        ], check=True)

if __name__ == "__main__":
    build_and_run_images()
