"""
run.py — Entry point para el servidor de desarrollo Flask.
Responsabilidad: Iniciar la aplicación con la configuración correcta.
"""

from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
