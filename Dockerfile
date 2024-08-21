FROM --platform=linux/amd64 python:3.12-slim-bullseye

ENV TZ=Asia/Taipei


COPY requirements.txt requirements.txt
#COPY ./src/ app/src/
COPY ./src /usr/local/prefect/src/
COPY ./.ssh/ /root/.ssh/

RUN apt-get update && \
    apt-get install git zsh vim curl wget zip procps gcc python3-dev -y && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    mkdir -p /root/.ssh/ && \
    echo "Y" | sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install google-cloud-storage

# Prefect config
RUN prefect config set PREFECT_LOGGING_LOG_PRINTS=True 
RUN prefect cloud login --key pnu_JUTq5fPlvneM1qIFqCl3EtwbMHjPqb3UP0te --workspace evans-chen/default

#ENV PYTHONPATH="$PYTHONPATH:/app/src"
ENV PYTHONPATH="$PYTHONPATH:/usr/local/prefect/"