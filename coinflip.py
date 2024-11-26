import discord
import random
import json
import os
from discord.ext import commands

DATABASE_FILE = "coins.json"

# Load and save coin data
def load_coin_data():
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    return {}

def save_coin_data():
    with open(DATABASE_FILE, 'w') as file:
        json.dump(coin_totals, file, indent=4)

# Coin management functions
coin_totals = load_coin_data()

def add_coins(user_id, amount):
    user_id = str(user_id)
    if user_id in coin_totals:
        coin_totals[user_id] += amount
    else:
        coin_totals[user_id] = amount
    save_coin_data()

def remove_coins(user_id, amount):
    user_id = str(user_id)
    if user_id in coin_totals:
        coin_totals[user_id] -= amount
        if coin_totals[user_id] < 0:
            coin_totals[user_id] = 0
    save_coin_data()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

coinflip_games = []

# Coinflip game class
class CoinflipGame:
    def __init__(self, creator, amount):
        self.creator = creator
        self.amount = amount
        self.opponent = None

    async def flip(self, interaction):
        winner = random.choice([self.creator, self.opponent])
        loser = self.creator if winner == self.opponent else self.opponent

        add_coins(str(winner.id), self.amount)
        remove_coins(str(loser.id), self.amount)

        await interaction.response.send_message(
            f"{winner.mention} won the coinflip and took {self.amount} coins from {loser.mention}!"
        )

# Coinflip command
@bot.tree.command(name="coinflip", description="Start a coinflip or view available games.")
async def coinflip(interaction: discord.Interaction, amount: int = None):
    user_id = str(interaction.user.id)

    if amount:
        if coin_totals.get(user_id, 0) >= amount:
            remove_coins(user_id, amount)
            game = CoinflipGame(interaction.user, amount)
            coinflip_games.append(game)

            await interaction.response.send_message(f"{interaction.user.mention} created a coinflip for {amount} coins! Use /coinflip to join.")
        else:
            await interaction.response.send_message("You don't have enough coins!", ephemeral=True)
    else:
        if not coinflip_games:
            await interaction.response.send_message("No coinflip games available.", ephemeral=True)
            return

        options = [discord.SelectOption(label=f"{game.creator.name}'s coinflip for {game.amount} coins", value=str(i)) for i, game in enumerate(coinflip_games)]

        class CoinflipSelect(discord.ui.Select):
            def __init__(self):
                super().__init__(placeholder="Choose a coinflip", min_values=1, max_values=1, options=options)

            async def callback(self, interaction: discord.Interaction):
                game_index = int(self.values[0])
                if game_index < len(coinflip_games):
                    game = coinflip_games.pop(game_index)
                    game.opponent = interaction.user
                    await game.flip(interaction)
                else:
                    await interaction.response.send_message("This coinflip is no longer available.", ephemeral=True)

        view = discord.ui.View()
        view.add_item(CoinflipSelect())
        await interaction.response.send_message("Choose a coinflip game to join:", view=view)

# Run the bot
@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')
    await bot.tree.sync()

bot.run('token')
