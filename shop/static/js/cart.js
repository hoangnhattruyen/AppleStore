// Apple Shopping Bag (Cart) Manager
async function addToCart(variantId, quantity = 1) {
  try {
    const response = await fetch('/cart/add/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ variant_id: variantId, quantity: quantity }),
    });

    const data = await response.json();
    if (data.success) {
      updateCartBadge(data.cart_count);
      renderDrawerItems(data.items, data.formatted_total_price);
      showToast(data.message || 'Đã thêm vào túi hàng');
      toggleBagDrawer(true);
    } else {
      showToast(data.error || 'Có lỗi xảy ra', 'error');
    }
  } catch (error) {
    console.error('Cart add error:', error);
    showToast('Lỗi kết nối máy chủ', 'error');
  }
}

async function updateCartItem(variantId, quantity) {
  try {
    const response = await fetch('/cart/update/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ variant_id: variantId, quantity: quantity }),
    });

    const data = await response.json();
    if (data.success) {
      updateCartBadge(data.cart_count);
      renderDrawerItems(data.items, data.formatted_total_price);
    }
  } catch (error) {
    console.error('Cart update error:', error);
  }
}

async function removeCartItem(variantId) {
  try {
    const response = await fetch('/cart/remove/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ variant_id: variantId }),
    });

    const data = await response.json();
    if (data.success) {
      updateCartBadge(data.cart_count);
      renderDrawerItems(data.items, data.formatted_total_price);
      showToast('Đã xóa sản phẩm khỏi túi');
    }
  } catch (error) {
    console.error('Cart remove error:', error);
  }
}

async function loadCartDrawerData() {
  try {
    const response = await fetch('/cart/json/');
    const data = await response.json();
    updateCartBadge(data.cart_count);
    renderDrawerItems(data.items, data.formatted_total_price);
  } catch (error) {
    console.error('Cart load error:', error);
  }
}

function updateCartBadge(count) {
  const badge = document.getElementById('cartNavBadge');
  if (badge) {
    badge.textContent = count;
    badge.style.display = count > 0 ? 'inline-block' : 'none';
  }
}

function renderDrawerItems(items, formattedTotal) {
  const container = document.getElementById('drawerItemsContainer');
  const totalElem = document.getElementById('drawerTotalPrice');
  const footer = document.getElementById('drawerFooter');

  if (!container) return;

  if (!items || items.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding: 48px 12px; color: var(--apple-text-secondary);">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom:12px; opacity:0.6;">
          <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <path d="M16 10a4 4 0 0 1-8 0"></path>
        </svg>
        <p style="font-size:16px; font-weight:600; color:var(--apple-dark-gray); margin-bottom:4px;">Túi của bạn đang trống.</p>
        <p style="font-size:13px;">Giao hàng miễn phí và đổi trả miễn phí cho mọi đơn hàng.</p>
      </div>
    `;
    if (footer) footer.style.display = 'none';
    return;
  }

  if (footer) footer.style.display = 'block';
  if (totalElem) totalElem.textContent = formattedTotal;

  container.innerHTML = items.map(item => `
    <div class="cart-item-row" data-variant-id="${item.variant_id}">
      <img src="${item.image_url}" alt="${item.color_name}" style="width:36px; height:58px; object-fit:contain; filter:drop-shadow(0 2px 4px rgba(0,0,0,0.15)); flex-shrink:0;">
      <div class="cart-item-details">
        <div class="cart-item-name">${item.product_title}</div>
        <div class="cart-item-meta">${item.phone_model} — ${item.color_name}</div>
        <div class="cart-item-qty">
          <button class="qty-btn" onclick="updateCartItem(${item.variant_id}, ${item.quantity - 1})">-</button>
          <span style="font-size:13px; font-weight:600;">${item.quantity}</span>
          <button class="qty-btn" onclick="updateCartItem(${item.variant_id}, ${item.quantity + 1})">+</button>
          <button class="cart-remove-btn" onclick="removeCartItem(${item.variant_id})">Xóa</button>
        </div>
      </div>
      <div class="cart-item-price">${item.formatted_total_price}</div>
    </div>
  `).join('');
}
