FROM ubuntu:22.04 as rpm2deb

#build stage 2
FROM python:3.10

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    python3-psycopg2 \
    sshpass \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/
WORKDIR /usr/src/app/scanner/

# pass the entrypoint-script name as a docker build-time argument
ARG entrypoint_arg
# set the script-name to an ENV variable
ENV env_entrypoint=$entrypoint_arg
# provide execute permission to the entrypoint-script
RUN chmod +x $env_entrypoint
# set the script as entrypoint
ENTRYPOINT $env_entrypoint