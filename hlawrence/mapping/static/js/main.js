
// Create floating particles
function createParticles() {
	const particlesContainer = document.getElementById('particles');
	const particleCount = 30;

	for (let i = 0; i < particleCount; i++) {
		const particle = document.createElement('div');
		particle.className = 'particle';
		
		const size = Math.random() * 4 + 2;
		particle.style.width = size + 'px';
		particle.style.height = size + 'px';
		particle.style.left = Math.random() * 100 + '%';
		particle.style.animationDelay = Math.random() * 20 + 's';
		particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
		
		particlesContainer.appendChild(particle);
	}
}


// Navigation functionality
function initializeNavigation() {
    // Mobile menu toggle functionality
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            
            // Update toggle icon
            const icon = this.querySelector('span');
            if (navMenu.classList.contains('active')) {
                icon.textContent = '✕';
            } else {
                icon.textContent = '☰';
            }
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                const icon = mobileToggle.querySelector('span');
                icon.textContent = '☰';
            }
        });
        
        // Close mobile menu when window is resized to desktop
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                navMenu.classList.remove('active');
                const icon = mobileToggle.querySelector('span');
                icon.textContent = '☰';
            }
        });
    }
    
    // Highlight active page based on current URL
    highlightActivePage();
    
    // Add spooky sound effects (optional)
    addNavSoundEffects();
}

// Function to highlight the active page
function highlightActivePage() {
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        
        // Remove active class from all links
        link.classList.remove('active');
        
        // Add active class to current page link
        if (currentPath === linkPath || 
            (currentPath === '/' && linkPath === '/') ||
            (currentPath.startsWith(linkPath) && linkPath !== '/')) {
            link.classList.add('active');
        }
    });
}

// Add subtle sound effects for navigation (optional)
function addNavSoundEffects() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Create audio context for sound effects (if supported)
    let audioContext;
    try {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    } catch (e) {
        // Audio context not supported, continue without sound
        return;
    }
    
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            // Create a subtle "whisper" sound effect
            if (audioContext && audioContext.state === 'running') {
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                oscillator.frequency.setValueAtTime(200, audioContext.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(100, audioContext.currentTime + 0.1);
                
                gainNode.gain.setValueAtTime(0, audioContext.currentTime);
                gainNode.gain.linearRampToValueAtTime(0.01, audioContext.currentTime + 0.05);
                gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.1);
                
                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + 0.1);
            }
        });
    });
}

// Initialize navigation when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
});

// Also initialize if this script loads after DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeNavigation);
} else {
    initializeNavigation();
}
