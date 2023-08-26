import discord
import os

tmp_channels: set[discord.VoiceChannel] = set()

class Bot(discord.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user}!')

        for guild in self.guilds:
            await [x for x in guild.channels if isinstance(x, discord.TextChannel)][0].send('I am online!')
            print(guild.name)

    async def on_message(self, msg: discord.Message):
        print(f'{msg.author}: {msg.content}!')
        if msg.author.id != self.user.id:
            await msg.channel.send(f'{msg.author} {self.user}')

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        # perms = member.guild.self_role.permissions
        c = after.channel
        if c and "new" in c.name.lower():
            try:
                channel = await c.guild.create_voice_channel(f"{member.name}'s channel", category=c.category)
                tmp_channels.add(channel)
                await member.move_to(channel)
            except discord.errors.Forbidden:
                print('forbidden')

        for c in tmp_channels:
            if len(c.members) == 0:
                tmp_channels.remove(c)
                await c.delete()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = Bot(intents=intents)

@bot.slash_command(name='foo')
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond(f"Hello {ctx.author.display_name}!")
    print(ctx.guild.name)
    for user in ctx.guild.members:
        try:
            await user.edit(nick='FOO')
        except discord.errors.Forbidden:
            print(f'No permission to edit nickname of {user}')

if "DISCORD_TOKEN" in os.environ:
    token = os.environ['DISCORD_TOKEN']
else:
    f = open("token.txt", 'r')
    token = f.readline()

bot.run(token)

