<h1>✈️METARbot✈️</h1>

<h3>To invite this bot to your server to test out click here: <a href=https://discord.com/oauth2/authorize?client_id=929045807842361404&permissions=3072&scope=bot>LINK</a></h3>

This bot is hosted on a VPS inside a Docker container. The Dockerfile and requirements file are all included if you want to host your own version or run locally.

Clone this repo then outside the directory created, build the image using: 
```bash
docker build METARbot/ --tag metarbot
```

Then:
```bash
docker run -d metarbot
```
This should run the docker image in a detached state and in the background
