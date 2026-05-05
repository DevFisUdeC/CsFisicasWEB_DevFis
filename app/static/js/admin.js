/**
 * admin.js — Interactividad del Panel de Administración.
 * Responsabilidad: Preview de imágenes, tag input, confirmaciones, copy URL.
 */

document.addEventListener('DOMContentLoaded', () => {
    initImagePreviews();
    initTagInputs();
    initDeleteConfirmations();
    initCopyButtons();
    initFlashAutoDismiss();
    initHomeHeroPreview();
});


/* ═══════════════════════════════════════════
   1. Image Preview on File Input
   ═══════════════════════════════════════════ */

function initImagePreviews() {
    document.querySelectorAll('[data-image-preview]').forEach(input => {
        const previewId = input.getAttribute('data-image-preview');
        const previewEl = document.getElementById(previewId);
        if (!previewEl) return;

        input.addEventListener('change', (e) => {
            previewEl.innerHTML = '';
            const files = Array.from(e.target.files);
            const images = files.filter(f => f.type.startsWith('image/'));

            if (images.length === 0) {
                previewEl.style.display = 'none';
                return;
            }

            previewEl.style.display = 'flex';
            previewEl.style.gap = 'var(--space-sm)';
            previewEl.style.flexWrap = 'wrap';

            images.forEach(file => {
                const reader = new FileReader();
                reader.onload = (ev) => {
                    const img = document.createElement('img');
                    img.src = ev.target.result;
                    img.alt = 'Preview';
                    previewEl.appendChild(img);
                };
                reader.readAsDataURL(file);
            });
        });
    });
}


/* ═══════════════════════════════════════════
   2. Tag Input Component
   ═══════════════════════════════════════════ */

function initTagInputs() {
    document.querySelectorAll('.tag-input').forEach(container => {
        const hiddenInput = container.querySelector('.tag-input__hidden');
        const textField = container.querySelector('.tag-input__field');
        if (!hiddenInput || !textField) return;

        // Initialize tags from hidden input value
        const initialValue = hiddenInput.value.trim();
        if (initialValue) {
            initialValue.split(',').forEach(tag => {
                const trimmed = tag.trim();
                if (trimmed) addTag(container, hiddenInput, trimmed);
            });
        }

        textField.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                const value = textField.value.trim();
                if (value) {
                    addTag(container, hiddenInput, value);
                    textField.value = '';
                }
            }
            // Remove last tag on backspace if field is empty
            if (e.key === 'Backspace' && textField.value === '') {
                const tags = container.querySelectorAll('.tag-input__tag');
                if (tags.length > 0) {
                    tags[tags.length - 1].remove();
                    syncTags(container, hiddenInput);
                }
            }
        });

        // Focus text field when clicking container
        container.addEventListener('click', () => textField.focus());
    });
}

function addTag(container, hiddenInput, text) {
    const textField = container.querySelector('.tag-input__field');
    const tag = document.createElement('span');
    tag.className = 'tag-input__tag';
    tag.appendChild(document.createTextNode(`${text} `));
    const remove = document.createElement('span');
    remove.className = 'tag-input__remove';
    remove.title = 'Eliminar';
    remove.textContent = '×';
    tag.appendChild(remove);

    remove.addEventListener('click', () => {
        tag.remove();
        syncTags(container, hiddenInput);
    });

    container.insertBefore(tag, textField);
    syncTags(container, hiddenInput);
}

function syncTags(container, hiddenInput) {
    const tags = container.querySelectorAll('.tag-input__tag');
    const values = Array.from(tags).map(t => t.textContent.replace('×', '').trim());
    hiddenInput.value = values.join(', ');
}


/* ═══════════════════════════════════════════
   3. Delete Confirmations
   ═══════════════════════════════════════════ */

function initDeleteConfirmations() {
    document.querySelectorAll('[data-confirm]').forEach(el => {
        el.addEventListener('submit', (e) => {
            const message = el.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}


/* ═══════════════════════════════════════════
   4. Copy URL to Clipboard
   ═══════════════════════════════════════════ */

function initCopyButtons() {
    document.querySelectorAll('[data-copy]').forEach(btn => {
        btn.addEventListener('click', () => {
            const text = btn.getAttribute('data-copy');
            navigator.clipboard.writeText(text).then(() => {
                const original = btn.textContent;
                btn.textContent = '¡Copiado!';
                btn.style.color = 'var(--color-success)';
                setTimeout(() => {
                    btn.textContent = original;
                    btn.style.color = '';
                }, 1500);
            });
        });
    });
}


/* ═══════════════════════════════════════════
   5. Flash Auto-Dismiss
   ═══════════════════════════════════════════ */

function initFlashAutoDismiss() {
    document.querySelectorAll('.admin-toast').forEach(toast => {
        setTimeout(() => {
            toast.style.display = 'none';
        }, 5000);
    });
}


/* ═══════════════════════════════════════════
   6. Home Hero Preview Configurator
   ═══════════════════════════════════════════ */

function initHomeHeroPreview() {
    const preview = document.querySelector('[data-page-hero-preview], [data-home-hero-preview]');
    if (!preview) return;
    const canvas = preview.querySelector('[data-page-hero-canvas], [data-home-hero-canvas]');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const currentImage = preview.getAttribute('data-current-image') || '';
    const inputFile = document.querySelector('[data-page-hero-file], [data-home-hero-file]');
    const inputEnabled = document.querySelector('[data-page-hero-enabled], [data-home-hero-enabled]');
    const inputX = document.querySelector('[data-page-hero-x], [data-home-hero-x]');
    const inputY = document.querySelector('[data-page-hero-y], [data-home-hero-y]');
    const inputZoom = document.querySelector('[data-page-hero-zoom], [data-home-hero-zoom]');
    const inputCropLeft = document.querySelector('[data-page-hero-crop-left], [data-home-hero-crop-left]');
    const inputCropRight = document.querySelector('[data-page-hero-crop-right], [data-home-hero-crop-right]');
    const inputCropTop = document.querySelector('[data-page-hero-crop-top], [data-home-hero-crop-top]');
    const inputCropBottom = document.querySelector('[data-page-hero-crop-bottom], [data-home-hero-crop-bottom]');
    const inputOverlay = document.querySelector('[data-page-hero-overlay], [data-home-hero-overlay]');
    const inputBlur = document.querySelector('[data-page-hero-blur], [data-home-hero-blur]');
    const zoomLabel = document.querySelector('[data-page-hero-zoom-label], [data-home-hero-zoom-label]');
    const xLabel = document.querySelector('[data-page-hero-x-label], [data-home-hero-x-label]');
    const yLabel = document.querySelector('[data-page-hero-y-label], [data-home-hero-y-label]');
    const cropLeftLabel = document.querySelector('[data-page-hero-crop-left-label], [data-home-hero-crop-left-label]');
    const cropRightLabel = document.querySelector('[data-page-hero-crop-right-label], [data-home-hero-crop-right-label]');
    const cropTopLabel = document.querySelector('[data-page-hero-crop-top-label], [data-home-hero-crop-top-label]');
    const cropBottomLabel = document.querySelector('[data-page-hero-crop-bottom-label], [data-home-hero-crop-bottom-label]');
    const overlayLabel = document.querySelector('[data-page-hero-overlay-label], [data-home-hero-overlay-label]');
    const resetBtn = document.querySelector('[data-page-hero-reset], [data-home-hero-reset]');
    const pageSelector = document.querySelector('[data-page-hero-selector]');

    if (pageSelector) {
        pageSelector.addEventListener('change', () => {
            if (pageSelector.value) {
                window.location.href = pageSelector.value;
            }
        });
    }

    function normalizeCropRanges() {
        if (inputCropLeft && inputCropRight) {
            const left = Number(inputCropLeft.value || 0);
            const right = Number(inputCropRight.value || 0);
            if (left + right > 90) {
                inputCropRight.value = Math.max(0, 90 - left);
            }
        }
        if (inputCropTop && inputCropBottom) {
            const top = Number(inputCropTop.value || 0);
            const bottom = Number(inputCropBottom.value || 0);
            if (top + bottom > 90) {
                inputCropBottom.value = Math.max(0, 90 - top);
            }
        }
    }

    const loadedImage = new Image();
    let imageReady = false;

    loadedImage.onload = () => {
        imageReady = true;
        drawPreview();
    };
    loadedImage.onerror = () => {
        imageReady = false;
        drawPreview();
    };

    function drawFallback() {
        const w = canvas.width;
        const h = canvas.height;
        const grad = ctx.createLinearGradient(0, 0, w, h);
        grad.addColorStop(0, '#003f7f');
        grad.addColorStop(1, '#0a6ebd');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);
    }

    function drawPreview() {
        const enabled = inputEnabled && inputEnabled.checked;
        const x = Number(inputX ? inputX.value : 50);
        const y = Number(inputY ? inputY.value : 45);
        const zoomFactor = Number(inputZoom ? inputZoom.value : 1);
        const cropLeft = Number(inputCropLeft ? inputCropLeft.value : 0);
        const cropRight = Number(inputCropRight ? inputCropRight.value : 0);
        const cropTop = Number(inputCropTop ? inputCropTop.value : 0);
        const cropBottom = Number(inputCropBottom ? inputCropBottom.value : 0);
        const overlay = Number(inputOverlay ? inputOverlay.value : 0.45);
        const blurEnabled = !!(inputBlur && inputBlur.checked);

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawFallback();

        if (!enabled || !imageReady) return;

        const iw = loadedImage.naturalWidth;
        const ih = loadedImage.naturalHeight;

        const cx0 = Math.round(iw * (cropLeft / 100));
        const cx1 = Math.round(iw * (1 - (cropRight / 100)));
        const cy0 = Math.round(ih * (cropTop / 100));
        const cy1 = Math.round(ih * (1 - (cropBottom / 100)));
        const croppedW = Math.max(10, cx1 - cx0);
        const croppedH = Math.max(10, cy1 - cy0);

        const cW = canvas.width;
        const cH = canvas.height;
        const containScale = Math.min(cW / croppedW, cH / croppedH);
        const coverScale = Math.max(cW / croppedW, cH / croppedH);
        const scale = coverScale * Math.max(0.01, Math.min(10, zoomFactor));
        const drawW = Math.max(1, Math.round(croppedW * scale));
        const drawH = Math.max(1, Math.round(croppedH * scale));

        // Fondo blurred (cover) para permitir "alejar" sin espacios vacíos.
        const bgScale = coverScale;
        const bgW = Math.max(1, Math.round(croppedW * bgScale));
        const bgH = Math.max(1, Math.round(croppedH * bgScale));
        const bgX = Math.round((cW - bgW) / 2);
        const bgY = Math.round((cH - bgH) / 2);
        ctx.save();
        ctx.filter = 'blur(14px)';
        ctx.drawImage(loadedImage, cx0, cy0, croppedW, croppedH, bgX, bgY, bgW, bgH);
        ctx.restore();

        let drawX;
        let drawY;
        if (drawW > cW) {
            drawX = -Math.round((drawW - cW) * (x / 100));
        } else {
            drawX = Math.round((cW - drawW) / 2);
        }
        if (drawH > cH) {
            drawY = -Math.round((drawH - cH) * (y / 100));
        } else {
            drawY = Math.round((cH - drawH) / 2);
        }

        ctx.drawImage(loadedImage, cx0, cy0, croppedW, croppedH, drawX, drawY, drawW, drawH);
        if (blurEnabled) {
            const snapshot = ctx.getImageData(0, 0, cW, cH);
            ctx.clearRect(0, 0, cW, cH);
            ctx.save();
            ctx.filter = 'blur(8px)';
            const temp = document.createElement('canvas');
            temp.width = cW;
            temp.height = cH;
            const tctx = temp.getContext('2d');
            if (tctx) {
                tctx.putImageData(snapshot, 0, 0);
                ctx.drawImage(temp, 0, 0);
            }
            ctx.restore();
        }
        ctx.fillStyle = `rgba(0, 24, 52, ${Math.max(0, Math.min(0.9, overlay))})`;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function renderPreview(imageUrl) {
        normalizeCropRanges();
        const x = inputX ? inputX.value : '50';
        const y = inputY ? inputY.value : '45';
        const zoom = inputZoom ? inputZoom.value : '1';
        const cropLeft = inputCropLeft ? inputCropLeft.value : '0';
        const cropRight = inputCropRight ? inputCropRight.value : '0';
        const cropTop = inputCropTop ? inputCropTop.value : '0';
        const cropBottom = inputCropBottom ? inputCropBottom.value : '0';
        const overlay = inputOverlay ? inputOverlay.value : '0.45';

        if (zoomLabel) zoomLabel.textContent = Number(zoom).toFixed(2);
        if (xLabel) xLabel.textContent = x;
        if (yLabel) yLabel.textContent = y;
        if (cropLeftLabel) cropLeftLabel.textContent = cropLeft;
        if (cropRightLabel) cropRightLabel.textContent = cropRight;
        if (cropTopLabel) cropTopLabel.textContent = cropTop;
        if (cropBottomLabel) cropBottomLabel.textContent = cropBottom;
        if (overlayLabel) overlayLabel.textContent = overlay;

        if (imageUrl) {
            imageReady = false;
            loadedImage.src = imageUrl;
        } else {
            imageReady = false;
            drawPreview();
        }
    }

    let localImageUrl = currentImage;
    renderPreview(localImageUrl);

    if (inputFile) {
        inputFile.addEventListener('change', (e) => {
            const file = e.target.files && e.target.files[0];
            if (!file) {
                localImageUrl = currentImage;
                renderPreview(localImageUrl);
                return;
            }
            const reader = new FileReader();
            reader.onload = (ev) => {
                localImageUrl = ev.target && ev.target.result ? ev.target.result : currentImage;
                renderPreview(localImageUrl);
            };
            reader.readAsDataURL(file);
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            if (inputZoom) inputZoom.value = '1';
            if (inputX) inputX.value = '50';
            if (inputY) inputY.value = '45';
            if (inputCropLeft) inputCropLeft.value = '0';
            if (inputCropRight) inputCropRight.value = '0';
            if (inputCropTop) inputCropTop.value = '0';
            if (inputCropBottom) inputCropBottom.value = '0';
            if (inputOverlay) inputOverlay.value = '0.45';
            renderPreview(localImageUrl);
        });
    }

    [inputEnabled, inputX, inputY, inputZoom, inputCropLeft, inputCropRight, inputCropTop, inputCropBottom, inputOverlay, inputBlur].forEach((el) => {
        if (!el) return;
        const eventName = el.type === 'checkbox' ? 'change' : 'input';
        el.addEventListener(eventName, () => renderPreview(localImageUrl));
    });
}
