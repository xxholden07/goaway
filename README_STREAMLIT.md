# GoAway - Streamlit Version

Versão do app GoAway para Streamlit Cloud!

## 🚀 Deploy no Streamlit Cloud

### Passo 1: Fazer commit no GitHub

1. Crie um repositório no GitHub
2. Faça commit dos arquivos:
   - `streamlit_app.py`
   - `requirements.txt`

```bash
git init
git add streamlit_app.py requirements.txt
git commit -m "GoAway app para Streamlit"
git remote add origin https://github.com/seu-usuario/goaway.git
git push -u origin main
```

### Passo 2: Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Selecione:
   - Repository: `seu-usuario/goaway`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
5. Clique em "Deploy"!

## 🎯 Funcionalidades

- ⏰ Timer configurável
- 🔔 Lembretes periódicos com notificações toast
- 📊 Barra de progresso visual
- ⏸️ Pausar/retomar timer
- 📝 Histórico de lembretes
- 🎨 Interface responsiva e moderna
- 📱 Funciona em mobile

## 💻 Rodar Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar o app
streamlit run streamlit_app.py
```

O app abrirá no navegador em `http://localhost:8501`

## 📱 Usar no Celular

Depois do deploy:
1. Acesse a URL do seu app Streamlit
2. Adicione à tela inicial do celular
3. Use como um app!

## ⚡ Recursos Streamlit

- Auto-refresh a cada segundo quando o timer está ativo
- Notificações toast para lembretes
- Session state para manter o estado do timer
- CSS customizado para visual moderno
- Gradiente roxo elegante

## 🔄 Diferenças da Versão HTML

- Sem síntese de voz (limitação do Streamlit)
- Notificações via toast em vez de notificações do navegador
- Timer server-side (mais confiável)
- Interface Streamlit nativa

## 🎨 Personalização

Você pode personalizar:
- Cores no CSS customizado
- Mensagens de lembrete no código
- Layout e componentes

---

**Aproveite e não passe vergonha ficando muito tempo na casa dos outros!** 😄
