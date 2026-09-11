document.querySelectorAll('[data-share-url]').forEach((button) => {
  if (!navigator.clipboard || !window.isSecureContext) return;
  button.hidden = false;
  button.addEventListener('click', async () => {
    const status = button.parentElement.querySelector('.share-status');
    try {
      await navigator.clipboard.writeText(button.dataset.shareUrl);
      status.textContent = 'Link copied.';
    } catch {
      status.textContent = 'Use the permalink to copy this page’s address.';
    }
  });
});
