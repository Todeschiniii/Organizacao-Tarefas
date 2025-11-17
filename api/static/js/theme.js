// Sistema de Tema
function inicializarTema() {
    const temaSalvo = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', temaSalvo);
    atualizarBotaoTema(temaSalvo);
    console.log('🎨 Tema inicializado:', temaSalvo);
}

function alternarTema() {
    const temaAtual = document.documentElement.getAttribute('data-theme') || 'light';
    const novoTema = temaAtual === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', novoTema);
    localStorage.setItem('theme', novoTema);
    atualizarBotaoTema(novoTema);
    
    console.log('🔄 Tema alterado para:', novoTema);
}

function atualizarBotaoTema(tema) {
    const botao = document.getElementById('themeToggle');
    if (botao) {
        // Manter os emojis originais (🌞 e 🌛)
        botao.innerHTML = '<span class="sun">🌞</span><span class="moon">🌛</span>';
        
        // Aplicar transformações baseadas no tema
        const sol = botao.querySelector('.sun');
        const lua = botao.querySelector('.moon');
        
        if (tema === 'light') {
            sol.style.transform = 'scale(2.0)';
            lua.style.transform = 'scale(1.6)';
        } else {
            sol.style.transform = 'scale(1.6)';
            lua.style.transform = 'scale(2.0)';
        }
    }
}

// Inicializar tema quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    inicializarTema();
    
    // Adicionar event listener se o botão existir
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', alternarTema);
    }
});

// Exportar funções para uso em módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { inicializarTema, alternarTema, atualizarBotaoTema };
}