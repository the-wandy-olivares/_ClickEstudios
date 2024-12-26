from django.core.mail import send_mail
from django.conf import settings  # Importa settings
from django.core.mail import send_mail


def Send_Mail(email, name, plan, date, time):
    send_mail(
        'Notificacion de confirmación de cita',
        f'¡Guau! 🎉 {name} acabas de reservar una cita en ClickEstudios! 📅, ¡prepárate para brillar el {date} a las {time}!. '
        f'✨ Y eso no es todo... ¡ha elegido uno de nuestros mejores planes, el {plan}!  ¡Esto se va a poner genial! 🥳 ¡Felicidades, te esperamos. {name}!',
        'ClickEstudios <{}>'.format(settings.EMAIL_HOST_USER),  # Modificado aquí
        [email],
        fail_silently=False,
    )

  