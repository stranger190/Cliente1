// Player de música global
let audioPlayer = null;
let musicaAtual = null;

function criarPlayerMusica() {
    if (document.getElementById('global-player')) return;
    
    const playerHTML = `
        <div id="global-player" style="position: fixed; bottom: 20px; right: 20px; z-index: 2000; background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); border-radius: 50px; padding: 10px 20px; display: none; align-items: center; gap: 15px; border: 1px solid rgba(255,255,255,0.2);">
            <i id="player-play" class="fas fa-play" style="color: white; cursor: pointer;"></i>
            <i id="player-pause" class="fas fa-pause" style="color: white; cursor: pointer; display: none;"></i>
            <span id="player-titulo" style="color: white; font-size: 14px;"></span>
            <i id="player-close" class="fas fa-times" style="color: white; cursor: pointer;"></i>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', playerHTML);
    
    audioPlayer = new Audio();
    
    document.getElementById('player-play').addEventListener('click', function() {
        audioPlayer.play();
        document.getElementById('player-play').style.display = 'none';
        document.getElementById('player-pause').style.display = 'block';
    });
    
    document.getElementById('player-pause').addEventListener('click', function() {
        audioPlayer.pause();
        document.getElementById('player-play').style.display = 'block';
        document.getElementById('player-pause').style.display = 'none';
    });
    
    document.getElementById('player-close').addEventListener('click', function() {
        audioPlayer.pause();
        document.getElementById('global-player').style.display = 'none';
        musicaAtual = null;
    });
    
    audioPlayer.addEventListener('ended', function() {
        document.getElementById('player-play').style.display = 'block';
        document.getElementById('player-pause').style.display = 'none';
    });
}

function tocarMusica(caminho, titulo) {
    criarPlayerMusica();
    
    if (musicaAtual === caminho && audioPlayer && !audioPlayer.paused) {
        audioPlayer.pause();
        document.getElementById('player-play').style.display = 'block';
        document.getElementById('player-pause').style.display = 'none';
        return;
    }
    
    if (musicaAtual === caminho && audioPlayer && audioPlayer.paused) {
        audioPlayer.play();
        document.getElementById('player-play').style.display = 'none';
        document.getElementById('player-pause').style.display = 'block';
        return;
    }
    
    audioPlayer.src = '/' + caminho;
    audioPlayer.play();
    musicaAtual = caminho;
    
    document.getElementById('player-titulo').textContent = titulo || 'Música';
    document.getElementById('global-player').style.display = 'flex';
    document.getElementById('player-play').style.display = 'none';
    document.getElementById('player-pause').style.display = 'block';
}

// Menu mobile toggle
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    const navLinks = document.querySelectorAll('.nav-menu li a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
        });
    });
    
    // Adicionar botões de play nas músicas
    const musicas = document.querySelectorAll('.musica-item');
    musicas.forEach(musica => {
        const btnPlay = musica.querySelector('.btn-play');
        const caminho = musica.dataset.caminho;
        const titulo = musica.dataset.titulo;
        
        if (btnPlay) {
            btnPlay.addEventListener('click', function() {
                tocarMusica(caminho, titulo);
            });
        }
    });
});

// Partículas no fundo
function initParticles() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const ctx = canvas.getContext('2d');
    let particles = [];
    
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 3 + 1;
            this.speedX = Math.random() * 1 - 0.5;
            this.speedY = Math.random() * 1 - 0.5;
            this.color = `rgba(255, 255, 255, ${Math.random() * 0.5 + 0.2})`;
        }
        
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            
            if (this.x > canvas.width) this.x = 0;
            if (this.x < 0) this.x = canvas.width;
            if (this.y > canvas.height) this.y = 0;
            if (this.y < 0) this.y = canvas.height;
        }
        
        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    function init() {
        particles = [];
        for (let i = 0; i < 100; i++) {
            particles.push(new Particle());
        }
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();
        }
        
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 100) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(255, 255, 255, ${0.1 * (1 - distance / 100)})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
        
        requestAnimationFrame(animate);
    }
    
    init();
    animate();
    
    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        init();
    });
}

initParticles();

// Galeria - clique para expandir
const galleryItems = document.querySelectorAll('.gallery-item');
galleryItems.forEach(item => {
    item.addEventListener('click', function() {
        const img = this.querySelector('img');
        if (img) {
            const modal = document.createElement('div');
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0,0,0,0.9)';
            modal.style.zIndex = '2000';
            modal.style.display = 'flex';
            modal.style.alignItems = 'center';
            modal.style.justifyContent = 'center';
            modal.style.cursor = 'pointer';
            
            const modalImg = document.createElement('img');
            modalImg.src = img.src;
            modalImg.style.maxWidth = '90%';
            modalImg.style.maxHeight = '90%';
            modalImg.style.borderRadius = '10px';
            
            modal.appendChild(modalImg);
            document.body.appendChild(modal);
            
            modal.addEventListener('click', function() {
                modal.remove();
            });
        }
    });
});
