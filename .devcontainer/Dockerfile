ARG VARIANT=bullseye

FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

ENV DEBIAN_FRONTEND=noninteractive

# trunk-ignore(hadolint/DL3009)
RUN apt-get update
# trunk-ignore(hadolint/DL3008)
# trunk-ignore(hadolint/DL3015)
# trunk-ignore(hadolint/DL3059)
RUN apt-get install -y apt-utils
# trunk-ignore(hadolint/DL3059)
RUN apt-get upgrade -y
# trunk-ignore(hadolint/DL3008)
# trunk-ignore(hadolint/DL3015)
# trunk-ignore(hadolint/DL3059)
RUN apt-get install -y python3-pip \
  npm jq gnupg software-properties-common wget curl git openssh-client
RUN apt-get autopurge -y && \
  apt-get clean all && rm -rf /var/cache/apt
