## IRC chatbot

#### This software is an automated chatbot to be used with web chatrooms. Users are able to specify a server, port, password, and desired room to connect to the bot to. This chatbot reads chatroom user messages and processes them, producing a desired output.   

![alt text](https://i.imgur.com/QPeU0sT.png)


## Open for hacktober contributions!
#### - Create modules and add them to actuators, or just make the bot more robust!  
#### - Find the contribution guidelines [here](CONTRIBUTING.md)  
  

## Instructions

#### 1. Clone the repository to your local machine

#### 2. Optional: configure default_config.json to a server other than default settings

#### 2. Build Docker image: 

```shell
docker build -t chatbot .
```
#### 3. Run chatbot:

```shell
docker run --rm -it chatbot
```

## Commands

#### - Chatbot registers commands as phrases prefixed with exclamation points (e.g., !help)
#### - Some commands require an argument following the initial phrase! (e.g., !roll 5d50)
* #### **!urban rat** -Searches and returns urban dictionary for provided word
* #### **!wiki humans** - Searches and returns urban dictionary for provided word/phrase
* #### **!roll 5d50** - Provides randomized rolls of a 5 sided dice 50 times
* #### **!flip** - Provides randomized head or tails
* #### **!joke** - Provides a random joke
* #### **!chuck** - Provides a random Chuck Norris joke
* #### **!quote** - Provides a random quote
* #### **!horoscope libra** - Provides your daily horoscope
* #### **!cat** - Displays a super cute cat pic
* #### **!dog** - Displays a super cute dog pic
* #### **!jesus** - Provides a special message from jesus
* #### **!catfact** - Provides a random cat fact
* #### **!draw** - Provides a card randomly drawn from a deck
* #### **!help** - Displays available commands



