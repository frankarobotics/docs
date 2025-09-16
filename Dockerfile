FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

ARG USER_UID=1001
ARG USER_GID=1001
ARG USERNAME=user

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    bash \
    bash-completion \
    git \
    build-essential \
    npm \
    ssh-client \
    sudo \
    vim \
    python3-pip \
    python3-wheel \
    python3-setuptools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --ignore-installed --no-cache-dir \
    sphinx==5.1.1 \
    sphinx-rtd-theme==1.0.0 \
    sphinx-reredirects==0.1.1 \
    myst-parser==0.18.0 \
    "docutils<0.18" \
    vcstool

WORKDIR /workspace

# Setup user configuration
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && chown $USERNAME:$USERNAME /workspace

USER $USERNAME 

COPY entrypoint.sh /
CMD [ "/bin/bash" ]
ENTRYPOINT [ "/entrypoint.sh" ]
