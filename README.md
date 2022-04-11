# MemeToaster

Add MemeToaster to your server by following this link:
https://discord.com/api/oauth2/authorize?client_id=920060661294309378&permissions=52224&scope=bot%20applications.commands

This is a Discord bot you can use to spice up your conversations with captioned pictures, aka 'memes'. Enter in a picture category and a caption, and MemeToaster will randomly choose a picture from the category you supplied and caption it with the message you type.

# Commands
## meme
Type this: `toast.meme -laugh this bot is hilarious`

And get back something like this:

![is it working][data/images/README/laugh.png]

### Pref][ix Command
Syntax:
toast.meme -tag caption

Example:
toast.meme -sleep I'm exhausted and I need a nap

🖼️

### Slash Command
Example:
**/meme** `tag`: wat `caption`: these pretzels are making me thirsty (use screenshot)

🖼️


## tags
Type this: `toast.tags`

And get back a link to a list of currently available tags

(screenshot)

You can check out this list itself here: https://memetoaster.s3.us-west-1.amazonaws.com/tags.txt

This is also available as a slash command: **/tags**

## help
Type this: `toast.help`

And receive a quick review on how to use MemeToaster, including a link to this README.


# Permissions
The following permissions are necessary for MemeToaster to work as intended:
- View Channels
- Send Messages
- Embed Links
- Attach Files

# About
This bot was developed using Python, relying on the hikari and lightbulb libraries to communicate with Discord. Image data management is done in PostGreSQL. Images hosted on Amazon Web Services S3. Bot is hosted on Heroku.
