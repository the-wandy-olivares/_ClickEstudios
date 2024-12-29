from django.core.mail import send_mail
from django.conf import settings  # Importa settings
from django.core.mail import send_mail
from django.db.models import Max
from . import models

def Send_Mail(email, name, plan, date, time):
    send_mail(
        'Notificacion de confirmación de cita',
        f'¡Guau! 🎉 {name} acabas de reservar una cita en ClickEstudios! 📅, ¡prepárate para brillar el {date} a las {time}!. '
        f'✨ Y eso no es todo... ¡ha elegido uno de nuestros mejores planes, el {plan}!  ¡Esto se va a poner genial! 🥳 ¡Felicidades, te esperamos. {name}!',
        'ClickEstudios <{}>'.format(settings.EMAIL_HOST_USER),  # Modificado aquí
        [email],
        fail_silently=False,
    )


def GetNCF(sale_type):
        """
        Genera el próximo NCF dependiendo del tipo de venta (credito o consumidor).
        """
        # Determinar el prefijo según el tipo de venta
        if sale_type == 'credito':
            last_nfc = models.Sale.objects.filter(sale_type='credito')
            prefix = 'B01'  # NCF para crédito
        else:
            last_nfc = models.Sale.objects.filter(sale_type='consumidor')
            prefix = 'B02'  # NCF 

        # Generar el siguiente número secuencial
        if last_nfc.exists():
            last_nfc_value = last_nfc.aggregate(Max('credito_fiscal'))['credito_fiscal__max']
            if last_nfc_value:
                # Extraer la parte numérica (asegurándonos de que la secuencia tenga el formato adecuado)
                sequence = int(last_nfc_value[3:])  # Extraemos la parte numérica, después de "B01" o "B02"
                next_sequence = sequence + 1
            else:
                next_sequence = 1  # Si no hay registros, empezar desde 1
        else:
            next_sequence = 1  # Si no hay registros, empezar desde 1

        # Formatear el NCF con el prefijo y la secuencia de 7 dígitos
        new_nfc = f"{prefix}{next_sequence:07d}"  # 7 dígitos en total, incluyendo el prefijo
        return new_nfc