# Library Telegram Bot
This is a personal project on deploying a Telegram Bot to invoke the SMU Library URL and obtain the occupancy level in both libraries: Li Ka Shing Library and Kwa Geok Choo Law Library


# Steps to run locally
1. Replace the `TOKEN` for the Telegram Bot with your own
Refer to <a href="https://telegra.ph/Awesome-Telegram-Bot-11-11">this guide</a> to obtain a token of your own 

2. Build the docker image
```
docker build -t <dockerid>/library_telebot:1.0 ./
```

3. Run the docker image
```
docker run -p 5000:5000 <dockerid>/library_telebot:1.0
```
*this uses port 5000, feel free to change the port accordingly*

4. Telegram bot is done!

# Deploying Telegram bot to Heroku
1. Ensure that you have Heroku CLI
Refer to <a href="https://devcenter.heroku.com/articles/heroku-cli">this guide</a>

2. Login to heroku
```
heroku login
```

3. Login to heroku container
```
heroku container:login
```

3. Create your application
```
heroku create <Heroku app name>
```

4. Push the application as a container to Heroku (using worker)
```
heroku container:push worker -a <Heroku app name>
heroku container:release worker -a <Heroku app name>
```

**You can also use `web` to push the application with Flask**