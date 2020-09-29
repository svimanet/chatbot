# IRC chatbot

### This software is an automated chatbot to be used with web chatrooms. Users are able to specify a server, port, password, and desired room to connect to the bot to. This chatbot reads chatroom user messages and processes them, producing a desired output.   

![alt text](https://i.imgur.com/QPeU0sT.png)


# Open for hacktober contributions!
### - Create modules and add them to actuators - or just make the bot more robust!  
### - Find the contribution guidelines [here](CONTRIBUTING.md)  
  

# Instructions

1. Clone the repository to your local machine

2. Optional: configure default_config.json to a server other than default settings

2. Build Docker image: 

```shell
docker build -t chatbot .
```

3. Run chatbot:

```shell
docker run --rm -it chatbot
```



