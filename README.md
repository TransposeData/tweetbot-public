# Tweetbot

A system for spinning up tweetbots that tweet when things happen on the blockchain.

Read the full blog post for step-by-step setup instructions: 

## Setting up a new bot
You will need a fresh twitter account to use for the bot. This must unfortunately be created and authenticated manually.

1. Set up a fresh free email at proton.me
2. Create a new twitter account with this email: https://twitter.com/signup
3. Get dev access here: https://developer.twitter.com/en/portal/petition/essential/basic-info
4. Note down your api key, secret key and bearer token in a file in `./credentials/[BOT NAME]_credentials.json` (see existing examples)

## Connecting to EC2
`ssh -i [pemfile] ubuntu@ec2-3-80-148-125.compute-1.amazonaws.com`
