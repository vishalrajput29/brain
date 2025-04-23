FROM python:3.9-slim-buster

# Set working directory inside container
WORKDIR /app

# Copy all files to container
COPY . /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the YOLOv8 model file from GitHub (⚠️ replace this link)
RUN curl -L -o best.pt https://github.com/vishalrajput29/brain/blob/main/best.pt
# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python3", "app.py"]
