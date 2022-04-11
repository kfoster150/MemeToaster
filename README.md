# MemeToaster

Add MemeToaster to your server by following this link:
https://discord.com/api/oauth2/authorize?client_id=920060661294309378&permissions=52224&scope=bot%20applications.commands

This is a Discord bot you can use to spice up your conversations with captioned pictures, aka 'memes'. Enter in a picture category and a caption, and MemeToaster will randomly choose a picture from the category you supplied and caption it with the message you type.

# Commands
## meme
Type this: `toast.meme -laugh this bot is hilarious`

And get back something like this:

![toast.meme -laugh this bot is hilarious](https://user-images.githubusercontent.com/38412483/162673295-cb33065b-4a44-4f1d-baa1-e2663cc9a7ee.png)

### Prefix Command
Syntax:
toast.meme -tag caption

Example:
toast.meme -sleep I'm exhausted and I need a nap

![toast.meme -sleep I'm exhausted and I need a nap](https://raw.githubusercontent.com/kfoster150/MemeToaster/master/data/images/README/sleep.png)

### Slash Command
Example:
**/meme** `tag`: wat `caption`: these pretzels are making me thirsty
![these pretzels are making me thirsty](https://user-images.githubusercontent.com/38412483/162673762-856eb151-ee4e-46dc-9df4-40b5bb8c11b4.png)

![these pretzels are making me thirsty](https://user-images.githubusercontent.com/38412483/162673884-e3db9dba-0ea3-4414-9316-f488f98f13b0.png)

## tags
Type this: `toast.tags`

And get back a link to a list of currently available tags

![image](https://user-images.githubusercontent.com/38412483/162674001-5585fab8-30c1-4b8c-898e-717a7342b961.png)

You can check out this list itself here: https://memetoaster.s3.us-west-1.amazonaws.com/tags.txt

This is also available as a slash command: **/tags**

## help
Type this: `toast.help`

And receive a quick review on how to use MemeToaster, including a link to this README.

![image](https://user-images.githubusercontent.com/38412483/162674057-7e30c461-c0ae-494a-9bb0-56857ebafe0b.png)

# Permissions
The following permissions are necessary for MemeToaster to work as intended:
- View Channels
- Send Messages
- Embed Links
- Attach Files

# About
This bot was developed using Python, relying on the hikari and lightbulb libraries to communicate with Discord. Image data management is done in PostGreSQL. Images hosted on Amazon Web Services S3. Bot is hosted on Heroku.
