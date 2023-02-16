# HOW TO QUICKLY BUILD YOUR OWN TELEGRAM CHAT BOT WITH OPENAI

## features
1. chat
2. generate weekly report


## 1. apply for telegram bot api key

## 2. apply for openai api key

## 3. install python

## 4. pip install python-telegram-bot,requests,pyinstaller

## 5. modify the code
1. replace the "TELEGRAM_BOT_TOKEN","CHAT_API_KEY"  with yours

OR 

2. export TELEGRAM_BOT_TOKEN,CHAT_API_KEY to OS environment variables

## 6. package to executable file
check if the pyinstaller is installed, if not, install it first
```
pip install pyinstaller
```
then run the package script
```
sh package.sh
```
the executable file will be generated in the dist folder

## 7. deplop and run
upload the dist binary file (for example,telegramOpenAIChatbot) to your server, and run the bot
with the following script
```
sh deploy.sh
```