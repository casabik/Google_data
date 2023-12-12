FROM python:3.7

CMD pip install -y googla-ads
COPY credentials.json credentials.json

CMD ["python3", "main.py"]