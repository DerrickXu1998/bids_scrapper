FROM python:3.14
WORKDIR /usr/local/scaper/python-boilerplate

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

ENV PYTHON /usr/local/bin/python3.14
ENV UV_CACHE_DIR=/tmp/uv-cache

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]