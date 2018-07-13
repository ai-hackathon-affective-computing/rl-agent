# Read Me

http://ec2-54-194-217-192.eu-west-1.compute.amazonaws.com/observe?gender=0&age=25&music_on=1&has_sunglasses=0


## Deploy Server

docker build -t rl-agent .

docker run -d --restart=always -p 80:80 rl-agent
