FROM python:3.10.5-bullseye

RUN apt-get update -y && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install --no-install-recommends \
    sudo \
    vim \
    git \
    zsh

ARG CONTAINER_USER_NAME

ARG CONTAINER_USER_PASSWORD

ARG CONTAINER_USER_GROUP=${CONTAINER_USER_NAME}

RUN addgroup ${CONTAINER_USER_GROUP}

RUN useradd -m -g ${CONTAINER_USER_GROUP} -s /usr/bin/zsh ${CONTAINER_USER_NAME} -p ${CONTAINER_USER_PASSWORD}

RUN usermod -aG ${CONTAINER_USER_GROUP} ${CONTAINER_USER_NAME}

RUN echo "${CONTAINER_USER_GROUP} ALL=(ALL) ALL" >> /etc/sudoers

RUN usermod -aG sudo ${CONTAINER_USER_NAME}

RUN usermod -aG sudo root

RUN echo "sudo ALL=(ALL) ALL" >> /etc/sudoers

RUN sh -c 'echo root:${CONTAINER_USER_PASSWORD} | chpasswd'

ARG WORKDIR=/home/${CONTAINER_USER_NAME}/app

WORKDIR ${WORKDIR}

ENV PYTHONPATH=${WORKDIR}

RUN chown -R ${CONTAINER_USER_NAME}:${CONTAINER_USER_GROUP} ${WORKDIR}

USER ${CONTAINER_USER_NAME}

# RUN pip install \
#     --disable-pip-version-check \
#     --no-cache-dir \
#     --no-compile \
#     poetry

ARG APP_PORT

EXPOSE ${APP_PORT}

CMD ["tail", "-f", "/dev/null"]
