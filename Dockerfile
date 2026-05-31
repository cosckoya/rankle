FROM kalilinux/kali-rolling:latest

LABEL description="Toolbox" \
      maintainer="cosckoya@mail.me"

# Set the working directory
WORKDIR /root

# Install Base Packages
ENV DEBIAN_FRONTEND=noninteractive

# Update and install base packages in one RUN command to reduce image layers
RUN apt-get update -qq && \
    apt-get install -qq -y --no-install-recommends \
        ca-certificates \
        apt-transport-https \
        lsb-release \
        gnupg \
        wget \
        curl \
        iputils-ping \
        nmap \
        unzip \
        git \
        jq \
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        libffi-dev \
        libncurses5-dev \
        libncursesw5-dev \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install asdf
RUN git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.18.0 && \
    echo '. "$HOME/.asdf/asdf.sh"' >> ~/.bashrc && \
    echo '. "$HOME/.asdf/completions/asdf.bash"' >> ~/.bashrc

# Validate installation
RUN python3 --version && \
    bash -c '. ~/.asdf/asdf.sh && asdf --version'

# Use non-root user for better security
RUN useradd -m -s /bin/bash toolbox && \
    chown -R toolbox:toolbox /home/toolbox

USER toolbox
WORKDIR /home/toolbox
