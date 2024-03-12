#use the official Python image as the base image
FROM python:3.9

#set the working directory
WORKDIR /app

#copy the application files into the container
COPY . /app

#create the uploads directory
RUN mkdir -p /app/uploads

#copy the templates directory into the container
COPY templates /app/templates

#install required packages
RUN pip install --no-cache-dir flask==3.0.2
RUN pip install visionone-filesecurity
RUN pip install requests

#set the environment variables (only availabe in us-1 region right now will leave as default) please just add your api key
ENV C1_ADDRESS="antimalware.us-1.cloudone.trendmicro.com:443"
ENV API_KEY="YOUR V1 API KEY here"
ENV C1_REGION="us-1"

#expose port 5000
EXPOSE 5000

#run the Flask application
CMD ["python", "app.py"]