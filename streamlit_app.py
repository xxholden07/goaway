import streamlit as st
import time
from datetime import datetime, timedelta
import random

# Configuração da página
st.set_page_config(
    page_title="GoAway - Hora de Ir Embora!",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-title {
        text-align: center;
        color: white;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 0;
    }
    
    .subtitle {
        text-align: center;
        color: white;
        font-size: 1.2em;
        opacity: 0.9;
        margin-bottom: 2em;
    }
    
    .timer-display {
        text-align: center;
        font-size: 5em;
        font-weight: bold;
        color: white;
        font-family: 'Courier New', monospace;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
        margin: 20px 0;
    }
    
    .status-normal {
        padding: 20px;
        background: #e8f5e9;
        border-radius: 10px;
        color: #2e7d32;
        font-weight: 600;
        text-align: center;
        margin: 20px 0;
    }
    
    .status-warning {
        padding: 20px;
        background: #fff3e0;
        border-radius: 10px;
        color: #e65100;
        font-weight: 600;
        text-align: center;
        margin: 20px 0;
        animation: pulse 2s infinite;
    }
    
    .status-danger {
        padding: 20px;
        background: #ffebee;
        border-radius: 10px;
        color: #c62828;
        font-weight: 600;
        text-align: center;
        margin: 20px 0;
        animation: shake 0.5s infinite;
    }
    
    .reminder-message {
        padding: 15px;
        background: white;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 10px 0;
        font-size: 1.1em;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .urgent-message {
        padding: 20px;
        background: #ff5252;
        color: white;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 1.3em;
        font-weight: bold;
        text-align: center;
        animation: shake 0.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 3em;
        color: white;
    }
</style>
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
    "Você poderia estar dormindo confortavelmente."
]

URGENT_MESSAGES = [
    "URGENTE! Você precisa ir embora AGORA!",
    "ATENÇÃO! Seu tempo acabou!",
    "VAI LOGO! JÁ PASSOU DA HORA!",
    "CORRE! TEM QUE IR EMBORA JÁ!",
    "SÉRIO! TCHAU TCHAU! HORA DE IR!"
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

def add_reminder(message):
    """Adiciona um lembrete ao histórico"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.reminders.insert(0, {"time": timestamp, "message": message})
    if len(st.session_state.reminders) > 10:
        st.session_state.reminders = st.session_state.reminders[:10]

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
    st.subheader("⚙️ Configurar Timer")
    
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
    
    if st.button("🚀 Começar Visita", use_container_width=True, type="primary"):
        start_timer(visit_time, reminder_interval)
        st.rerun()

else:
    # Tela do timer ativo
    remaining = get_remaining_seconds()
    elapsed = get_elapsed_seconds()
    percent_remaining = (remaining / st.session_state.total_seconds) * 100
    
    # Verificar se acabou o tempo
    if remaining <= 0 and not st.session_state.paused:
        message = random.choice(URGENT_MESSAGES)
        st.markdown(f'<div class="urgent-message">{message}</div>', unsafe_allow_html=True)
        add_reminder(message)
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
    st.markdown('<p style="text-align: center; color: white; font-size: 1.1em;">Tempo restante</p>', unsafe_allow_html=True)
    
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
        pause_label = "▶️ Retomar" if st.session_state.paused else "⏸️ Pausar"
        if st.button(pause_label, use_container_width=True):
            pause_timer()
            st.rerun()
    
    with col2:
        if st.button("🛑 Parar", use_container_width=True):
            stop_timer()
            st.rerun()
    
    # Histórico de lembretes
    if st.session_state.reminders:
        st.markdown("---")
        st.subheader("📝 Histórico de Lembretes")
        
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
    '<p style="text-align: center; color: white; opacity: 0.8;">Feito para você não passar vergonha</p>',
    unsafe_allow_html=True
)
