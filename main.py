import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_option, create_permission

from mcrcon import MCRcon

Bot = commands.Bot(command_prefix="c:", intents=discord.Intents.all())
slash = SlashCommand(Bot, sync_commands=True)


def main():
    print('Start main()')

    @Bot.event
    async def on_member_join(member):
        # print(member.guild.id)
        if member.guild.id == 840320349890805760:
            guild = Bot.get_guild(840320349890805760)
            role = guild.get_role(841470996988821534)
            await member.add_roles(role)
            channel = Bot.get_channel(841459824054370334)
            await channel.send(content=f'Привет, <@{member.id}>, добро пожаловать! :partying_face:')

    @Bot.event
    async def on_ready():
        print('Ready!')
        await Bot.change_presence(status=discord.Status.dnd)

##################################################################
####                    Command /whitelist                    ####
##################################################################
    @slash.slash(
        name="whitelist",
        description="Добавить себя в Whitelist сервера Minecraft (Только для сабов)",
        options=[
            create_option(
                name="nickname",
                description="Впишите сюда свой никнейм",
                option_type=3,
                required=True,
            )
        ])
    async def whitelist(ctx, nickname: str):
        if ctx.channel_id == 889770631938334721:
            if ' ' in nickname:
                emb = discord.Embed(description=f':warning: Ник не должен содержать пробелы',
                                    colour=discord.Color.red())
                await ctx.send(embed=emb, hidden=True)
            else:
                try:
                    with MCRcon("ip", "pass") as mcr:
                        resp = mcr.command(f'whitelistpro add {nickname}')
                        print(resp)
                except ConnectionRefusedError:
                    emb = discord.Embed(
                        description=f':warning: Не удалось подключиться к серверу',
                        colour=discord.Color.orange())
                    msg = await ctx.send(embed=emb, hidden=True)
                    return
                except Exception:
                    emb = discord.Embed(
                        description=f':warning: Произошла неизвестая ошибка',
                        colour=discord.Color.orange())
                    msg = await ctx.send(embed=emb, hidden=True)
                    return
                time.sleep(1)
                resp = resp[2:]
                resp = resp[:-2]
                resp = resp.replace("§c", "")
                resp = resp.replace("§e", "")
                if resp == f'You have added {nickname} to the whitelist':
                    emb = discord.Embed(
                        description=f'**`{nickname}`** добавлен в Whitelist  {Bot.get_emoji(869494941074718750)}',
                        colour=discord.Color.green())
                    msg = await ctx.send(embed=emb)
                elif resp == 'That person is already whitelisted':
                    emb = discord.Embed(
                        description=f':information_source: Этот ник уже в белом списке!',
                        colour=discord.Color.blue())
                    msg = await ctx.send(embed=emb, hidden=True)
                else:
                    emb = discord.Embed(
                        description=f':interrobang: Что-то пошло не так...',
                        colour=discord.Color.red())
                    print(resp)
                    msg = await ctx.send(embed=emb, hidden=True)
        else:
            emb = discord.Embed(description=f':warning: Вы не можете использовать здесь эту команду',
                                colour=discord.Color.red())
            await ctx.send(embed=emb, hidden=True)

############################################################
####                  Command /command                  ####
############################################################
    @slash.slash(name="command",
                 description="Выполнить команду на сервере. (Только для администрации)")
    @slash.permission(guild_id=840320349890805760,
                      permissions=[
                          create_permission(888877744543367218, SlashCommandPermissionType.ROLE, True),
                          create_permission(840320349890805760, SlashCommandPermissionType.ROLE, False)
                      ])
    async def cmd(ctx, action: str):
        if ctx.guild.id == 840320349890805760:
            try:
                with MCRcon("ip", "pass") as mcr:
                    resp = mcr.command(f'{action}')
                    print(resp)
            except ConnectionRefusedError:
                emb = discord.Embed(
                    description=f':warning: Не удалось подключиться к серверу',
                    colour=discord.Color.orange())
                msg = await ctx.send(embed=emb, hidden=True)
                return
            except Exception:
                emb = discord.Embed(
                    description=f':warning: Произошла неизвестая ошибка',
                    colour=discord.Color.orange())
                msg = await ctx.send(embed=emb, hidden=True)
                return

            resp = resp.replace("§c", "")
            resp = resp.replace("§e", "")
            resp = resp.replace("§a", "")
            resp = resp.replace("§f", "")
            resp = resp.replace("§r", "")
            for num in range(10):
                resp = resp.replace(f"§{num}", "")

            emb = discord.Embed(
                description=f'Ответ сервера:\n```{resp}```',
                colour=discord.Color.blue())
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f':warning: Вы не можете использовать здесь эту команду',
                                colour=discord.Color.red())
            await ctx.send(embed=emb, hidden=True)

    Bot.run('bot.key')


if __name__ == '__main__':
    main()
