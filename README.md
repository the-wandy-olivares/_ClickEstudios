## Descripción
Click es una aplicación diseñada para facilitar la gestión de tareas de estudios. Con una interfaz intuitiva y funcionalidades avanzadas, Click te ayuda a mantenerte organizado y productivo.

## Características
- Gestión de citas
- Recordatorios, notificaciones (Gmail)
- Integración con IA Gemini o GPT
- Flujo de control de caja

## Requisitos 
- Python 3.12.10
- Django 5.1.5
- Pip 25.0.1

## Instalacion

```bash
git clone https://github.com/the-wandy-olivares/Click.git
cd Click
python3.12.10 -m venv vn
. vn/bin/activate  # En Windows usa `env\Scripts\activate`
pip install -r requirements.txt
py manage.py migrate
py manage.py createsuperuser  # Obligatorio, para crear un usuario administrador

```
## Uso
Para iniciar la aplicación, ejecuta:

```bash
py manage.py runserver
```

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles

## Contacto
Para cualquier consulta o sugerencia, por favor contacta a [the.wandy.olivares@icloud.com]
