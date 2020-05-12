# Base Image
FROM python:3.7-slim

# set proxy
ENV http_proxy http://wwwproxy.unimelb.edu.au:8000
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000
ENV HTTP_PROXY http://wwwproxy.unimelb.edu.au:8000/
ENV HTTPS_PROXY http://wwwproxy.unimelb.edu.au:8000/
ENV no_proxy localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.u nimelb.edu.au,.cloud.unimelb.edu.au

# create and set working directory
# Add current directory code to working directory
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]