FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY wordlist.txt ./
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ffmpeg -y


COPY . .

ENV DISCORD_TOKEN ODU4Mzg4OTY3NzgzMTM3Mjkx.YNdbBg.xcOqUCvAnQ1SuKd5BoQLI41A6ik

CMD [ "python", "./bot.py"]
