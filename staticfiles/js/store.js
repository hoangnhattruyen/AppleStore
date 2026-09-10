// Apple Product Detail & Live Swatches Manager
class CaseProductViewer {
  constructor(matrixData, initialModelSlug, initialColorSlug) {
    this.matrix = matrixData;
    this.currentModelSlug = initialModelSlug;
    this.currentColorSlug = initialColorSlug;
    this.viewMode = 'back'; // 'back' or 'inside'
    this.activeVariant = null;

    this.init();
  }

  init() {
    this.bindEvents();
    this.updateViewer();
  }

  setViewMode(mode) {
    this.viewMode = mode;
    this.updateViewer();
  }

  bindEvents() {
    // Model selection buttons
    const modelButtons = document.querySelectorAll('[data-model-slug]');
    modelButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const slug = btn.getAttribute('data-model-slug');
        this.setModel(slug);
      });
    });

    // Color swatch buttons
    const colorButtons = document.querySelectorAll('[data-color-slug]');
    colorButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const slug = btn.getAttribute('data-color-slug');
        this.setColor(slug);
      });
    });

    // Add to cart main button
    const addToCartBtn = document.getElementById('addToCartMainBtn');
    if (addToCartBtn) {
      addToCartBtn.addEventListener('click', () => {
        if (this.activeVariant) {
          addToCart(this.activeVariant.id, 1);
        }
      });
    }

    // Engraving input preview
    const engravingInput = document.getElementById('engravingInput');
    const engravingDisplay = document.getElementById('engravingDisplay');
    if (engravingInput && engravingDisplay) {
      engravingInput.addEventListener('input', (e) => {
        const text = e.target.value.trim();
        engravingDisplay.textContent = text;
        engravingDisplay.style.display = text ? 'block' : 'none';
      });
    }
  }

  setModel(modelSlug) {
    const validColors = Object.keys(this.matrix)
      .filter(key => key.startsWith(`${modelSlug}_`))
      .map(key => key.replace(`${modelSlug}_`, ''));

    const nextColor = validColors.includes(this.currentColorSlug) ? this.currentColorSlug : (validColors[0] || '');
    const params = new URLSearchParams(window.location.search);
    params.set('model', modelSlug);
    if (nextColor) {
      params.set('color', nextColor);
    } else {
      params.delete('color');
    }

    const newUrl = `${window.location.pathname}?${params.toString()}`;
    window.location.href = newUrl;
  }

  setColor(colorSlug) {
    const params = new URLSearchParams(window.location.search);
    params.set('color', colorSlug);
    const newUrl = `${window.location.pathname}?${params.toString()}`;
    window.location.href = newUrl;
  }

  updateViewer() {
    const key = `${this.currentModelSlug}_${this.currentColorSlug}`;
    const variant = this.matrix[key];

    if (!variant) {
      const fallbackColors = Object.keys(this.matrix).filter(k => k.startsWith(`${this.currentModelSlug}_`));
      if (fallbackColors.length > 0) {
        const fallbackKey = fallbackColors[0];
        const fallbackVariant = this.matrix[fallbackKey];
        this.currentColorSlug = fallbackVariant.color_slug;
        this.activeVariant = fallbackVariant;
      } else {
        console.warn(`Variant not found for ${key}`);
        return;
      }
    } else {
      this.activeVariant = variant;
    }

    // 1. Update Case Actual Image (with smooth transition)
    const mainImg = document.getElementById('mainCaseImage');
    if (mainImg) {
      const targetSrc = (this.viewMode === 'inside') ? variant.image_inside_url : variant.image_url;
      if (mainImg.src !== targetSrc) {
        mainImg.style.opacity = '0.4';
        setTimeout(() => {
          mainImg.src = targetSrc;
          mainImg.alt = `${variant.model_name} - ${variant.color_name}`;
          mainImg.style.opacity = '1';
        }, 120);
      }
    }

    // 2. Update color labels
    const colorLabel = document.getElementById('activeColorName');
    if (colorLabel) {
      colorLabel.textContent = `${variant.color_name} (${variant.color_en})`;
    }

    // 3. Update model label
    const modelLabel = document.getElementById('activeModelName');
    if (modelLabel) {
      modelLabel.textContent = variant.model_name;
    }

    // 4. Update price & SKU
    const priceLabel = document.getElementById('activePrice');
    if (priceLabel) {
      priceLabel.textContent = variant.formatted_price;
    }

    const skuLabel = document.getElementById('activeSku');
    if (skuLabel) {
      skuLabel.textContent = variant.sku;
    }

    // 5. Camera Control feature indicator
    const ccBanner = document.getElementById('cameraControlNotice');
    if (ccBanner) {
      ccBanner.style.display = variant.has_camera_control ? 'block' : 'none';
    }
  }
}
