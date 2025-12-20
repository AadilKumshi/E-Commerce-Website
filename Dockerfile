# 1. Start with a lightweight Linux installation that has Python 3.10
FROM python:3.10-slim

# 2. Create a folder inside the container to hold your app
WORKDIR /app

# 3. Copy your requirements file into the container
COPY requirements.txt .

# 4. Install all the libraries inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your project code into the container
COPY . .

# 6. Open port 8000 so the world can talk to your API
EXPOSE 8000

# 7. The command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]