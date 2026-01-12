// Estado da aplicação
let timer = null;
let isPaused = false;
let totalSeconds = 0;
let secondsRemaining = 0;
let reminderIntervalSeconds = 0;
let nextReminderAt = 0;
let useVoice = true;
let useNotification = true;

// Estado do screensaver
let screensaverTimer = null;
let currentActivity = 'idle';
let activityDuration = 0;

// Mensagens para lembretes
const reminderMessages = [
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
];

const urgentMessages = [
    "URGENTE! Você precisa ir embora AGORA!",
    "ATENÇÃO! Seu tempo acabou!",
    "VAI LOGO! JÁ PASSOU DA HORA!",
    "CORRE! TEM QUE IR EMBORA JÁ!",
    "SÉRIO! TCHAU TCHAU! HORA DE IR!"
];

// Elementos DOM
const setupCard = document.getElementById('setupCard');
const timerCard = document.getElementById('timerCard');
const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const stopBtn = document.getElementById('stopBtn');
const timeDisplay = document.getElementById('timeDisplay');
const progressFill = document.getElementById('progressFill');
const statusMessage = document.getElementById('statusMessage');
const logList = document.getElementById('logList');
const castaway = document.getElementById('castaway');
const activityText = document.getElementById('activityText');
const messageBottle = document.getElementById('messageBottle');
const bird = document.getElementById('bird');

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Solicitar permissão para notificações
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
    
    // Prevenir zoom no iOS ao focar em inputs
    const inputs = document.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            document.body.style.zoom = '1.0';
        });
    });
    
    // Manter a tela ativa durante a visita (se suportado)
    if ('wakeLock' in navigator) {
        console.log('Wake Lock API disponível');
    }

    // Event listeners
    startBtn.addEventListener('click', startVisit);
    pauseBtn.addEventListener('click', togglePause);
    stopBtn.addEventListener('click', stopVisit);
});

function startVisit() {
    const visitTime = parseInt(document.getElementById('visitTime').value);
    const reminderInterval = parseInt(document.getElementById('reminderInterval').value);
    useVoice = document.getElementById('useVoice').checked;
    useNotification = document.getElementById('useNotification').checked;

    if (visitTime < 1) {
        alert('Por favor, configure um tempo válido!');
        return;
    }

    // Converter para segundos
    totalSeconds = visitTime * 60;
    secondsRemaining = totalSeconds;
    reminderIntervalSeconds = reminderInterval * 60;
    nextReminderAt = secondsRemaining - reminderIntervalSeconds;

    // Resetar log
    logList.innerHTML = '';

    // Mostrar card do timer
    setupCard.classList.add('hidden');
    timerCard.classList.remove('hidden');
    
    // Tentar manter a tela ativa (Wake Lock API)
    if ('wakeLock' in navigator) {
        navigator.wakeLock.request('screen')
            .then(() => console.log('Tela mantida ativa'))
            .catch(err => console.log('Não foi possível manter a tela ativa', err));
    }

    // Iniciar timer
    updateDisplay();
    timer = setInterval(tick, 1000);
    
    // Iniciar screensaver
    startScreensaver();

    addLog('Visita iniciada!');
}

function tick() {
    if (isPaused) return;

    secondsRemaining--;

    if (secondsRemaining <= 0) {
        // Tempo acabou!
        finalReminder();
        stopVisit();
        return;
    }

    updateDisplay();

    // Verificar se é hora de lembrete
    if (secondsRemaining <= nextReminderAt) {
        sendReminder();
        nextReminderAt -= reminderIntervalSeconds;
    }
}

function updateDisplay() {
    const minutes = Math.floor(secondsRemaining / 60);
    const seconds = secondsRemaining % 60;
    
    timeDisplay.textContent = 
        `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    // Atualizar barra de progresso
    const progress = ((totalSeconds - secondsRemaining) / totalSeconds) * 100;
    progressFill.style.width = `${progress}%`;

    // Atualizar status message
    const percentRemaining = (secondsRemaining / totalSeconds) * 100;
    
    if (percentRemaining > 50) {
        statusMessage.className = 'status-message';
        statusMessage.textContent = 'Aproveite sua visita!';
    } else if (percentRemaining > 25) {
        statusMessage.className = 'status-message warning';
        statusMessage.textContent = 'Metade do tempo já passou!';
    } else {
        statusMessage.className = 'status-message danger';
        statusMessage.textContent = 'Tempo acabando! Prepare-se para sair!';
        timerCard.classList.add('shake');
        setTimeout(() => timerCard.classList.remove('shake'), 500);
    }
}

function sendReminder() {
    const message = reminderMessages[Math.floor(Math.random() * reminderMessages.length)];
    
    // Vibração em dispositivos móveis
    if ('vibrate' in navigator) {
        navigator.vibrate([200, 100, 200]);
    }
    
    // Síntese de voz
    if (useVoice && 'speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(message);
        utterance.lang = 'pt-BR';
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        speechSynthesis.speak(utterance);
    }

    // Notificação
    if (useNotification && 'Notification' in window && Notification.permission === 'granted') {
        new Notification('GoAway - Lembrete', {
            body: message,
            tag: 'goaway-reminder',
            vibrate: [200, 100, 200],
            requireInteraction: false
        });
    }

    // Adicionar ao log
    addLog(message);
}

function finalReminder() {
    const message = urgentMessages[Math.floor(Math.random() * urgentMessages.length)];
    
    // Vibração forte em dispositivos móveis
    if ('vibrate' in navigator) {
        navigator.vibrate([300, 100, 300, 100, 300]);
    }
    
    // Síntese de voz com ênfase
    if (useVoice && 'speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(message);
        utterance.lang = 'pt-BR';
        utterance.rate = 1.2;
        utterance.pitch = 1.2;
        utterance.volume = 1.0;
        speechSynthesis.speak(utterance);
    }

    // Notificação urgente
    if (useNotification && 'Notification' in window && Notification.permission === 'granted') {
        new Notification('GoAway - URGENTE!', {
            body: message,
            requireInteraction: true,
            tag: 'goaway-urgent',
            vibrate: [300, 100, 300, 100, 300]
        });
    }

    addLog(message);
}

function togglePause() {
    isPaused = !isPaused;
    
    if (isPaused) {
        pauseBtn.textContent = 'Retomar';
        statusMessage.textContent = 'Timer pausado';
        statusMessage.className = 'status-message';
        addLog('Timer pausado');
    } else {
        pauseBtn.textContent = 'Pausar';
        updateDisplay();
        addLog('Timer retomado');
    }
}

function stopVisit() {
    clearInterval(timer);
    timParar screensaver
    stopScreensaver();
    
    // er = null;
    isPaused = false;
    
    // Voltar para tela de configuração
    setupCard.classList.remove('hidden');
    timerCard.classList.add('hidden');
    
    pauseBtn.textContent = 'Pausar';
    
    if (secondsRemaining <= 0) {
        alert('Tempo esgotado! Você deveria ter ido embora!');
    }
}

function addLog(message) {
    const li = document.createElement('li');
    const now = new Date();
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
    li.textContent = `[${timeStr}] ${message}`;
    logList.insertBefore(li, logList.firstChild);
    
    // Manter apenas os últimos 10 logs
 

// ===== SCREENSAVER FUNCTIONS =====

const activities = [
    { name: 'idle', text: 'Esperando na ilha...', duration: 5000, animation: 'idle' },
    { name: 'walking', text: 'Caminhando pela praia...', duration: 4000, animation: 'walking' },
    { name: 'waving', text: 'Acenando para um navio distante...', duration: 3000, animation: 'waving' },
    { name: 'sitting', text: 'Sentado pensando na vida...', duration: 5000, animation: 'sitting' },
    { name: 'bottle', text: 'Encontrou uma garrafa com mensagem!', duration: 4000, animation: 'idle' },
    { name: 'bird', text: 'Um pássaro passou voando...', duration: 3000, animation: 'idle' },
    { name: 'looking', text: 'Olhando o horizonte...', duration: 4000, animation: 'waving' },
    { name: 'resting', text: 'Descansando embaixo da palmeira...', duration: 5000, animation: 'sitting' }
];

function startScreensaver() {
    currentActivity = 'idle';
    activityDuration = 0;
    screensaverTimer = setInterval(updateScreensaver, 100);
    changeActivity();
}

function stopScreensaver() {
    if (screensaverTimer) {
        clearInterval(screensaverTimer);
        screensaverTimer = null;
    }
    resetCastaway();
}

function updateScreensaver() {
    if (isPaused) return;
    
    activityDuration += 100;
    
    // Mudar atividade quando o tempo acabar
    if (activityDuration >= getCurrentActivity().duration) {
        changeActivity();
    }
}

function getCurrentActivity() {
    return activities.find(a => a.name === currentActivity) || activities[0];
}

function changeActivity() {
    // Escolher nova atividade aleatória
    const newActivity = activities[Math.floor(Math.random() * activities.length)];
    currentActivity = newActivity.name;
    activityDuration = 0;
    
    // Atualizar texto
    activityText.textContent = newActivity.text;
    
    // Resetar animações
    resetCastaway();
    
    // Aplicar nova animação
    setTimeout(() => {
        switch(newActivity.animation) {
            case 'walking':
                castaway.classList.add('walking');
                break;
            case 'waving':
                castaway.classList.add('waving');
                break;
            case 'sitting':
                castaway.classList.add('sitting');
                break;
            case 'idle':
            default:
                // Usa a animação padrão
                break;
        }
        
        // Ações especiais
        if (currentActivity === 'bottle') {
            messageBottle.classList.remove('hidden');
            setTimeout(() => {
                messageBottle.classList.add('hidden');
            }, newActivity.duration - 500);
        }
        
        if (currentActivity === 'bird') {
            bird.classList.add('flying');
            setTimeout(() => {
                bird.classList.remove('flying');
            }, newActivity.duration);
        }
    }, 100);
}

function resetCastaway() {
    castaway.classList.remove('walking', 'waving', 'sitting');
    castaway.style.left = '50%';
    messageBottle.classList.add('hidden');
    bird.classList.remove('flying');
}   while (logList.children.length > 10) {
        logList.removeChild(logList.lastChild);
    }
}
