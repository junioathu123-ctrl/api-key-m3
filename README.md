# API M3 Key Bot 🔑

Bot Discord para gerenciar keys com comandos slash.

## Funcionalidades

- **`/gerar`** - Gera uma nova key para o usuário
- **`/reset`** - Deleta a key (pede confirmação digitando a key)
- **`/add`** - Autoriza um usuário a gerar keys (apenas owner)
- **`/autorizados`** - Lista os usuários autorizados (apenas owner)

## Instalação

### 1. Clonar o repositório
```bash
git clone https://github.com/junioathu123-ctrl/api-key-m3.git
cd api-key-m3
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar o token
Edite `main.py` e substitua `SEU_TOKEN_AQUI` pelo seu token do bot:

```python
bot.run("SEU_TOKEN_AQUI")
```

### 4. Rodar o bot
```bash
python main.py
```

## Como usar

### `/gerar`
- Gera uma key aleatória de 16 caracteres
- Apenas usuários autorizados ou o owner podem usar
- Cada usuário só pode ter uma key por vez

### `/reset`
- Abre um modal pedindo para confirmar com a key atual
- Se digitar a key correta, ela é deletada
- Depois disso a key não funciona mais

### `/add @usuario`
- Autoriza um usuário a gerar keys
- Apenas o owner do servidor pode fazer isso

### `/autorizados`
- Lista todos os usuários autorizados
- Apenas o owner pode ver

## Arquivos de dados

- `keys.json` - Armazena as keys geradas (user_id -> key)
- `authorized.json` - Armazena os IDs dos usuários autorizados

## Permissões necessárias no Discord

O bot precisa dessas permissões:
- Send Messages
- Use Slash Commands
- Send Messages in Threads

## Autor

Desenvolvido por junioathu123-ctrl
