# Base Image
FROM python:3

# create and set working directory
# Add current directory code to working directory
COPY . /app
WORKDIR /app


# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

RUN pip install -r requirements.txt

EXPOSE 8888
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8888"]