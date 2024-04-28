FROM python:3.11-slim-buster
RUN apt-get update && apt-get install

RUN apt-get install -y \
    dos2unix \
    libpq-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc \
    && apt-get clean

WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000" ]