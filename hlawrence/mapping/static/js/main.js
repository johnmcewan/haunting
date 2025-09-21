
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
