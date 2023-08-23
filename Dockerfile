FROM python:3.10
RUN apt-get update && apt-get install -y locales locales-all && \
    locale-gen ru_RU.utf-8 && \
    update-locale LANG=ru_RU.utf-8
ENV LC_ALL ru_RU.utf-8
ENV LANG ru_RU.utf-8

WORKDIR /app



COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]