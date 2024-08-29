FROM --platform=linux/amd64 python:3.12-slim-bullseye

ENV TZ=Asia/Taipei

# 安裝必要的軟件包
RUN apt-get update && \
    apt-get install git zsh vim curl wget zip procps gcc python3-dev -y && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 複製代碼和設置 SSH 密鑰
COPY requirements.txt requirements.txt
COPY ./src /usr/local/prefect/src/
COPY ./.ssh/ /root/.ssh/

# 設置 SSH 密鑰權限
RUN chmod 600 /root/.ssh/id_rsa

# 安裝 Oh My Zsh
RUN echo "Y" | sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 安裝 Python 庫
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install google-cloud-storage mysql-connector-python google-cloud-bigquery google-cloud-translate pandas

# 使用 BuildKit 的 SSH 功能克隆私有 Git 存儲庫
RUN --mount=type=ssh git clone git@github.com:Evans8109/prefect.git /usr/local/prefect/

# 配置 Prefect
RUN prefect config set PREFECT_LOGGING_LOG_PRINTS=True 
RUN prefect cloud login --key pnu_JUTq5fPlvneM1qIFqCl3EtwbMHjPqb3UP0te --workspace evans-chen/default

# 設置 PYTHONPATH 環境變量
ENV PYTHONPATH="$PYTHONPATH:/usr/local/prefect/" 