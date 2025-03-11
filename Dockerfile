#Pull base image
FROM python:3.11-slim

#Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

#Install diffrent Linux Packages
RUN apt-get update && apt-get -y install gcc postgresql postgresql-contrib libpq-dev python3-dev netcat-traditional && apt-get clean 


#Set working directory
WORKDIR /app

#Copy requirements first for better caching
COPY ./requirements.txt ./requirements.txt

#Install dependencies
RUN pip install -r requirements.txt

#Copy project
COPY . /app/

COPY ./entrypoint.sh /app/entrypoint.sh

# give execution permission to the entrypoint script
# RUN chmod +x /app/entrypoint.sh

# #Run entrypoint.sh
# ENTRYPOINT ["/app/entrypoint.sh"]