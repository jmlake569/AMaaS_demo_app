# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy only the necessary directories and files
COPY templates /app/templates
COPY . /app

# Create the necessary directories
RUN mkdir -p /app/uploads /app/logs

# Install required packages
RUN pip install --no-cache-dir flask==3.0.2 visionone-filesecurity requests

#set the environment variables region value should be one of ['ap-southeast-2', 'eu-central-1', 'ap-south-1', 'ap-northeast-1', 'ap-southeast-1', 'us-east-1']
ENV API_KEY="YOUR_API_KEY"
ENV REGION="us-east-1" 

# Expose port 5000
EXPOSE 5000

# Run the application as a non-root user for security reasons
RUN useradd -m myuser
# Change ownership of the entire app directory
RUN chown -R myuser:myuser /app

USER myuser

# Run the Flask application
CMD ["python", "app.py"]