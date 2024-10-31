# Use the official Python Alpine image as a base
FROM python:alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY src/requirments.txt .

# Install dependencies
RUN pip install -r requirments.txt

RUN pip install gunicorn
# Copy the application code
COPY src/* .

# Expose the port for Gunicorn
EXPOSE 8000

# Run migrations and then start Gunicorn
# CMD ["sh", "-c", "python manage.py migrate && gunicorn --workers=3 --bind=0.0.0.0:8000 core.wsgi:application"]
ENTRYPOINT [ "docker-entrypoint.sh" ]