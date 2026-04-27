FROM python:3.14
WORKDIR /usr/local/scaper/python-boilerplate

# Create and use a virtual environment with Python 3.14
ENV VIRTUAL_ENV=/opt/venv
RUN python3.14 -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 8080
ENV PYTHONPATH=/usr/local/scaper/python-boilerplate/src

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

ENV UV_CACHE_DIR=/tmp/uv-cache

CMD ["python", "-m", "bids_scrapper"]