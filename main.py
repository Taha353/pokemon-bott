import discord
from discord.ext import commands

from config import token
from logic import Pokemon

# Bot için yetkileri/intents ayarlama
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
)


@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')


# '!go' komutu
@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        pokemon = Pokemon(author)
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")


# Ek Görev: '!feed' komutu
@bot.command()
async def feed(ctx):
    author = ctx.author.name
    # Kullanıcının bir Pokémon'u olup olmadığını kontrol et
    if author in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[author]
        # logic.py içindeki feed metodunu çağır ve sonucunu gönder
        result = await pokemon.feed()
        await ctx.send(result)
    else:
        await ctx.send(
            "Henüz bir Pokémonunuz yok! Önce '!go' komutuyla bir Pokémon oluşturun."
        )


# Botun çalıştırılması
bot.run(token)
