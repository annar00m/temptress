#!/bin/python3
"""
by using API from personalityforge bot can talk like it does, for documentation visit https://www.personalityforge.com/chatbot-api-docs.php
"""
import discord
import requests
import database
from os import environ
from random import choice
from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botID = 106996 # NSFW Annabelle Lee = 106996, Laurel Sweet = 71367 Lil Neko = 148149 SFW Cyber Ty = 63906, prob = 23958, 157181
        self.key = environ['FORGE']
        self.base_chat_url = f"https://www.personalityforge.com/api/chat/?apiKey={self.key}&chatBotID={self.botID}&message="  # "{message}&externalID=<externalID>&firstName=<firstName>&lastName=<lastName>&gender=<gender>"

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.content.startswith('..'):
            return

        print('first part is fine')
        ban_data = database.is_botban(message.author.id)
        print('second part is fine')
        if ban_data is None:
            if set(database.get_config('chat', message.guild.id)) & set([role.id for role in message.author.roles]) or database.get_config('chat', message.guild.id) == [0]:
                print('third part is fine')
                ctx = await self.bot.get_context(message)

                async with ctx.typing():
                    if not message.channel.nsfw:
                        await ctx.reply(f'This channel is not NSFW, I only chat in NSFW channels to be safe.')
                        return
                    
                    print('(after typing)')

                    if set(database.get_config('domme', message.guild.id)) & set([role.id for role in message.author.roles]):
                        gender = 'f'
                    else:
                        gender = 'm'

                    print('fourth part is fine')
                    message = message.content[2:]
                    url = f"{self.base_chat_url}{message}&externalID={ctx.author.id}&gender={gender}"
                    data = requests.get(url).json()
                    print(data)
                    message_data = data['message']['message'].replace('<br>', '\n')
                    emotion = data['message']['emotion']
                    if emotion == 'happy-9':
                        # await ctx.message.add_reaction(emoji='simp:858985009905664040')
                        message_data = message_data + ' <:giggle:897777342791942225>'
                    print('fifth part is fine')
                    if 'cowboy!' in message_data:
                        NSFW_reply = ['*ignoring*', 'Go watch porn pervert.', 'I am not a Pervert like you', 'I am not a pathetic slut like you.', ]
                        message_data = choice(NSFW_reply)
                    print('last part is also fine')
                    await ctx.reply(message_data)
                        
            else:
                print('role error')
                roles = '>'
                for r in database.get_config('chat', message.guild.id):
                    roles = f"{roles} <@&{r}>\n>"
                embed = discord.Embed(description=f"you don't have any of the following roles to talk to me.\n{roles[:-2]}", color=0xF2A2C0)
                await message.channel.send(embed=embed)
                return
        else:
            embed = discord.Embed(title='Bot Ban',
                                  description=f"{message.author.mention} you are banned from using {self.bot.user.mention} till {ban_data[1]}",
                                  color=0xF2A2C0)
            await message.reply(embed=embed)


def setup(bot):
    bot.add_cog(Chat(bot))
