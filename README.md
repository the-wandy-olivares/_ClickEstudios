# Click

## Descripción
Click es una aplicación diseñada para facilitar la gestión de tareas de estudios. Con una interfaz intuitiva y funcionalidades avanzadas, Click te ayuda a mantenerte organizado y productivo.

## Características
- Gestión de citas
- Recordatorios, notificaciones (Gmail)
- Integración con IA Gemini o GPT
- Flujo de control de caja
## Instalación
Para instalar Click, sigue estos pasos:

```bash
git clone https://github.com/the-wandy-olivares/Click.git
cd Click
python3.12 -m venv vn
source env/bin/activate  # En Windows usa `env\Scripts\activate`
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # Obligatorio, para crear un usuario administrador

```
## Uso
Para iniciar la aplicación, ejecuta:

```bash
python manage.py runserver
```

## Contribuir
Si deseas contribuir al desarrollo de Click, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto
Para cualquier consulta o sugerencia, por favor contacta a [the.wandy.olivares@icloud.com].
