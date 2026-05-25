import discord
from discord import app_commands
from discord.ext import commands
import json
import secrets
import os

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Arquivo de armazenamento
KEYS_FILE = "keys.json"
AUTHORIZED_FILE = "authorized.json"

# Carregar dados
def load_keys():
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_keys(data):
    with open(KEYS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_authorized():
    if os.path.exists(AUTHORIZED_FILE):
        with open(AUTHORIZED_FILE, "r") as f:
            return json.load(f)
    return []

def save_authorized(data):
    with open(AUTHORIZED_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_key(length=16):
    """Gera uma key aleatória"""
    return secrets.token_hex(length // 2).upper()

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"✅ Sincronizados {len(synced)} comando(s)")
    except Exception as e:
        print(f"❌ Erro ao sincronizar: {e}")

@bot.tree.command(name="gerar", description="Gera uma nova key para você")
async def gerar(interaction: discord.Interaction):
    """Gera uma key para o usuário"""
    user_id = str(interaction.user.id)
    authorized = load_authorized()
    
    # Verifica se o usuário está autorizado
    if interaction.user.id != interaction.guild.owner_id and user_id not in authorized:
        await interaction.response.send_message(
            "❌ Você não tem permissão para gerar keys!",
            ephemeral=True
        )
        return
    
    keys = load_keys()
    
    # Se o usuário já tem uma key, avisa
    if user_id in keys:
        await interaction.response.send_message(
            f"⚠️ Você já possui uma key: `{keys[user_id]}`\n"
            f"Use `/reset` para deletar a key anterior.",
            ephemeral=True
        )
        return
    
    # Gera nova key
    new_key = generate_key()
    keys[user_id] = new_key
    save_keys(keys)
    
    await interaction.response.send_message(
        f"✅ Key gerada com sucesso!\n"
        f"Sua key: `{new_key}`\n"
        f"⚠️ Guarde bem! Use `/reset` se precisar deletar.",
        ephemeral=True
    )

@bot.tree.command(name="reset", description="Deleta sua key (vai pedir confirmação)")
async def reset(interaction: discord.Interaction):
    """Reseta a key do usuário"""
    user_id = str(interaction.user.id)
    keys = load_keys()
    
    # Verifica se o usuário tem uma key
    if user_id not in keys:
        await interaction.response.send_message(
            "❌ Você não possui uma key!",
            ephemeral=True
        )
        return
    
    current_key = keys[user_id]
    
    # Cria um modal para pedir a key
    class ResetModal(discord.ui.Modal, title="Confirmar Reset"):
        key_input = discord.ui.TextInput(
            label="Digite sua key para confirmar",
            placeholder="Cole sua key aqui...",
            required=True
        )
        
        async def on_submit(self, modal_interaction: discord.Interaction):
            if modal_interaction.data['components'][0]['components'][0]['value'] == current_key:
                # Key correta, deleta
                del keys[user_id]
                save_keys(keys)
                
                await modal_interaction.response.send_message(
                    f"✅ Key deletada com sucesso!\n"
                    f"Sua key `{current_key}` não funciona mais.",
                    ephemeral=True
                )
            else:
                await modal_interaction.response.send_message(
                    "❌ Key incorreta! Tente novamente.",
                    ephemeral=True
                )
    
    await interaction.response.send_modal(ResetModal())

@bot.tree.command(name="add", description="Adiciona uma pessoa autorizada a gerar keys")
@app_commands.describe(user="O usuário que será autorizado")
async def add(interaction: discord.Interaction, user: discord.User):
    """Adiciona um usuário autorizado"""
    
    # Verifica se é o owner
    if interaction.user.id != interaction.guild.owner_id:
        await interaction.response.send_message(
            "❌ Apenas o dono do servidor pode adicionar autorizações!",
            ephemeral=True
        )
        return
    
    authorized = load_authorized()
    user_id = str(user.id)
    
    if user_id in authorized:
        await interaction.response.send_message(
            f"⚠️ {user.mention} já está autorizado!",
            ephemeral=True
        )
        return
    
    authorized.append(user_id)
    save_authorized(authorized)
    
    await interaction.response.send_message(
        f"✅ {user.mention} foi autorizado a gerar keys!",
        ephemeral=True
    )

# Comando para listar autorizados (bônus)
@bot.tree.command(name="autorizados", description="Lista usuários autorizados")
async def autorizados(interaction: discord.Interaction):
    """Lista os usuários autorizados"""
    
    # Verifica se é o owner
    if interaction.user.id != interaction.guild.owner_id:
        await interaction.response.send_message(
            "❌ Apenas o dono do servidor pode ver isso!",
            ephemeral=True
        )
        return
    
    authorized = load_authorized()
    
    if not authorized:
        await interaction.response.send_message(
            "📋 Nenhum usuário autorizado ainda.",
            ephemeral=True
        )
        return
    
    user_mentions = []
    for user_id in authorized:
        try:
            user = await bot.fetch_user(int(user_id))
            user_mentions.append(f"- {user.mention} (`{user_id}`)")
        except:
            user_mentions.append(f"- ID: `{user_id}` (usuário não encontrado)")
    
    await interaction.response.send_message(
        f"📋 **Usuários autorizados:**\n" + "\n".join(user_mentions),
        ephemeral=True
    )

# Rodar o bot
bot.run("SEU_TOKEN_AQUI")
