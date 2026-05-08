import asyncio
import random
import pytz
from datetime import datetime, timedelta
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest, TelegramError

# ================================
# CONFIGURAÇÕES
# ================================

TOKEN = "8645674167:AAH9NCm_MHzHhSYSzivgSgmnXcU8vEYNGVU"
CHAT_ID = 6541300474

# FUSO HORÁRIO BRASIL
tz = pytz.timezone("America/Sao_Paulo")

jogos = {
    "tiger": {
        "nome": "🐯 FORTUNE TIGER 🐯",
        "imagem": "https://raster.digital/sinais/imagens/fortunetiger.jpg",
        "link": "https://hype33.fun"
    },
    "snake": {
        "nome": "🐍 FORTUNE SNAKE 🐍",
        "imagem": "https://raster.digital/sinais/imagens/fortunesnake.jpg",
        "link": "https://hype33.fun"
    },
    "dragon": {
        "nome": "🐉 FORTUNE DRAGON 🐉",
        "imagem": "https://raster.digital/sinais/imagens/fortunedragon.jpg",
        "link": "https://hype33.fun"
    },
    "rabbit": {
        "nome": "🐰 RABBIT FORTUNE 🐰",
        "imagem": "https://raster.digital/sinais/imagens/rabbitfortune.jpg",
        "link": "https://hype33.fun"
    }
}

# ================================
# BOT
# ================================

async def enviar_sinais():

    bot = Bot(token=TOKEN)

    print("🚀 BOT INICIADO")

    while True:

        try:

            jogo = random.choice(list(jogos.values()))

            giros = random.randint(8, 15)
            normal = random.randint(8, 12)
            turbo = random.randint(1, 3)

            duracao = random.randint(240, 360)

            tempo = datetime.now(tz) + timedelta(seconds=duracao)
            hora = tempo.strftime("%H:%M")

            mensagem = f"""
🤑 <b>HORA DE FAZER GRANA</b>

{jogo["nome"]}

⭐ Máximo de Giros: {giros}

🔥 APROVEITE AGORA

💰 {normal}X Normal
🚀 {turbo}X Turbo

💡 Dica: Alterne os giros

⏰ Brecha até: {hora}

ESSA AQUI PAGA MUITO ⤵️
"""

            teclado = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎰 JOGAR AGORA", url=jogo["link"])]
            ])

            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=jogo["imagem"],
                caption=mensagem,
                parse_mode="HTML",
                reply_markup=teclado
            )

            print("✅ Sinal enviado:", jogo["nome"], "| Próximo até:", hora)

            await asyncio.sleep(duracao - 30)

            mensagem_lucro = """
✅ <b>LUCRANDO COM SINAIS</b>

🤑 Recolha seu lucro e fique atento à próxima oportunidade.

🎁 Cadastre-se
https://www.hype33.fun

🔎 Buscando novas brechas...
"""

            await bot.send_message(
                chat_id=CHAT_ID,
                text=mensagem_lucro,
                parse_mode="HTML"
            )

            print("💰 Mensagem de lucro enviada")

            await asyncio.sleep(30)

        except BadRequest as e:
            print("⚠️ Erro Telegram:", e)
            await asyncio.sleep(10)

        except TelegramError as e:
            print("⚠️ Falha Telegram:", e)
            await asyncio.sleep(10)

        except Exception as erro:
            print("❌ ERRO GERAL:", erro)
            await asyncio.sleep(10)


# ================================
# EXECUÇÃO
# ================================

if __name__ == "__main__":
    asyncio.run(enviar_sinais())
