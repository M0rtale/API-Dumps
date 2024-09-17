FROM python:3.12-slim-bookworm


RUN apt-get update

RUN useradd -ms /bin/sh app
WORKDIR /home/app

COPY . .

RUN python3 -m pip install --no-cache-dir -r requirements.txt && \ 
    chown -R root:app /home/app && \
    chmod 750 /home/app && \
    chmod 550 /home/app/*

EXPOSE 9996

CMD ["gunicorn", "--log-level", "info", "--workers", "8", "-b", "0.0.0.0:9996", "app:app"]	



