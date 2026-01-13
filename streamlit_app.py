import streamlit as st
import time
from datetime import datetime, timedelta
import random

# Configuração da página
st.set_page_config(
    page_title="GoAway - 8-Bit Edition",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado 8-bits retro com screensaver
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    * {
        image-rendering: pixelated;
        image-rendering: -moz-crisp-edges;
        image-rendering: crisp-edges;
    }
    
    .stApp {
        background: #2b2b2b;
        font-family: 'Press Start 2P', monospace;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.15),
            rgba(0, 0, 0, 0.15) 1px,
            transparent 1px,
            transparent 2px
        );
        pointer-events: none;
        z-index: 9999;
    }
    
    .main-title {
        text-align: center;
        color: #00ff00;
        font-size: 1.8em;
        font-weight: normal;
        font-family: 'Press Start 2P', monospace;
        text-shadow: 2px 2px 0 #006600, 4px 4px 0 #003300;
        margin-bottom: 10px;
        padding: 20px;
        background: #000;
        border: 4px solid #00ff00;
        box-shadow: 0 0 10px #00ff00, inset 0 0 10px rgba(0, 255, 0, 0.3);
        animation: blink 1s steps(2) infinite;
    }
    
    .subtitle {
        text-align: center;
        color: #ffff00;
        font-size: 0.6em;
        font-family: 'Press Start 2P', monospace;
        text-shadow: 1px 1px 0 #666600;
        margin-bottom: 2em;
    }
    
    .timer-display {
        text-align: center;
        font-size: 3.5em;
        font-weight: normal;
        color: #00ff00;
        font-family: 'Press Start 2P', monospace;
        text-shadow: 2px 2px 0 #006600, 0 0 10px #00ff00;
        margin: 20px 0;
        padding: 30px;
        background: #000;
        border: 4px solid #00ff00;
        box-shadow: inset 0 0 20px rgba(0, 255, 0, 0.3);
        animation: blink 1s steps(1) infinite;
    }
    
    .status-normal {
        padding: 15px;
        background: #000;
        border: 3px solid #00ff00;
        color: #00ff00;
        font-weight: normal;
        font-family: 'Press Start 2P', monospace;
        font-size: 0.6em;
        text-align: center;
        margin: 20px 0;
        text-shadow: 1px 1px 0 #006600;
        box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.3);
    }
    
    .status-warning {
        padding: 15px;
        background: #000;
        border: 3px solid #ff8800;
        color: #ff8800;
        font-weight: normal;
        font-family: 'Press Start 2P', monospace;
        font-size: 0.6em;
        text-align: center;
        margin: 20px 0;
        text-shadow: 1px 1px 0 #663300;
        box-shadow: inset 0 0 10px rgba(255, 136, 0, 0.3);
        animation: blink 0.5s steps(2) infinite;
    }
    
    .status-danger {
        padding: 15px;
        background: #000;
        border: 3px solid #ff0000;
        color: #ff0000;
        font-weight: normal;
        font-family: 'Press Start 2P', monospace;
        font-size: 0.6em;
        text-align: center;
        margin: 20px 0;
        text-shadow: 1px 1px 0 #660000;
        box-shadow: inset 0 0 10px rgba(255, 0, 0, 0.3);
        animation: blink 0.3s steps(2) infinite;
    }
    
    .reminder-message {
        padding: 12px;
        background: #000;
        border: 2px solid #00ff00;
        margin: 10px 0;
        font-size: 0.5em;
        font-family: 'Press Start 2P', monospace;
        color: #00ffff;
        text-shadow: 1px 1px 0 #006666;
        box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.2);
    }
    
    .urgent-message {
        padding: 20px;
        background: #000;
        border: 4px solid #ff0000;
        color: #ff0000;
        margin: 10px 0;
        font-size: 1em;
        font-weight: normal;
        font-family: 'Press Start 2P', monospace;
        text-align: center;
        text-shadow: 2px 2px 0 #660000;
        box-shadow: 0 0 20px #ff0000, inset 0 0 20px rgba(255, 0, 0, 0.3);
        animation: blink 0.2s steps(2) infinite;
    }
    
    @keyframes blink {
        0%, 49% { opacity: 1; }
        50%, 100% { opacity: 0.3; }
    }
    
    /* Estilizar elementos Streamlit */
    div[data-testid="stMetricValue"] {
        font-size: 2em;
        color: #00ff00;
        font-family: 'Press Start 2P', monospace;
    }
    
    .stButton button {
        background: #000;
        color: #00ff00;
        border: 4px solid #00ff00;
        font-family: 'Press Start 2P', monospace;
        font-size: 0.7em;
        padding: 15px;
        text-shadow: 1px 1px 0 #006600;
        box-shadow: 4px 4px 0 #003300;
        transition: none;
    }
    
    .stButton button:hover {
        background: #003300;
        box-shadow: 2px 2px 0 #003300;
    }
    
    .stNumberInput input {
        background: #000;
        color: #00ff00;
        border: 3px solid #00ff00;
        font-family: 'Press Start 2P', monospace;
        box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.3);
    }
    
    label {
        color: #00ffff;
        font-family: 'Press Start 2P', monospace;
        font-size: 0.6em;
        text-shadow: 1px 1px 0 #006666;
    }
    
    h2, h3 {
        color: #ffff00;
        font-family: 'Press Start 2P', monospace;
        text-shadow: 2px 2px 0 #666600;
    }
    
    .stProgress > div > div {
        background: #000;
        border: 3px solid #00ff00;
    }
    
    .stProgress > div > div > div {
        background: repeating-linear-gradient(
            90deg,
            #00ff00,
            #00ff00 4px,
            #00cc00 4px,
            #00cc00 8px
        );
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.8);
    }
    
    hr {
        border-color: #00ff00;
        border-width: 2px;
        border-style: solid;
    }
    
    /* Screensaver 8-bit */
    .screensaver-container {
        position: relative;
        width: 100%;
        height: 200px;
        margin-bottom: 20px;
    }
    
    .screensaver-pixel {
        position: relative;
        width: 100%;
        height: 100%;
        background: 
            repeating-linear-gradient(
                0deg,
                #5599ff 0px,
                #5599ff 2px,
                #77aaff 2px,
                #77aaff 4px
            );
        border: 4px solid #00ff00;
        overflow: hidden;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5), 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    .sun-pixel {
        position: absolute;
        top: 15px;
        right: 25px;
        width: 24px;
        height: 24px;
        background: #ffff00;
        box-shadow: 0 0 8px rgba(255, 255, 0, 0.8);
        animation: sunPulse 2s steps(2) infinite;
    }
    
    @keyframes sunPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .cloud-pixel {
        position: absolute;
        width: 6px;
        height: 6px;
        background: #ffffff;
        opacity: 0.9;
        box-shadow: 
            6px 0 0 #ffffff,
            12px 0 0 #ffffff,
            0 6px 0 #ffffff,
            6px 6px 0 #ffffff,
            12px 6px 0 #ffffff;
    }
    
    .cloud1 {
        top: 20px;
        left: 15%;
        animation: floatCloud 20s steps(100) infinite;
    }
    
    .cloud2 {
        top: 35px;
        left: 55%;
        animation: floatCloud 25s steps(100) infinite;
    }
    
    @keyframes floatCloud {
        0% { transform: translateX(0); }
        100% { transform: translateX(60px); }
    }
    
    .water-pixel {
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 40%;
        background: 
            repeating-linear-gradient(
                0deg,
                #0066cc 0px,
                #0066cc 3px,
                #0088ff 3px,
                #0088ff 6px
            );
        animation: waterWave 1s steps(2) infinite;
    }
    
    @keyframes waterWave {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-2px); }
    }
    
    .sand-pixel {
        position: absolute;
        bottom: 0;
        width: 60%;
        height: 30%;
        left: 20%;
        background: 
            repeating-linear-gradient(
                0deg,
                #ffcc66 0px,
                #ffcc66 3px,
                #ffaa44 3px,
                #ffaa44 6px
            );
        clip-path: polygon(10% 0%, 90% 0%, 100% 100%, 0% 100%);
    }
    
    .palm-pixel {
        position: absolute;
        bottom: 45px;
        left: 35%;
        z-index: 10;
    }
    
    .trunk-pixel {
        width: 10px;
        height: 45px;
        background: 
            repeating-linear-gradient(
                0deg,
                #663300 0px,
                #663300 3px,
                #884422 3px,
                #884422 6px
            );
        margin: 0 auto;
        box-shadow: 0 0 0 1px #000;
    }
    
    .leaves-pixel {
        position: relative;
        width: 32px;
        height: 16px;
        margin-left: -11px;
        margin-top: -8px;
        background: #00aa00;
        box-shadow: 
            -6px -3px 0 0 #00aa00,
            6px -3px 0 0 #00aa00,
            -12px -6px 0 0 #008800,
            12px -6px 0 0 #008800;
    }
    
    .castaway-pixel {
        position: absolute;
        bottom: 50px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 11;
        animation: castawayIdle 1s steps(2) infinite;
    }
    
    @keyframes castawayIdle {
        0%, 100% { transform: translateX(-50%) translateY(0); }
        50% { transform: translateX(-50%) translateY(-3px); }
    }
    
    .head-pixel {
        width: 12px;
        height: 12px;
        background: #ffcc99;
        margin: 0 auto;
        position: relative;
        box-shadow: 0 0 0 2px #000;
    }
    
    .head-pixel::after {
        content: '';
        position: absolute;
        top: 0;
        width: 100%;
        height: 6px;
        background: #663300;
        box-shadow: 0 0 0 1px #000;
    }
    
    .body-pixel {
        width: 12px;
        height: 16px;
        background: #0066ff;
        margin: 2px auto;
        box-shadow: 0 0 0 2px #000;
        position: relative;
    }
    
    .body-pixel::before,
    .body-pixel::after {
        content: '';
        position: absolute;
        width: 10px;
        height: 3px;
        background: #ffcc99;
        top: 0;
        box-shadow: 0 0 0 1px #000;
    }
    
    .body-pixel::before {
        left: -8px;
        transform: rotate(20deg);
    }
    
    .body-pixel::after {
        right: -8px;
        transform: rotate(-20deg);
    }
    
    .bird-pixel {
        position: absolute;
        top: 30px;
        left: -30px;
        width: 12px;
        height: 6px;
        background: #000;
        animation: flyAcross 10s steps(50) infinite;
    }
    
    .bird-pixel::before,
    .bird-pixel::after {
        content: '';
        position: absolute;
        width: 10px;
        height: 3px;
        background: #000;
        top: 2px;
        animation: flap 0.2s steps(1) infinite;
    }
    
    .bird-pixel::before {
        left: -8px;
        transform: rotate(-30deg);
    }
    
    .bird-pixel::after {
        right: -8px;
        transform: rotate(30deg);
    }
    
    @keyframes flyAcross {
        0% { left: -30px; opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { left: calc(100% + 30px); opacity: 0; }
    }
    
    @keyframes flap {
        0% { transform: rotate(-30deg) translateY(0); }
        50% { transform: rotate(-50deg) translateY(-2px); }
    }
    
    .activity-pixel {
        position: absolute;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
        background: #000;
        padding: 5px 8px;
        border: 2px solid #00ff00;
        font-size: 0.4em;
        color: #00ff00;
        font-family: 'Press Start 2P', monospace;
        box-shadow: 0 0 8px rgba(0, 255, 0, 0.5);
        text-align: center;
        text-shadow: 1px 1px 0 #006600;
        animation: blink 2s steps(2) infinite;
    }
    
    /* Chat Widget 8-bit */
    .chat-widget {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 10000;
    }
    
    .chat-button {
        width: 60px;
        height: 60px;
        background: #000;
        border: 4px solid #00ff00;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5em;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.8), 4px 4px 0 #003300;
        animation: chatPulse 2s ease-in-out infinite;
        transition: transform 0.1s;
    }
    
    .chat-button:hover {
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(0, 255, 0, 1), 4px 4px 0 #003300;
    }
    
    @keyframes chatPulse {
        0%, 100% { box-shadow: 0 0 15px rgba(0, 255, 0, 0.8), 4px 4px 0 #003300; }
        50% { box-shadow: 0 0 25px rgba(0, 255, 0, 1), 4px 4px 0 #003300; }
    }
    
    .chat-popup {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 400px;
        height: 600px;
        background: #000;
        border: 4px solid #00ff00;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.8), inset 0 0 10px rgba(0, 255, 0, 0.3);
        display: none;
        flex-direction: column;
        z-index: 10001;
        image-rendering: pixelated;
    }
    
    .chat-popup.active {
        display: flex;
    }
    
    .chat-header {
        background: #00ff00;
        color: #000;
        padding: 15px;
        font-family: 'Press Start 2P', monospace;
        font-size: 0.7em;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 4px solid #00ff00;
    }
    
    .chat-close {
        cursor: pointer;
        font-size: 1.2em;
        font-weight: bold;
        padding: 5px 10px;
        background: #000;
        color: #00ff00;
        border: 2px solid #000;
    }
    
    .chat-close:hover {
        background: #ff0000;
        color: #fff;
        border-color: #ff0000;
    }
    
    .chat-body {
        flex: 1;
        overflow: hidden;
    }
    
    .chat-body iframe {
        width: 100%;
        height: 100%;
        border: none;
    }
    
    @media (max-width: 768px) {
        .chat-popup {
            width: calc(100vw - 40px);
            height: calc(100vh - 140px);
            right: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Widget de Chat Flutuante
st.markdown("""
<div class="chat-widget">
    <div class="chat-button" onclick="toggleChat()">
        🤖
    </div>
    <div class="chat-popup" id="chatPopup">
        <div class="chat-header">
            <span>CHEGO TARDE</span>
            <span class="chat-close" onclick="toggleChat()">X</span>
        </div>
        <div class="chat-body">
            <iframe src="https://chatgpt.com/g/g-69668205e3ac8191b3b04c831302c5d6-chego-tarde" 
                    allow="microphone; camera" 
                    loading="lazy">
            </iframe>
        </div>
    </div>
</div>

<script>
    function toggleChat() {
        const popup = document.getElementById('chatPopup');
        popup.classList.toggle('active');
    }
</script>
""", unsafe_allow_html=True)

# Mensagens para lembretes
REMINDER_MESSAGES = [
    "Psiu! Já pensou em ir embora?",
    "Ei, tá na hora de ir para casa!",
    "Você ainda tá aí? Hora de vazar!",
    "Atenção: seu tempo de visita está acabando!",
    "Lembrete: você precisa ir embora em breve!",
    "Não se esqueça: você tem que ir para casa!",
    "Ei! Já tá passando do horário!",
    "Cuidado! O tempo está acabando!",
    "Alerta: hora de preparar a saída!",
    "Atenção: considere começar a se despedir!",
    "Você poderia estar lendo um livro agora.",
    "Você poderia estar jogando game em casa.",
    "Você poderia estar assistindo sua série favorita.",
    "Você poderia estar descansando no seu sofá.",
    "Você poderia estar fazendo aquele curso online.",
    "Você poderia estar treinando na academia.",
    "Você poderia estar cozinhando algo delicioso.",
    "Você poderia estar tocando seu instrumento.",
    "Você poderia estar aprendendo algo novo.",
    "Você poderia estar dormindo confortavelmente.",
    "Oi, tá na hora de ir pra casa.",
    "Chegou a hora de acabar esse encontro.",
    "Você tá perdendo dinheiro, hein? Podia estar em casa assistindo TV."
]

URGENT_MESSAGES = [
    "URGENTE! Você precisa ir embora AGORA!",
    "ATENÇÃO! Seu tempo acabou!",
    "VAI LOGO! JÁ PASSOU DA HORA!",
    "CORRE! TEM QUE IR EMBORA JÁ!",
    "SÉRIO! TCHAU TCHAU! HORA DE IR!",
    "Chegou a hora de acabar esse encontro!",
    "Oi, tá na hora de ir pra casa!",
    "Você tá perdendo dinheiro, hein? Meu amigo, você podia estar em casa assistindo a GNT. Em vez de estar aqui, tá na hora de se despedir!"
]

# Inicializar session state
if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False
if 'paused' not in st.session_state:
    st.session_state.paused = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0
if 'reminder_interval' not in st.session_state:
    st.session_state.reminder_interval = 0
if 'last_reminder' not in st.session_state:
    st.session_state.last_reminder = 0
if 'reminders' not in st.session_state:
    st.session_state.reminders = []
if 'pause_time' not in st.session_state:
    st.session_state.pause_time = 0
if 'elapsed_before_pause' not in st.session_state:
    st.session_state.elapsed_before_pause = 0

def get_elapsed_seconds():
    """Calcula quantos segundos se passaram"""
    if st.session_state.paused:
        return st.session_state.elapsed_before_pause
    
    if st.session_state.start_time:
        elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
        return st.session_state.elapsed_before_pause + elapsed
    return 0

def get_remaining_seconds():
    """Calcula quantos segundos restam"""
    elapsed = get_elapsed_seconds()
    remaining = st.session_state.total_seconds - elapsed
    return max(0, remaining)

def format_time(seconds):
    """Formata segundos em MM:SS"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def speak_message(message):
    """Reproduz o áudio da mensagem usando Web Speech API"""
    # Escapar aspas na mensagem para JavaScript
    safe_message = message.replace("'", "\\'").replace('"', '\\"')
    
    audio_html = f"""
    <script>
        if ('speechSynthesis' in window) {{
            const utterance = new SpeechSynthesisUtterance("{safe_message}");
            utterance.lang = 'pt-BR';
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;
            
            // Garantir que a síntese está pronta
            if (window.speechSynthesis.speaking) {{
                window.speechSynthesis.cancel();
            }}
            
            window.speechSynthesis.speak(utterance);
        }}
    </script>
    """
    st.components.v1.html(audio_html, height=0)

def add_reminder(message):
    """Adiciona um lembrete ao histórico e reproduz áudio"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.reminders.insert(0, {"time": timestamp, "message": message})
    if len(st.session_state.reminders) > 10:
        st.session_state.reminders = st.session_state.reminders[:10]
    
    # Reproduzir áudio da mensagem
    speak_message(message)

def start_timer(visit_time, reminder_interval):
    """Inicia o timer"""
    st.session_state.timer_active = True
    st.session_state.paused = False
    st.session_state.start_time = datetime.now()
    st.session_state.total_seconds = visit_time * 60
    st.session_state.reminder_interval = reminder_interval * 60
    st.session_state.last_reminder = 0
    st.session_state.reminders = []
    st.session_state.elapsed_before_pause = 0
    add_reminder("Visita iniciada!")

def pause_timer():
    """Pausa o timer"""
    if not st.session_state.paused:
        st.session_state.paused = True
        st.session_state.elapsed_before_pause = get_elapsed_seconds()
        st.session_state.pause_time = datetime.now()
        add_reminder("Timer pausado")
    else:
        st.session_state.paused = False
        st.session_state.start_time = datetime.now()
        add_reminder("Timer retomado")

def stop_timer():
    """Para o timer"""
    st.session_state.timer_active = False
    st.session_state.paused = False
    st.session_state.start_time = None

# Header
st.markdown('<h1 class="main-title">GoAway</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Seu assistente para não ficar tempo demais</p>', unsafe_allow_html=True)

# Mostrar configuração ou timer baseado no estado
if not st.session_state.timer_active:
    # Tela de configuração
    st.markdown("---")
    st.subheader("CONFIGURAR TIMER")
    
    col1, col2 = st.columns(2)
    
    with col1:
        visit_time = st.number_input(
            "Tempo de visita (minutos)",
            min_value=1,
            max_value=480,
            value=60,
            step=5
        )
    
    with col2:
        reminder_interval = st.number_input(
            "Intervalo entre lembretes (minutos)",
            min_value=1,
            max_value=60,
            value=5,
            step=1
        )
    
    st.markdown("---")
    
    if st.button(">>> COMECAR VISITA <<<", use_container_width=True, type="primary"):
        start_timer(visit_time, reminder_interval)
        st.rerun()

else:
    # Tela do timer ativo
    remaining = get_remaining_seconds()
    elapsed = get_elapsed_seconds()
    percent_remaining = (remaining / st.session_state.total_seconds) * 100
    
    # Screensaver 8-bit animado
    screensaver_html = """
    <div class="screensaver-container">
        <div class="screensaver-pixel">
            <div class="sun-pixel"></div>
            <div class="cloud-pixel cloud1"></div>
            <div class="cloud-pixel cloud2"></div>
            <div class="water-pixel"></div>
            <div class="sand-pixel"></div>
            <div class="palm-pixel">
                <div class="trunk-pixel"></div>
                <div class="leaves-pixel"></div>
            </div>
            <div class="castaway-pixel">
                <div class="head-pixel"></div>
                <div class="body-pixel"></div>
            </div>
            <div class="bird-pixel"></div>
        </div>
        <div class="activity-pixel">NA ILHA ESPERANDO...</div>
    </div>
    """
    
    st.markdown(screensaver_html, unsafe_allow_html=True)
    
    # Verificar se acabou o tempo
    if remaining <= 0 and not st.session_state.paused:
        message = random.choice(URGENT_MESSAGES)
        st.markdown(f'<div class="urgent-message">{message}</div>', unsafe_allow_html=True)
        add_reminder(message)
        speak_message(message)  # Áudio extra para mensagem urgente
        time.sleep(2)
        stop_timer()
        st.rerun()
    
    # Verificar se é hora de lembrete
    if not st.session_state.paused and remaining > 0:
        time_since_last = elapsed - st.session_state.last_reminder
        if time_since_last >= st.session_state.reminder_interval:
            message = random.choice(REMINDER_MESSAGES)
            add_reminder(message)
            st.session_state.last_reminder = elapsed
            st.toast(message, icon="🔔")
    
    # Display do timer
    st.markdown(f'<div class="timer-display">{format_time(remaining)}</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #ffff00; font-size: 0.7em; font-family: \'Press Start 2P\', monospace; text-shadow: 1px 1px 0 #666600;">TEMPO RESTANTE</p>', unsafe_allow_html=True)
    
    # Barra de progresso
    progress = min(1.0, elapsed / st.session_state.total_seconds)
    st.progress(progress)
    
    # Status message
    if percent_remaining > 50:
        st.markdown('<div class="status-normal">Aproveite sua visita!</div>', unsafe_allow_html=True)
    elif percent_remaining > 25:
        st.markdown('<div class="status-warning">Metade do tempo já passou!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-danger">Tempo acabando! Prepare-se para sair!</div>', unsafe_allow_html=True)
    
    # Botões de controle
    col1, col2 = st.columns(2)
    
    with col1:
        pause_label = ">>> RETOMAR <<<" if st.session_state.paused else "|| PAUSAR ||"
        if st.button(pause_label, use_container_width=True):
            pause_timer()
            st.rerun()
    
    with col2:
        if st.button("[X] PARAR", use_container_width=True):
            stop_timer()
            st.rerun()
    
    # Histórico de lembretes
    if st.session_state.reminders:
        st.markdown("---")
        st.subheader("HISTORICO DE LEMBRETES")
        
        for reminder in st.session_state.reminders:
            st.markdown(
                f'<div class="reminder-message">[{reminder["time"]}] {reminder["message"]}</div>',
                unsafe_allow_html=True
            )
    
    # Auto-refresh a cada segundo se o timer estiver ativo
    if not st.session_state.paused:
        time.sleep(1)
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #00ff00; font-size: 0.5em; font-family: \'Press Start 2P\', monospace; text-shadow: 1px 1px 0 #006600; animation: blink 2s steps(2) infinite;">FEITO PARA VOCE NAO PASSAR VERGONHA</p>',
    unsafe_allow_html=True
)
