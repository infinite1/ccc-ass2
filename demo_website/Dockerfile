# Base Image
FROM python:3

# create and set working directory
# Add current directory code to working directory
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 70
CMD ["python3", "manage.py", "runserver", "0.0.0.0:70"]