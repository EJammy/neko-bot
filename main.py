import discord
import os

tmp_channels: set[discord.VoiceChannel] = set()

def get_log_channel(guild: discord.Guild):
    all_channel = [x for x in guild.channels if isinstance(x, discord.TextChannel)]
    log_channel = all_channel[0]
    for i in all_channel:
        if 'bot' in i.name:
            log_channel = i
            break
    return log_channel

class Bot(discord.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user}!')

        for guild in self.guilds:
            await get_log_channel(guild).send('I am online!')
            print(guild.name)

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        # perms = member.guild.self_role.permissions
        c = after.channel
        if c and "new" in c.name.lower():
            try:
                channel = await c.guild.create_voice_channel(
                        f"{member.name}'s channel",
                        overwrites=c.overwrites,
                        category=c.category, position=1)
                tmp_channels.add(channel)
                await member.move_to(channel)
            except discord.errors.Forbidden:
                print('forbidden')
                await get_log_channel(c.guild).send('forbidden')

        for c in tmp_channels:
            if len(c.members) == 0:
                tmp_channels.remove(c)
                await c.delete()
                break


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

