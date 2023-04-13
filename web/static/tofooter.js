var contactBtn = document.getElementById('contact-btn');
var contactSection = document.getElementById('contact');

contactBtn.addEventListener('click', function() {
  contactSection.scrollIntoView({ behavior: 'smooth' });
});