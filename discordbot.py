import os
import logging
from dotenv import load_dotenv
from chatbot import flow

import discord
from discord.ext import commands
from discord import app_commands

load_dotenv()
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="", intents=intents)

# Bot events:
@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} in guilds:\n')
    for guild in bot.guilds:
        logging.info(guild.name)
    await bot.tree.sync()
    logging.info("Slash commands synced.")


@bot.tree.command(name="bot", description="Have the bot respond to your message with an OpenAPI response")
@app_commands.describe(message="The message from OpenAPI.")
async def bot_command(interaction: discord.Interaction, message: str):
    response, bot.conversation_summary = flow(message, bot.conversation_summary)
    await interaction.response.send_message(response)


# Example usage
if __name__ == "__main__":
    bot.conversation_summary = ""
    bot.run(os.getenv("DISCORD_TOKEN"))
