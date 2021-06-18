# Exemple of fastapi ldap

## Standard build
```
➜  docker build -t fastapi_ldap -f Dockerfile . 
```
## Build with docker-slim
```
➜  ./docker_slim_tool/docker-slim build --target fastapi_ldap --tag fastapi_ldap-slim 
```
## Show docker images
```
➜  docker image ls -f 'reference=fastapi_*'                                           
REPOSITORY                            TAG       IMAGE ID       CREATED          SIZE
fastapi_ldap-slim                     latest    ac50b31587f4   20 seconds ago   56.9MB
fastapi_ldap                          latest    ceeb28edede1   12 minutes ago   161MB
```