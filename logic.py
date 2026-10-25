from datetime import datetime, timedelta
import random
import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane


class Pokemon:
    pokemons = {}

    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = random.randint(50, 100)
        self.power = random.randint(10, 20)
        # Son beslenme zamanını saklayan nitelik (Başlangıçta None)
        self.last_feed_time = None

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["forms"][0]["name"]
                return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return (
            f"Pokémonunuzun ismi: {self.name} | Canı (HP): {self.hp} | "
            f"Gücü: {self.power}"
        )

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            sans = random.randint(1, 5)
            if sans == 1:
                return (
                    f"@{enemy.pokemon_trainer} un Sihirbaz Pokémonu savaşta "
                    "sihirli bir kalkan kullandı ve saldırıyı savuşturdu! "
                    "Hiç hasar almadı."
                )

        if enemy.hp > self.power:
            enemy.hp -= self.power
            return (
                f"Pokémon eğitmeni @{self.pokemon_trainer}, "
                f"@{enemy.pokemon_trainer}'ne saldırdı.\n"
                f"@{enemy.pokemon_trainer}'nin yeni sağlık durumu: {enemy.hp}"
            )

        enemy.hp = 0
        self.hp += 20
        self.power += 5
        return (
            f"Pokémon eğitmeni @{self.pokemon_trainer}, "
            f"@{enemy.pokemon_trainer}'ni yendi! 🏆\n"
            "Bonus kazandınız! "
            f"Yeni Can: {self.hp}, Yeni Güç: {self.power}"
        )

    async def feed(self):
        # Varsayılan beslenme aralığı (örneğin 60 saniye)
        cooldown = timedelta(seconds=60)
        now = datetime.now()

        if (
            self.last_feed_time is not None
            and now - self.last_feed_time < cooldown
        ):
            remaining = cooldown - (now - self.last_feed_time)
            return (
                f"Pokémonunuzu çok erken beslemeye çalıştınız! "
                f"Tekrar beslemek için {int(remaining.total_seconds())} saniye beklemelisiniz."
            )

        self.hp += 10
        self.last_feed_time = now
        return (
            f"Pokémonunuz başarıyla beslendi! 🍏 Canı arttı. Güncel Can (HP): {self.hp}"
        )

    async def show_img(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["sprites"]["front_default"]
                return None


class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp = random.randint(100, 150)
        self.power = random.randint(8, 15)

    async def feed(self):
        # Wizard için beslenme aralığı kısaltılmış (örneğin 30 saniye)
        cooldown = timedelta(seconds=30)
        now = datetime.now()

        if (
            self.last_feed_time is not None
            and now - self.last_feed_time < cooldown
        ):
            remaining = cooldown - (now - self.last_feed_time)
            return (
                f"Sihirbaz Pokémonunuzu çok erken beslemeye çalıştınız! "
                f"Tekrar beslemek için {int(remaining.total_seconds())} saniye beklemelisiniz."
            )

        self.hp += 15
        self.last_feed_time = now
        return f"✨ Sihirbaz Pokémonunuz özel mamayla beslendi! Güncel Can (HP): {self.hp}"

    async def info(self):
        base_info = await super().info()
        return f"✨ Sihirbaz Pokémonunuz var! ✨\n{base_info}"


class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp = random.randint(60, 90)
        self.power = random.randint(20, 35)

    async def feed(self):
        # Fighter için normalden daha fazla sağlık artışı
        cooldown = timedelta(seconds=60)
        now = datetime.now()

        if (
            self.last_feed_time is not None
            and now - self.last_feed_time < cooldown
        ):
            remaining = cooldown - (now - self.last_feed_time)
            return (
                f"Dövüşçü Pokémonunuzu çok erken beslemeye çalıştınız! "
                f"Tekrar beslemek için {int(remaining.total_seconds())} saniye beklemelisiniz."
            )

        self.hp += 25  # Normalden daha fazla sağlık artışı
        self.last_feed_time = now
        return f"⚔️ Dövüşçü Pokémonunuz doyurucu bir öğün yedi! Normalden fazla can kazandı. Güncel Can (HP): {self.hp}"

    async def attack(self, enemy):
        super_guc = random.randint(5, 15)
        self.power += super_guc
        sonuc = await super().attack(enemy)
        self.power -= super_guc
        return (
            sonuc + f"\n💥 Dövüşçü Pokémon süper saldırı kullandı! "
            f"Eklenen güç: {super_guc}"
        )

    async def info(self):
        base_info = await super().info()
        return f"⚔️ Dövüşçü Pokémonunuz var! ⚔️\n{base_info}"