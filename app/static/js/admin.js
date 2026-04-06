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
    tag.innerHTML = `${text} <span class="tag-input__remove" title="Eliminar">&times;</span>`;

    tag.querySelector('.tag-input__remove').addEventListener('click', () => {
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
