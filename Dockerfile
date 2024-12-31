# Base Image (Ubuntu 24.04, matching the CoppeliaSim version)
FROM ubuntu:24.04

# Install essential packages
RUN apt-get update && apt-get install -y \
    wget \
    libxrender1 \
    libxxf86vm1 \
    libsm6 \
    libxext6 \
    xz-utils \
    libglib2.0-0 \
    libgl1 \
    libglx-mesa0 && \
    ldconfig

# Define user, if needed
ARG USER_NAME=coppelia
ARG USER_ID=1001
ARG GROUP_ID=1001

# Create user and group, only if they don't exist
RUN if ! getent group ${GROUP_ID} >/dev/null; then groupadd -g ${GROUP_ID} ${USER_NAME}; fi && \
    if ! getent passwd ${USER_ID} >/dev/null; then useradd -rm -d /home/${USER_NAME} -s /bin/bash -g ${GROUP_ID} -u ${USER_ID} ${USER_NAME}; fi

# Set CoppeliaSim version and URL as environment variables
ENV COPPELIASIM_VERSION="V4_7_0_rev4"
ENV COPPELIASIM_URL="https://downloads.coppeliarobotics.com/${COPPELIASIM_VERSION}/CoppeliaSim_Pro_${COPPELIASIM_VERSION}_Ubuntu24_04.tar.xz"
ENV COPPELIASIM_DIR="/opt/coppelia"

# Create a directory for CoppeliaSim installation
RUN mkdir -p ${COPPELIASIM_DIR}

# Download CoppeliaSim
ADD ${COPPELIASIM_URL} ${COPPELIASIM_DIR}/coppelia.tar.xz

# Extract CoppeliaSim to the installation directory
RUN tar -xf ${COPPELIASIM_DIR}/coppelia.tar.xz -C ${COPPELIASIM_DIR} --strip-components=1 && \
    rm ${COPPELIASIM_DIR}/coppelia.tar.xz

# Change ownership to the non-root user
RUN chown -R ${USER_NAME}:${USER_NAME} ${COPPELIASIM_DIR}

# Set working directory
WORKDIR /opt/${USER_NAME}

# Switch to the non-root user
USER ${USER_NAME}

# Expose the default remote API port (optional)
EXPOSE 19997

# Expose the default visualization stream port
EXPOSE 23000

# Command to start CoppeliaSim in headless mode
CMD ["./coppeliaSim.sh", "-h"]
