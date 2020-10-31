## IRC chatbot

#### This software is an automated IRC chatbot to be used with web chatrooms. Users are able to specify a server, port, password, and desired room to connect the bot to. This chatbot reads chatroom messages and processes them, producing a desired output in the chatroom.   

![alt text](https://i.imgur.com/dAwS00J.png)


## Open for hacktober contributions!       ![alt text](https://img.shields.io/github/contributors-anon/svimanet/chatbot)


#### - Create modules and add them to actuators, or just make the bot more robust!
#### - Find the contribution guidelines [here](docs/CONTRIBUTING.md)  
  

## Instructions

#### 1. Clone/copy this repository to your local machine

#### 2. Navigate inside of the newly downloaded directory

#### 3. Optional: configure config.json to settings other than default

#### 4. Build Docker image: 

```shell
docker build -t chatbot .
```
#### 5. Run chatbot:

```shell
docker run --rm -it chatbot
```

## Commands

#### - Chatbot reads commands as phrases prefixed with exclamation points (e.g., !help)
#### - Some commands require an argument following the initial phrase (e.g., !roll 5d50)
* #### **!help** - Returns available commands
* #### **!urban word** - Searches and returns urban dictionary description of a specified term
* #### **!wiki word/phrase** - Searches and returns wikipedia description of a specified term
* #### **!roll 5d50** - Returns randomized rolls of a 5 sided dice 50 times. Any format of 'XdY' works
* #### **!flip** - Flips a coin and returns heads, tails, or ... edge?
* #### **!joke** - Returns a random joke
* #### **!chuck** - Returns a random Chuck Norris joke
* #### **!quote** - Returns the Quote of the Day. Only changes once per day
* #### **!horoscope libra** - Returns a daily horoscope corresponding to the provided zodiac sign
* #### **!cat** - Returns a link to a super cute cat pic
* #### **!dog** - Returns a link to a super cute dog pic
* #### **!jesus** - Returns a special message from our lord and saviour, Jesus Christ
* #### **!catfact** - Returns a random cat fact
* #### **!draw** - Returns a card randomly drawn from a deck
* #### **!covidglobal** - Returns current covid-19 statistics globally
* #### **!covidcountry Germany** - Returns covid-19 statistics for the specified country
* #### **!sentiment word/phrase** - Returns the sentiment value of a specified sentence, based on an API
* #### **!today** - Retrieves all holidays for today and returns one at random
* #### **!todayall** - Returns all holidays for today
* #### **!weekno** - Returns the current week number as well as the from and to date for the current week

## License
#### [The Unlicense](LICENSE)
