import os
import discord

from html2image import Html2Image
from PIL import Image
import io

html_str = """

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  </head>
  <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@800&display=swap" rel="stylesheet" />
  <style>
    body {{
      padding: 0px;
      margin: 0;
    }}

    #welcomeCard {{
      width: 1045px;
      height: 450px;
      background-color: #2f3136;
      background-color:red;
    }}

    #image {{
      display: flex;
      justify-content: center;
      width: 1045px;
      height: 450px;
    }}

    #avatar {{
      top: 45px;
      width: 210px;
      border-radius: 150px;
      position: absolute;
    }}

    #memname {{
      font-size: 50px;
      font-family: "Baloo 2", cursive;
      position: absolute;
      text-align: center;
      width: 1045px;
      height: 450px;
      top: 260px;
      color: wheat;
    }}

    #bottom-text {{
      text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
      font-size: 25px;
      font-family: "Baloo 2", cursive;
      position: absolute;
      text-align: center;
      width: 1045px;
      height: 450px;
      top: 330px;
      color: skyblue;
    }}
  </style>

  <body>
    <div id="welcomeCard">
      <div id="image">
        <img src="{avatar_url}" alt="" id="avatar" />
      </div>
      <div id="memname">{user}</div>
      <div id="bottom-text">Welcome to {guild_name}!</div>
    </div>
  </body>
</html>


"""


async def get_welcome_card(member: discord.Member):
    guild_name = member.guild.name
    member_name = str(member)
    avatar_url = str(member.display_avatar.url)

    html = html_str.format(
        guild_name=guild_name, user=member_name, avatar_url=avatar_url
    )
    filename = "wel_{}_{}.png".format(member.guild.id, member.id)

    h2i = Html2Image()
    h2i.screenshot(html_str=html, save_as=filename, size=(1045, 450))

    pil_image = Image.open(filename)
    img_io = io.BytesIO()
    pil_image.save(img_io, "PNG")
    img_io.seek(0)
    pil_image.close()
    os.remove(filename)

    return img_io
