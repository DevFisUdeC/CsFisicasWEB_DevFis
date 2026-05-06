(() => {
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
                nodeSpacing: 36,
                rankSpacing: 46,
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
                fontSize: '15px',
            },
        });

        window.mermaid.run({
            nodes: [chart],
            suppressErrors: true,
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initOrgChart);
    } else {
        initOrgChart();
    }
})();
