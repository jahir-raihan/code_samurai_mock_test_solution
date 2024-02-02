# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 5000 for the Django development server
EXPOSE 5000

# Run database migrations and start the Django development server
CMD ["bash", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:5000"]
