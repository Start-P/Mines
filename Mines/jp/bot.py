import sys
sys.path.append('../')

import disnake
from disnake.ext import commands

from mines import MinesTableManager

bot = commands.InteractionBot()
user_game_list = {}

with open("token.txt") as f:
    token = f.read().splitlines()[0]

def show_down(table):
    view = disnake.ui.View()
    for x in range(0, 5):
        for y in range(0, 5):
            if table[x][y] == '💣':
                color = disnake.ButtonStyle.red
                emoji = "💣"
            else:
                color = disnake.ButtonStyle.green
                emoji = "💎"
            view.add_item(
                disnake.ui.Button(
                    label="",
                    emoji=emoji,
                    style=color,
                    custom_id=f"button.{str(x)},{str(y)}",
                    row=x,
                    disabled=True
            )       
        )
    return view

def make_button(position_list, _x = None, _y = None, emoji=None, color=None, disabled=None):
    view = disnake.ui.View()
    for x in range(0, 5):
        for y in range(0, 5):
            if [x, y] in position_list:
                view.add_item(
                    disnake.ui.Button(
                        label="",
                        emoji="💎",
                        style=disnake.ButtonStyle.green,
                        custom_id=f"button.{str(x)},{str(y)}",
                        row=x,
                        disabled=disabled
                )       
            )
                continue
            if x==_x and y==_y:
                view.add_item(
                    disnake.ui.Button(
                        label="",
                        emoji=emoji,
                        style=color,
                        custom_id=f"button.{str(x)},{str(y)}",
                        row=x,
                        disabled=disabled
                )       
            )
                continue
            view.add_item(
                disnake.ui.Button(
                    label=" ",
                    style=disnake.ButtonStyle.grey,
                    custom_id=f"button.{str(x)},{str(y)}",
                    row=x,
                    disabled=disabled
            )       
        )
    return view

@bot.slash_command(
    name="mines",
    description="Minesを遊ぶことができます",
    options=[
        disnake.Option(
            name="mines_amount",
            description="爆弾の数を数字で入力してください。",
            type=disnake.OptionType.number,
            required=True,
        ),
    ]
)
async def slash_calc(inter, mines_amount: int):
    if mines_amount < 0 or 25 <=  mines_amount:
        await inter.response.send_message("爆弾の数が多すぎるか少なすぎるため、ゲームを開始することができません。", ephemeral=True)
    view = make_button([])
    raw_button = []
    mines = MinesTableManager()
    table = mines.create_mines_table(int(mines_amount))
    print(table)
    embed = disnake.Embed(
        title="Mines Emulator",
    description="Minesを遊ぶことができます。",
        color=disnake.Colour.blue(),
        )

    embed.set_author(
        name=inter.user.name,
        icon_url=inter.user.avatar.url
            )
    embed.add_field(name="Status", value="継続中")
    embed.add_field(name="爆弾の数", value=str(int(mines_amount)))
    embed.add_field(name="残りパネル数", value="25")
    await inter.response.send_message(embed=embed, view=view)
    user_game_list[str(inter.user.id)] = [mines, []]

@bot.event
async def on_button_click(inter):
    custom_id = inter.data.custom_id
    await inter.response.defer(ephemeral=False)
    if custom_id.startswith("button."):
        xy = custom_id.replace("button.", "").split(",")
        x, y = map(int, xy)
        mines, position_list = user_game_list[str(inter.user.id)]
        checked = mines.check_bomb(x, y)
        already_checked, mines_amount = mines.return_infomation()
        remain_panels = str(25 - already_checked + mines_amount)
        already_checked, mines_amount = map(str, mines.return_infomation())
        if type(checked[0]) == list and checked[1] == "Safe":
            emoji = "💎"
            color = disnake.ButtonStyle.green
            embed_color = disnake.Colour.blue()
            disabled = False
            status = "継続中"
            view = make_button(position_list, x, y, emoji, color, disabled)
        if remain_panels == mines_amount:
            emoji = "💣"
            color = disnake.ButtonStyle.red
            embed_color = disnake.Colour.green()
            disabled = True
            status = "おめでとうございます🎉。\n爆弾を引くことなくゲームを終了できました。"
            view = show_down(mines.return_table())
        if checked[1] == "Bombed":
            emoji = "💣"
            color = disnake.ButtonStyle.red
            embed_color = disnake.Colour.red()
            disabled = True
            status = "爆弾を引いたため、ゲームが終了しました。"
            view = show_down(mines.return_table())
        embed = disnake.Embed(
            title="Mines Emulator",
        description="Minesを遊ぶことができます。",
            color=embed_color,
        )

        embed.set_author(
            name=inter.user.name,
            icon_url=inter.user.avatar.url
            )
        embed.add_field(name="Status", value=status)
        embed.add_field(name="爆弾の数", value=mines_amount)
        embed.add_field(name="残りパネル数", value=remain_panels)
        view = make_button(position_list, x, y, emoji, color, disabled)
        position_list.append([x, y])
        await inter.edit_original_message(embed=embed, view=view)
        user_game_list[str(inter.user.id)] = [mines, position_list]


bot.run(token)
