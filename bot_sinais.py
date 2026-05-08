import asyncio
import logging
import os
import random
import sys

import pytz

from dotenv import load_dotenv

from datetime import datetime, timedelta

from telegram import Bot
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.error import BadRequest
from telegram.error import Forbidden
from telegram.error import NetworkError
from telegram.error import RetryAfter
from telegram.error import TelegramError

# ==========================================
# CARREGAR .ENV
# ==========================================

load_dotenv()

# ==========================================
# UTF-8
# ==========================================

sys.stdout.reconfigure(encoding="utf-8")

# ==========================================
# LOGS
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================
# CONFIGURAÇÕES
# ==========================================

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN:
    raise ValueError("BOT_TOKEN não encontrado no .env")

if not CHAT_ID:
    raise ValueError("CHAT_ID não encontrado no .env")

CHAT_ID = int(CHAT_ID)

# ==========================================
# FUSO HORÁRIO
# ==========================================

tz = pytz.timezone("America/Sao_Paulo")

# ==========================================
# JOGOS
# ==========================================

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

# ==========================================
# BOT GLOBAL
# ==========================================

bot = Bot(
    token=TOKEN,
    connect_timeout=30,
    read_timeout=30,
    write_timeout=30,
    pool_timeout=30
)

# ==========================================
# ENVIAR SINAIS
# ==========================================

async def enviar_sinais():

    logger.info("🚀 BOT INICIADO")

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
                [
                    InlineKeyboardButton(
                        "🎰 JOGAR AGORA",
                        url=jogo["link"]
                    )
                ]
            ])

            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=jogo["imagem"],
                caption=mensagem,
                parse_mode="HTML",
                reply_markup=teclado
            )

            logger.info(
                f"✅ Sinal enviado | "
                f"{jogo['nome']} | "
                f"Próximo até: {hora}"
            )

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
                parse_mode="HTML",
                disable_web_page_preview=True
            )

            logger.info("💰 Mensagem de lucro enviada")

            await asyncio.sleep(30)

        except RetryAfter as e:

            tempo_espera = int(e.retry_after)

            logger.warning(
                f"⏳ Flood control | "
                f"Aguardando {tempo_espera}s"
            )

            await asyncio.sleep(tempo_espera)

        except Forbidden as e:

            logger.error(f"🚫 Sem permissão: {e}")

            await asyncio.sleep(60)

        except BadRequest as e:

            logger.error(f"⚠️ BadRequest: {e}")

            await asyncio.sleep(15)

        except NetworkError as e:

            logger.error(f"🌐 Erro de rede: {e}")

            await asyncio.sleep(20)

        except TelegramError as e:

            logger.error(f"⚠️ TelegramError: {e}")

            await asyncio.sleep(20)

        except Exception as erro:

            logger.exception(f"❌ ERRO GERAL: {erro}")

            await asyncio.sleep(30)

# ==========================================
# MAIN
# ==========================================

async def main():

    while True:

        try:

            await enviar_sinais()

        except Exception as erro:

            logger.exception(f"🔥 FALHA CRÍTICA: {erro}")

            await asyncio.sleep(10)

# ==========================================
# EXECUÇÃO
# ==========================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        logger.info("🛑 BOT FINALIZADO")