FROM python:3.10

# https://toil.readthedocs.io/en/latest/gettingStarted/install.html#extras
RUN apt update && \
    apt install -y \
    build-essential \
    python-dev \
    libssl-dev \
    libffi-dev

RUN pip install toil[all]

# These lines install docker to enable docker in docker in the celery containers so they can run workflows with
# image requirements
RUN apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt update && \
    apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

CMD ["toil", "server"]
