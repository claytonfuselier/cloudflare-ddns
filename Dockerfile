FROM python:3.11-slim

WORKDIR /app

COPY main.py .

RUN pip install requests pyyaml

CMD ["python", "main.py"]