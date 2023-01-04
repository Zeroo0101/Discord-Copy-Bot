import discord
from colorama import Fore
from colorama import init as colorama_init
from discord.ext import commands

colorama_init()

members = []


class Console:
    _message: str

    def __init__(self, _message):
        self._message = _message

    def warn(self):
        print(f"{Fore.YELLOW}Warning: {Fore.RESET}" + self._message)

    def error(self):
        print(f"{Fore.RED}Error: {Fore.RESET}" + self._message)

    def info(self):
        print(f"{Fore.LIGHTGREEN_EX}Info: {Fore.RESET}" + self._message)


class MyDiscordEvents(commands.Cog):
    _client: commands.Bot

    def __init__(self, client):
        self._client = client
        client.add_listener(self.on_ready)
        client.add_listener(self.on_message)

    async def on_ready(self):
        await self._client.add_cog(MyDiscordCommands(self._client))
        print(f'{Fore.GREEN}Logged on as {self._client.user}!')

    async def on_message(self, message):
        sender = message.author
        if sender in members:
            await message.reply(message.content)
            Console(f"Copied Message: {message.content}, Author: {message.author}").info()


class MyDiscordCommands(commands.Cog):
    _client: commands.Bot

    def __init__(self, client: commands.Bot):
        self._client = client

    @commands.command(name="copy")
    async def copy_member(self, ctx, *, member: discord.Member):
        if ctx.author.id == self._client.user.id:
            return
        elif member.id == self._client.user.id:
            await ctx.send(f"You can't copy me! Ha he.")
            return
        elif member in members:
            members.remove(member)
            await ctx.send(f"Not copying member {member.name} anymore.")
            Console(f"User {member} got removed from the copy list.").warn()
        else:
            members.append(member)
            await ctx.send(f"Copying member {member.name}.")
            Console(f"User {member} got added to the copy list.").warn()

    @commands.command(name="effected")
    async def effected_members(self, ctx):
        if len(members) > 0:
            await ctx.send(f" ".join(str(p) for p in members))
        else:
            await ctx.send(f"Not anyone effected right now.")


def main():
    Console("Start Running").info()

    client = commands.Bot(intents=discord.Intents.all(), command_prefix="!")

    MyDiscordEvents(client)

    client.run('MTA1OTg5MzU2ODM4ODQ4MTAzNA.Gn3ZVv._ejnRhFCNQfAgL7AjdhN9La2Lvp1c4-Cvl4VVI')


if __name__ == '__main__':
    main()
