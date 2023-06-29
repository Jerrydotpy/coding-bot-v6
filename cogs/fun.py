from __future__ import annotations

import random
from io import BytesIO
from typing import TYPE_CHECKING, Optional

import base64
import discord
from discord.ext import commands
from ext.helpers import create_trash_meme
from ext.http import Http

import asyncio

if TYPE_CHECKING:
    from ext.models import CodingBot


class Fun(commands.Cog, command_attrs=dict(hidden=False)):
    hidden = False

    def __init__(self, bot: CodingBot) -> None:
        self.http = Http(bot.session)
        self.bot = bot

    @commands.command(name="trash")
    async def trash(self, ctx: commands.Context[CodingBot], *, user: discord.Member):
        """
        Throw someone in the trash
        Usage:
        ------
        `{prefix}trash <user>`

        """
        resp1 = await ctx.author.display_avatar.read()
        resp2 = await user.display_avatar.read()

        avatar_one = BytesIO(resp1)
        avatar_two = BytesIO(resp2)
        file = await create_trash_meme(avatar_one, avatar_two)
        await self.bot.send(ctx, file=file)

    @commands.hybrid_command()
    async def number(
        self, ctx: commands.Context[CodingBot], number: Optional[int] = None
    ) -> None:
        """
        Gets a random number.
        Usage:
        ------
        `{prefix}number`: *will get a random number*
        `{prefix}number [number]`: *will get the [number]*
        """
        if number is None:
            number = random.randint(1, 100)
        await self.bot.reply(ctx, f"{number}")
        number = await (
            self.http.api["numbers"]["random"]()
            if (number is None)
            else self.http.api["numbers"]["number"](number)
        )
        embed = self.bot.embed(
            title=f"**{number}**",
            description=" ",
            url="https://www.youtube.com/watch?v=o-YBDTqX_ZU",
        )
        return await self.bot.reply(ctx, embed=embed)

    @commands.hybrid_command(name="meme")
    async def meme(self, ctx: commands.Context[CodingBot]):
        meme_json = await self.http.api["get"]["meme"]()

        meme_url = meme_json["url"]
        meme_name = meme_json["title"]
        meme_poster = meme_json["author"]
        meme_sub = meme_json["subreddit"]

        embed = discord.Embed(
            title=meme_name,
            description=f"Meme by {meme_poster} from subreddit {meme_sub}",
            color=discord.Color.random(),
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        embed.set_image(url=meme_url)

        await self.bot.reply(ctx, embed=embed)

    @commands.hybrid_command(name="joke")
    async def joke(self, ctx: commands.Context[CodingBot]):
        """
        Tells a programming joke

        Usage:
        ------
        `{prefix}joke`: *will get a random joke*
        """
        joke_json = await self.http.api["joke"]["api"]()
        setup = joke_json[0]["question"]
        delivery = joke_json[0]["punchline"]

        embed = self.bot.embed(
            title=setup,
            description=f"||{delivery}||",
        )
        await self.bot.reply(ctx, embed=embed)

    @commands.hybrid_command(name="8ball")
    async def eightball(self, ctx: commands.Context[CodingBot], *, question: str):
        responses = [
            "As I see it, yes.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Do not count on it.",
            "It is certain.",
            "It is decidedly so.",
            "Most likely.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Outlook good.",
            "Reply hazy, try again.",
            "Signs point to yes.",
            "Very doubtful.",
            "Without a doubt.",
            "Yes.",
            "Yes, definitely.",
            "You may rely on it.",
        ]
        response = random.choice(responses)

        embed = discord.Embed(
            title="8ball is answering",
            description=f"{question}\nAnswer : {response}",
            color=discord.Color.random(),
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
        )  # Support for nitro users
        await self.bot.reply(ctx, embed=embed)

    @commands.hybrid_command(name="token")
    async def token(self, ctx: commands.Context[CodingBot]):
        first_string = ctx.author.id
        middle_string = random.randint(0, 100)
        last_string = random.randint(1000000000, 9999999999)

        token_part1 = base64.b64encode(f"{first_string}".encode("utf-8")).decode(
            "utf-8"
        )
        token_part2 = base64.b64encode(f"{middle_string}".encode("utf-8")).decode(
            "utf-8"
        )
        token_part3 = base64.b64encode(f"{last_string}".encode("utf-8")).decode("utf-8")

        final_token = f"{token_part1}.{token_part2}.{token_part3}"

        embed = discord.Embed(
            title="Ha ha ha, I grabbed your token.",
            description=final_token,
            color=discord.Color.random(),
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        await self.bot.reply(ctx, embed=embed)

    @commands.hybrid_group(invoke_without_command=True)
    async def binary(self, ctx: commands.Context[CodingBot]):
        embed = discord.Embed(
            title="Binary command",
            description="Available methods: `encode`, `decode`",
            color=discord.Color.random(),
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        await self.bot.reply(ctx, embed=embed)

    @binary.command(name="encode")
    async def binary_encode(self, ctx: commands.Context[CodingBot], *, string: str):
        binary_string = " ".join((map(lambda x: f"{ord(x):08b}", string)))

        embed = discord.Embed(
            title="Encoded to binary",
            description=binary_string,
            color=discord.Color.random(),
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
        )

        await self.bot.reply(ctx, embed=embed)

    @binary.command(name="decode")
    async def binary_decode(self, ctx: commands.Context[CodingBot], *, binary: str):
        if (len(binary) - binary.count(" ")) % 8 != 0:
            return await self.bot.reply(ctx, "The binary is an invalid length.")
        binary = binary.replace(" ", "")
        string = "".join(
            chr(int(binary[i : i + 8], 2)) for i in range(0, len(binary), 8)
        )
        embed = discord.Embed(
            title="Decoded from binary",
            description=string,
            color=discord.Color.random(),
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
        )

        await self.bot.reply(ctx, embed=embed)

    @commands.hybrid_command(name="reverse")
    async def reverse(self, ctx: commands.Context[CodingBot], *, text: str):
        embed = discord.Embed(
            title="Reversed Text",
            description=f"{text[::-1]}",
            color=discord.Color.random(),
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="owofy")
    async def owofy(self, ctx: commands.Context[CodingBot], *, text: str):
        embed = discord.Embed(
            title="Owofied Text",
            description=text.replace("o", "OwO"),
            color=discord.Color.random(),
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        await self.bot.reply(ctx, embed=embed)

    @commands.hybrid_command(name="mock")
    async def mock(self, ctx: commands.Context[CodingBot], *, text: str):
        embed = discord.Embed(
            title="Mocked Text",
            description=text.swapcase(),
            color=discord.Color.random(),
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        await self.bot.reply(ctx, embed=embed)

    @commands.hybrid_command(name="beerparty")
    async def _beerparty(
        self, ctx: commands.Context, *, reason: commands.clean_content = None
    ):
        reason = ("\nReason: " + reason) if reason else ""
        msg = await ctx.send(
            f"Open invite to beerparty! React with 🍻 to join!{reason}"
        )
        await msg.add_reaction("\U0001f37b")
        await asyncio.sleep(60)
        msg = await ctx.channel.fetch_message(msg.id)
        users = [user async for user in msg.reactions[0].users()]
        users.remove(self.bot.user)
        if not users:
            return await ctx.send("Nobody joined the beerparty :(")
        await ctx.send(
            ", ".join(user.display_name for user in users) + " joined the beerparty!"
        )

async def setup(bot: CodingBot):
    await bot.add_cog(Fun(bot))
