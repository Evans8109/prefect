# FROM --platform=linux/amd64 python:3.12-slim-bullseye
FROM python:3.12-slim-bullseye
ENV TZ=Asia/Taipei
ENV PYTHONPATH="/usr/local/prefect/"

# 复制文件到容器中
COPY requirements.txt requirements.txt
COPY ./src /usr/local/prefect/src/
#COPY ./.ssh/ /root/.ssh/

# 使用 SSH 克隆私有仓库
RUN --mount=type=ssh git clone git@github.com:Evans8109/prefect.git /usr/local/prefect/

# 更新包列表并安装依赖
RUN apt-get update && \
    apt-get install git zsh vim curl wget zip procps gcc python3-dev -y && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    mkdir -p /root/.ssh && chmod 700 /root/.ssh && \
    chmod 600 /root/.ssh/id_rsa && \
    echo "Y" | sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 安装 Python 依赖
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install google-cloud-storage mysql-connector-python google-cloud-bigquery google-cloud-translate pandas pandas-gbq

# 配置 Prefect
RUN prefect config set PREFECT_LOGGING_LOG_PRINTS=True
RUN prefect cloud login --key pnu_JUTq5fPlvneM1qIFqCl3EtwbMHjPqb3UP0te --workspace evans-chen/default

# 设置 Python 路径
#ENV PYTHONPATH="$PYTHONPATH:/usr/local/prefect/"