# Docker Commands for SDN_VNF_REOC Project

This README provides a list of important Docker commands used in the SDN_VNF_REOC project. These commands are essential for building, running, and managing Docker containers and images.

## Building Docker Images

To build Docker images for the services defined in the `create_dockers.py` script (or simply execute the script):

```bash
docker build -t <image_name> -f <Dockerfile> .
```

Replace `<image_name>` with the desired image name and `<Dockerfile>` with the path to the Dockerfile.

## Running Docker Containers

To run a Docker container:

```bash
docker run -d --name <container_name> -e <ENV_VAR>=<value> <image_name>
```

- `-d` runs the container in detached mode.
- `--name` specifies the container name.
- `-e` sets environment variables inside the container.

Example:

```bash
docker run -d --name gateway_finale1-container -e GWF_NAME=your_gateway_name gateway_finale1-image
```

## Managing Docker Containers

### Stopping a Container

To stop a running container:

```bash
docker stop <container_name>
```

### Killing a Container

To forcefully stop a container:

```bash
docker kill <container_name>
```

### Removing a Container

To remove a stopped container:

```bash
docker rm <container_name>
```

## Show running container

```bash
sudo docker ps
```

## Accessing a Running Container

To enter a running container and execute commands:

```bash
docker exec -it <container_name> /bin/sh
```

Replace `/bin/sh` with `/bin/bash` if the container uses bash.

## Viewing Container Logs

To view the logs of a container:

```bash
docker logs <container_name>
```

## Notes

- Ensure that the necessary dependencies are installed in the Dockerfiles using `npm install` commands.
- Modify environment variables as needed for different configurations.


net