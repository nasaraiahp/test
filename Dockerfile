# Use the official Python 3.12.5 image
FROM python:3.12.5

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
