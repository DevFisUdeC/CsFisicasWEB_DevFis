(() => {
    const state = {
        scale: 1,
        tx: 0,
        ty: 0,
        dragging: false,
        startX: 0,
        startY: 0,
    };

    function clamp(value, min, max) {
        return Math.min(max, Math.max(min, value));
    }

    function applyTransform(canvas) {
        canvas.style.transform = `translate(${state.tx}px, ${state.ty}px) translate(-50%, -50%) scale(${state.scale})`;
    }

    function fitToViewport(viewport, canvas) {
        const svg = canvas.querySelector('svg');
        if (!svg) return;

        const vpRect = viewport.getBoundingClientRect();
        const width = svg.viewBox?.baseVal?.width || svg.getBBox().width || 1300;
        const height = svg.viewBox?.baseVal?.height || svg.getBBox().height || 850;
        const fitScale = Math.min((vpRect.width * 0.9) / width, (vpRect.height * 0.9) / height);

        state.scale = clamp(fitScale, 0.45, 2.1);
        state.tx = 0;
        state.ty = 0;
        applyTransform(canvas);
    }

    function openModal() {
        const modal = document.getElementById('org-modal');
        const viewport = document.getElementById('org-modal-viewport');
        const canvas = document.getElementById('org-modal-canvas');
        const source = document.querySelector('#org-chart-embed svg');

        if (!modal || !viewport || !canvas || !source) return;

        canvas.innerHTML = source.outerHTML;
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        fitToViewport(viewport, canvas);
    }

    function closeModal() {
        const modal = document.getElementById('org-modal');
        if (!modal) return;
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    function bindModalControls() {
        const modal = document.getElementById('org-modal');
        const viewport = document.getElementById('org-modal-viewport');
        const canvas = document.getElementById('org-modal-canvas');
        const expandBtn = document.getElementById('org-expand-btn');
        const chartEmbed = document.getElementById('org-chart-embed');
        if (!modal || !viewport || !canvas || !expandBtn || !chartEmbed) return;

        const doZoom = (factor) => {
            state.scale = clamp(state.scale * factor, 0.35, 3.2);
            applyTransform(canvas);
        };

        expandBtn.addEventListener('click', openModal);
        chartEmbed.addEventListener('click', openModal);

        modal.addEventListener('click', (event) => {
            const target = event.target;
            if (!(target instanceof HTMLElement)) return;

            if (target.dataset.orgClose === 'true') {
                closeModal();
                return;
            }

            const zoomAction = target.dataset.orgZoom;
            if (zoomAction === 'in') doZoom(1.15);
            if (zoomAction === 'out') doZoom(1 / 1.15);
            if (zoomAction === 'reset') fitToViewport(viewport, canvas);
        });

        viewport.addEventListener('wheel', (event) => {
            event.preventDefault();
            doZoom(event.deltaY < 0 ? 1.08 : 1 / 1.08);
        }, { passive: false });

        viewport.addEventListener('pointerdown', (event) => {
            state.dragging = true;
            state.startX = event.clientX - state.tx;
            state.startY = event.clientY - state.ty;
            canvas.classList.add('is-dragging');
        });

        window.addEventListener('pointermove', (event) => {
            if (!state.dragging) return;
            state.tx = event.clientX - state.startX;
            state.ty = event.clientY - state.startY;
            applyTransform(canvas);
        });

        window.addEventListener('pointerup', () => {
            state.dragging = false;
            canvas.classList.remove('is-dragging');
        });

        window.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') closeModal();
        });

        window.addEventListener('resize', () => {
            if (modal.classList.contains('is-open')) {
                fitToViewport(viewport, canvas);
            }
        });
    }

    function initOrgChart() {
        const chart = document.getElementById('org-mermaid');
        if (!chart || typeof window.mermaid === 'undefined') {
            return;
        }

        window.mermaid.initialize({
            startOnLoad: false,
            securityLevel: 'strict',
            theme: 'base',
            flowchart: {
                curve: 'basis',
                nodeSpacing: 52,
                rankSpacing: 64,
                padding: 10,
                useMaxWidth: true,
            },
            themeVariables: {
                background: '#ffffff',
                primaryColor: '#003b7a',
                primaryTextColor: '#ffffff',
                primaryBorderColor: '#0a4f9e',
                lineColor: '#9bb3cf',
                secondaryColor: '#ffffff',
                tertiaryColor: '#f6f9fc',
                fontFamily: 'Inter, sans-serif',
                fontSize: '30px',
            },
        });

        window.mermaid.run({
            nodes: [chart],
            suppressErrors: true,
        }).then(() => {
            bindModalControls();
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initOrgChart);
    } else {
        initOrgChart();
    }
})();
