FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install ffmpeg -y

COPY . .

ENV DISCORD_TOKEN REPLACE_THIS_TOKEN

CMD [ "python", "./bot.py"]
