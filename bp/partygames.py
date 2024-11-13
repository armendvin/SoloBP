
import discord
from redbot.core import commands
from redbot.core import Config
from redbot.core.data_manager import bundled_data_path
from redbot.core import checks
from redbot.core.i18n import Translator, cog_i18n, get_locale
import random
import asyncio
import json

CHARS = {
    'en-US': [
        'WEA', 'BRE', 'IST', 'CRA', 'STA',
        'SPL', 'REF', 'MIL', 'FOR', 'GAG',
        'TIC', 'ILL', 'RAF', 'BLA', 'JET',
        'CLA', 'CON', 'SIN', 'INK', 'SAT',
        'MIN', 'SCH', 'BER', 'ISE', 'IDE',
        'LAT', 'IMI', 'ZAP', 'ENT', 'WHI',
        'TRI', 'OVE', 'SAV', 'HAN', 'PUR',
        'LIN', 'LOG', 'CAT', 'INS', 'STI',
        'RIS', 'COM', 'INC', 'ELL', 'MEN',
        'TIN', 'SOF', 'KIL', 'BRO', 'ADJ',
        'PRO', 'BET', 'SHI', 'ORI', 'HUN',
        'LOW', 'LUB', 'ANG', 'SCA', 'RED',
        'DEP', 'PER', 'INT', 'ROA', 'RES',
        'TRA', 'WOR', 'SYR', 'MAT', 'MIS',
        'DIS', 'STR', 'COK', 'GRA', 'INE',
        'UNP', 'ATT', 'DIG', 'IOD', 'CAL',
        'LOV', 'ATE', 'LAG', 'INO', 'CRO',
        'PAL', 'PAT', 'ICA', 'ABS', 'DRA',
        'RAN', 'LIT', 'RAT', 'TRO', 'FLA',
        'REV', 'VER'
    ],
}

_ = Translator('PartyGames', __file__)

class PartyGames(commands.Cog):
    """Chat games focused on solo word guessing from 3 letters."""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=145519400223506432)
        self.config.register_guild(locale=None)
        self.words = self._load_words()

    def _load_words(self):
        """Loads words from the JSON file."""
        with open(bundled_data_path(self) / 'en-US.json') as f:
            words = json.load(f)
        return set(words)

    @commands.command(name="solopractice")
    async def solo_practice(self, ctx: commands.Context):
        """Start a solo practice mode where the user guesses words containing a random 3-letter sequence."""
        
        await ctx.send("Starting solo practice mode. Guess words that contain the given 3-letter sequence. Type 'quit' to exit.")

        prompts = CHARS.get("en-US", [])
        score = 0

        while True:
            prompt = random.choice(prompts)
            await ctx.send(f"Your prompt is: **{prompt}**. Type a word containing this sequence or 'quit' to exit.")

            try:
                response = await self.bot.wait_for(
                    "message",
                    timeout=60.0,
                    check=lambda message: message.author == ctx.author and message.channel == ctx.channel
                )
            except asyncio.TimeoutError:
                await ctx.send("Time's up! You took too long to respond. Exiting solo practice mode.")
                break

            if response.content.lower() == "quit":
                await ctx.send(f"Exiting solo practice mode. Your final score is: {score}. Thanks for playing!")
                break

            guess = response.content.lower()
            if prompt.lower() in guess and guess in self.words:
                score += 1
                await ctx.send(f"Good job! '{guess}' is a valid word containing {prompt}. Your current score is: {score}.")
            else:
                await ctx.send(f"'{guess}' is either invalid or doesn't contain {prompt}. Try again or type 'quit' to exit.")
