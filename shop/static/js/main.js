// Apple Store VN - Main Javascript
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Toast Notification
function showToast(message, type = 'success') {
  let toast = document.getElementById('apple-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'apple-toast';
    toast.className = 'apple-toast';
    document.body.appendChild(toast);
  }

  const icon = type === 'success' ? '✓' : 'ℹ';
  toast.innerHTML = `<span style="font-weight:bold; color:#34c759;">${icon}</span> <span>${message}</span>`;
  toast.classList.add('show');

  if (window.toastTimeout) clearTimeout(window.toastTimeout);
  window.toastTimeout = setTimeout(() => {
    toast.classList.remove('show');
  }, 3500);
}

// Shopping Bag Drawer Toggle
function toggleBagDrawer(show = true) {
  const overlay = document.getElementById('cartDrawerOverlay');
  if (!overlay) return;
  if (show) {
    overlay.classList.add('open');
    loadCartDrawerData();
  } else {
    overlay.classList.remove('open');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const bagBtn = document.getElementById('navBagBtn');
  if (bagBtn) {
    bagBtn.addEventListener('click', (e) => {
      e.preventDefault();
      toggleBagDrawer(true);
    });
  }

  const closeBtn = document.getElementById('drawerCloseBtn');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => toggleBagDrawer(false));
  }

  const overlay = document.getElementById('cartDrawerOverlay');
  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) toggleBagDrawer(false);
    });
  }
});
