FROM python:3.8

COPY . /app
WORKDIR /app
# Install dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get install -y \
        gcc \
        build-essential \
        zlib1g-dev \
        wget \
        unzip \
        cmake \
        python3-dev \
        gfortran \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        libsndfile1-dev \
        ffmpeg \
    && apt-get clean

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

VOLUME /app/static
EXPOSE 5612

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5612"]