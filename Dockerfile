FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY wordlist.txt ./
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ffmpeg -y


COPY . .

ENV DISCORD_TOKEN 

CMD [ "python", "./bot.py"]
