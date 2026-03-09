# BASE-IMAGE

FROM python:3.12-slim


RUN apt-get update && rm -rf /var/lib/apt/lists/*

# CREATE A WORKING DIRECTORY

WORKDIR /app

# COPY THE CODE FROM REMOTE TO LOCAL

COPY . . 

# INSTALLING THE PACKAGES & DEPENDENCIES

RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE

EXPOSE 5000

# SERVE THE APPLICATION

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
