# Read Me


## Run Server

With pipenv:
````
pipenv run python live_run.py
````


docker build -t rl-agent .

docker run -d --restart=always -p 80:80 rl-agent
