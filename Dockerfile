FROM python:3.10
WORKDIR /app
RUN apt update && apt install -y locales && locale-gen ru_RU && update-locale
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]