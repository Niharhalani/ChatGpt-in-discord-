import discord
import msg
import json
from discord import app_commands
from discord.ext import commands 

with open('config.json', 'r') as f:
    data = json.load(f)

# Send messages
async def send_message(message, user_message, is_private):
    try:
        response = msg.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

intents = discord.Intents.default()
intents.message_content = True

def AskME():
    TOKEN = data['discord_bot_token']
    # client = discord.Client(intents=intents)
    activity = discord.Activity(type=discord.ActivityType.watching, name="/chat | /private | /public | /reset")
    client = commands.Bot(command_prefix='!', intents=intents, activity=activity)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.tree.command(name="chat", description = "Have a chat with GPT")
    async def on_message(interaction: discord.Interaction, *, message: str):
        if interaction.user == client.user:
            return

        await interaction.response.defer(ephemeral=False)
        username = str(interaction.user)
        user_message = str(message)
        channel = str(interaction.channel)

        print(f"{username} said: '{user_message}' ({channel})")
        await interaction.followup.send(f"> **{username}** asked {user_message}")

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(interaction, user_message, is_private=False)
        else:
            await send_message(interaction, user_message, is_private=False)

    client.run(TOKEN)