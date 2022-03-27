# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Copy over pip requirements
ADD requirements.txt .

# Install some prerequsites for psycopg2 build then install our pip requirements and clean up
# NOTE: I'm important to do this all in one command because of the way docker handles the filesystem
# See https://blog.replicated.com/refactoring-a-dockerfile-for-image-size/
# Putting this all in one command netted a significant savings for the container size.
#   Before: 547 MB (384 MB over base image)
#   After:  197 MB (32 MB over base image)
RUN apt-get update && \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt && \
    apt-get --assume-yes autoremove && \
    rm -rf /var/lib/apt/lists/*

# Switch to correct folder instead of
WORKDIR /app
ADD . /app

# Copy bot to correct place
COPY ./bot /app/

# Create non-root application user
RUN useradd appuser && chown -R appuser /app

# Switching to a non-root user
USER appuser



# During debugging, this entry point will be overridden
CMD ["python", "/app/main.py"]
