FROM python:3.11-slim

# install ffmpeg and git
RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

WORKDIR /app

# dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# application code
COPY . .

# environment variables
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
