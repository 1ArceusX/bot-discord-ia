import os
import discord
from google import genai

# Obtener llaves secretas de las variables de entorno
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Inicializar cliente de Gemini
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# Configurar permisos del Bot de Discord
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'¡Bot conectado con éxito como {bot.user}!')

@bot.event
async def on_message(message):
    # Ignorar los mensajes enviados por el propio bot
    if message.author == bot.user:
        return

    # Responder solo si mencionan al bot o le hablan por privado
    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        # Limpiar la mención del texto
        clean_text = message.content.replace(f'<@{bot.user.id}>', '').strip()
        if not clean_text:
            clean_text = "Hola"

        async with message.channel.typing():
            try:
                # Generar respuesta con la IA de Gemini
                response = ai_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=clean_text
                )
                await message.channel.send(response.text)
            except Exception as e:
                await message.channel.send(f"Error al procesar: {e}")

bot.run(DISCORD_TOKEN)
