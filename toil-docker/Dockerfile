FROM python:3.11

# https://toil.readthedocs.io/en/latest/gettingStarted/install.html#extras
RUN apt update && \
    apt install -y \
    build-essential \
    python-dev \
    libssl-dev \
    libffi-dev

RUN pip install toil[all]

CMD ["toil", "server"]
