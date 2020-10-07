You can contribute with whatever you feel like would make the project better.
For instance, you can update files, fix mistakes, improve modules or the overall bot, create new modules, etc ...
Remember to test your changes before submitting a PR! I see no point in merging things that won't work, or that will break the bot.

How to create new modules:
1. Create a new py file under modules/
2. Create a function in the file, which can take both 'message' and 'nick' as parameters. Parameters are optional.
3. The function should return a String which will be the message that the bot sends to the chat.
4. Add an example use of your new command and a description to the "examples" list found in commands.py, this is what updates the readme.  
5. Import the module in main.py
6. Create an actuator for your module in the Bot.actuators() method. Try to make it robust so that the module won't kill the bot.
7. Test it to see if it works correctly. Upon testing your command, your module will be added to the readme commands section through the "examples" list. Do not add it manually to the readme!
