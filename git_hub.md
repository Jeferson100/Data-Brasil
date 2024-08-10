# Intalar o git

Para instalar o git, execute o seguinte comando:

```bash
sudo apt-get update
```	
```bash
sudo apt-get install git
```
```bash
git config --global --add safe.directory /workspaces/fundamentalist-stock-brazil
```
```bash
git config --global user.email "sehnemjeferson@gmail.com"
git config --global user.name "jeferson100"
```
# Conectar ao GitHub
## Passo 1: Gerar uma chave SSH (se ainda não tiver uma)
Se você ainda não tiver uma chave SSH configurada, gere uma nova chave SSH:

bash
Copiar código
```bash
ssh-keygen -t ed25519 -C "seu-email@example.com"
```

Siga as instruções na tela e aceite os padrões pressionando Enter. Isso criará uma chave SSH pública e privada em `cat ~/.ssh/id_ed25519` e `cat ~/.ssh/id_ed25519.pub`.

## Passo 2: Adicionar a chave SSH ao agente SSH

Inicie o agente SSH e adicione sua chave SSH privada ao agente:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```
## Passo 3: Adicionar a chave SSH ao GitHub

Copie o conteúdo da sua chave SSH pública para o clipboard:
```bash
cat ~/.ssh/id_ed25519.pub
```
Vá para [GitHub](https://github.com/settings/keys) e faça login.

Navegue até as configurações de SSH e GPG keys: Settings > SSH and GPG keys.

Clique em "New SSH key" e cole a chave pública no campo Key. Dê um título e clique em "Add SSH key".

## Passo 4: Testar a conexão SSH
Teste a conexão SSH com o GitHub:

```bash
ssh -T git@github.com
```
Se configurado corretamente, você verá uma mensagem de sucesso.





