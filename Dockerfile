# Use an official Python image
FROM python3.10-slim

# Install FFmpeg
RUN apt install ffmpeg_7.1-3ubuntu1_amd64.deb

# Set the working directory
WORKDIR app

# Copy files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD [python, app.py]
