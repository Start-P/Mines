import disnake
from disnake.ext import commands
from mines import MinesTableManager

bot = commands.InteractionBot()
user_game_list = {}

def make_button(_x = None, _y = None, emoji = None):
    view = disnake.ui.View()
    for x in range(0, 5):
        for y in range(0, 5):
            if _x and _y and x==_x and y==_y:
                view.add_item(
                    disnake.ui.Button(
                        label=" ",
                        emoji=emoji,
                        style=disnake.ButtonStyle.grey,
                        custom_id=f"button.{str(x)},{str(y)}",
                        row=x
                )       
            )
            view.add_item(
                disnake.ui.Button(
                    label=" ",
                    style=disnake.ButtonStyle.grey,
                    custom_id=f"button.{str(x)},{str(y)}",
                    row=x
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
    view = make_button()
    raw_button = []
    mines = MinesTableManager()
    table = mines.create_mines_table(int(mines_amount))
    await inter.response.send_message("クリックしてプレイ", view=view)
    user_game_list[str(inter.user.id)] = mines

@bot.event
async def on_button_click(inter):
    custom_id = inter.data.custom_id
    await inter.response.defer(ephemeral=False)
    if custom_id.startswith("button."):
        xy = custom_id.replace("button.", "").split(",")
        x, y = map(int, xy)
        mines = user_game_list[str(inter.user.id)]
        checked = mines.check_bomb(x, y)
        if type(checked[0]) == list and checked[1] == "Safe":
            emoji = "💎"
        view = make_button(x, y, emoji)
        await inter.response.edit_message(view=view)


bot.run()
