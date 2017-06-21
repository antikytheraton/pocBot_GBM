# coding: utf-8
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import json
from example.config import CONFIG
from fbmq import Attachment, Template, QuickReply, NotificationType
from example.fbpage import page

USER_SEQ = {}


@page.handle_optin
def received_authentication(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_auth = event.timestamp

    pass_through_param = event.optin.get("ref")

    print("Received authentication for user %s and page %s with pass "
          "through param '%s' at %s" % (sender_id, recipient_id, pass_through_param, time_of_auth))

    page.send(sender_id, "Authentication successful")


@page.handle_echo
def received_echo(event):
    message = event.message
    message_id = message.get("mid")
    app_id = message.get("app_id")
    metadata = message.get("metadata")
    print("page id : %s , %s" % (page.page_id, page.page_name))
    print("Received echo for message %s and app %s with metadata %s" % (message_id, app_id, metadata))


@page.handle_message
def received_message(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_message = event.timestamp
    message = event.message
    print("Received message for user %s and page %s at %s with message:"
          % (sender_id, recipient_id, time_of_message))
    print(message)

    seq = message.get("seq", 0)
    message_id = message.get("mid")
    app_id = message.get("app_id")
    metadata = message.get("metadata")

    message_text = message.get("text")
    message_attachments = message.get("attachments")
    quick_reply = message.get("quick_reply")

    seq_id = sender_id + ':' + recipient_id
    if USER_SEQ.get(seq_id, -1) >= seq:
        print("Ignore duplicated request")
        return None
    else:
        USER_SEQ[seq_id] = seq

    if quick_reply:
        quick_reply_payload = quick_reply.get('payload')
        print('-------------------------quick_replies----------------------------------------')
        print("quick reply for message %s with payload %s" % (message_id, quick_reply_payload))

        if quick_reply_payload == 'CONOCER_PERFIL':
            page.send(sender_id, 'Claro, solo necesito que me ayudes a responder algunas preguntas, las preguntas son de opción múltiple y sólo puedes seleccionar una respuesta')
            page.send(sender_id, 'Hablando sobre tu interés por invertir ¿Cuál es tu principal meta?')
            page.send(sender_id, Template.Generic([
                Template.GenericElement("Mantener el valor de la inversión.",
                                        subtitle="Minimizar el riesgo de mi inversión.",
                                        # item_url="https://www.oculus.com/en-us/rift/",
                                        image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                                        buttons=[
                                            Template.ButtonPostBack("seleccionar", "META")
                                        ]),
                Template.GenericElement("Acrecentar el valor de mi inversión.",
                                        subtitle="Acrecentar el valor de mi inversión.",
                                        # item_url="https://www.oculus.com/en-us/touch/",
                                        image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                                        buttons=[
                                            Template.ButtonPostBack("seleccionar", "META")
                                        ]),
                Template.GenericElement("Crecer sustancialmente mi inversión.",
                                        subtitle="Quiero beneficios a corto plazo.",
                                        # item_url="https://www.oculus.com/en-us/touch/",
                                        image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                                        buttons=[
                                            Template.ButtonPostBack("seleccionar", "META")
                                        ])
                ]))
            # print(CONFIG['SERVER_URL'] + "/assets/meta_2.jpg")
        elif quick_reply_payload == 'INVERSION_RENTA_SI':
            page.send(sender_id, "¿A qué plazo?",
              quick_replies=[QuickReply(title="De 1 - 3 años", payload="INVERSION_RENTA"),
                             QuickReply(title="De 3 - 7 años", payload="INVERSION_RENTA"),
                             QuickReply(title="De 7 o más años", payload="INVERSION_RENTA")],
              metadata="DEVELOPER_DEFINED_METADATA")

        elif quick_reply_payload == 'INVERSION_RENTA':
            page.send(sender_id, "¿Has invertido en sociedades de inversión de renta variable?",
              quick_replies=[QuickReply(title="Si", payload="PLAZO_SI"),
                             QuickReply(title="No", payload="MERCADO_DINERO")],
              metadata="DEVELOPER_DEFINED_METADATA")
        
        elif quick_reply_payload == 'PLAZO_SI':
            page.send(sender_id, "¿A qué plazo?",
              quick_replies=[QuickReply(title="De 1 - 3 años", payload="MERCADO_DINERO"),
                             QuickReply(title="De 3 - 7 años", payload="MERCADO_DINERO"),
                             QuickReply(title="De 7 o más años", payload="MERCADO_DINERO")],
              metadata="DEVELOPER_DEFINED_METADATA")
        
        elif quick_reply_payload == 'MERCADO_DINERO':
            page.send(sender_id, "¿Has invertido en Mercado de Dinero?",
                quick_replies=[QuickReply(title="Si", payload="MERCADO_CAPITALES_SI"),
                               QuickReply(title="No", payload="MERCADO_CAPITALES")],
                metadata='DEVELOPER_DEFINED_METADATA')

        elif quick_reply_payload == 'MERCADO_CAPITALES_SI':
            page.send(sender_id, "¿A qué plazo?",
              quick_replies=[QuickReply(title="De 1 - 3 años", payload="MERCADO_CAPITALES"),
                             QuickReply(title="De 3 - 7 años", payload="MERCADO_CAPITALES"),
                             QuickReply(title="De 7 o más años", payload="MERCADO_CAPITALES")],
              metadata="DEVELOPER_DEFINED_METADATA")
        
        elif quick_reply_payload == 'MERCADO_CAPITALES':
            page.send(sender_id, "¿Has invertido en Mercado de Dinero?",
                quick_replies=[QuickReply(title="Si", payload="MERCADO_DERIVADOS_SI"),
                               QuickReply(title="No", payload="MERCADO_DERIVADOS")],
                metadata='DEVELOPER_DEFINED_METADATA')

        elif quick_reply_payload == 'MERCADO_CAPITALES_SI':
            page.send(sender_id, "¿A qué plazo?",
              quick_replies=[QuickReply(title="De 1 - 3 años", payload="MERCADO_DERIVADOS"),
                             QuickReply(title="De 3 - 7 años", payload="MERCADO_DERIVADOS"),
                             QuickReply(title="De 7 o más años", payload="MERCADO_DERIVADOS")],
              metadata="DEVELOPER_DEFINED_METADATA")
        
        elif quick_reply_payload == 'MERCADO_DERIVADOS':
            page.send(sender_id, "¿Has invertido en Mercado de Dinero?",
                quick_replies=[QuickReply(title="Si", payload="lol"),
                               QuickReply(title="No", payload="lol")],
                metadata='DEVELOPER_DEFINED_METADATA')

        
        else:
            page.send(sender_id, "Quick reply tapped")

    # if message_text:
    #     send_message(sender_id, message_text)

    # elif message_attachments:
    if message_attachments:
        page.send(sender_id, "Message with attachment received")


@page.handle_delivery
def received_delivery_confirmation(event):
    delivery = event.delivery
    message_ids = delivery.get("mids")
    watermark = delivery.get("watermark")

    if message_ids:
        for message_id in message_ids:
            print("Received delivery confirmation for message ID: %s" % message_id)

    print("All message before %s were delivered." % watermark)


@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp

    payload = event.postback_payload
    
    print('-------------------------postback_payload----------------------------------------')
    print(payload)
    print("Received postback for user %s and page %s with payload '%s' at %s"
          % (sender_id, recipient_id, payload, time_of_postback))


    if payload == 'INIT_USERBOT':
        text = "Hola. En que te puedo ayudar?"
        page.send(sender_id, text,
                        quick_replies=[{'title': 'Mi perfil', 'payload': 'CONOCER_PERFIL'} ],
                        metadata="DEVELOPER_DEFINED_METADATA")

    elif payload == 'META':
        page.send(sender_id, "Hablemos de riesgo")
        page.send(sender_id, "¿Con que nivel de riesgo crees que te sentirías más cómodo?")
        # page.send(sender_id, "Antes de responder recuerda que el grado en el que el valor de la inversión aumenta o disminuye depende del nivel de riesgo que asuma.")
        # page.send(sender_id, "Inversiones con mayor riesgo generalmente ofrecen más crecimiento a largo plazo que aquellas con menos riesgo, pero pueden producir mayor volatilidad.")
        page.send(sender_id, Template.Generic([
            Template.GenericElement("Con el menor posible",
                subtitle="Enfocarse en estabilidad.",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "RIESGO")]),
            Template.GenericElement("Moderado",
                subtitle="Estoy dispuesto a asumir un riesgos.",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "RIESGO")]),
            Template.GenericElement("Un porcentage considerable",
                subtitle="Deseo asumir un riesgo alto.",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "RIESGO")])
            ]))

    elif payload == 'RIESGO':
        page.send(sender_id, "Para asegurar tu rendimiento, tu inversión se divide en diferentes instrumentos.")
        page.send(sender_id, "Al conjunto de estos instrumentos se le llama portafolio")
        page.send(sender_id, "Seleccione uno de los cinco escenarios posibles:")
        page.send(sender_id, Template.Generic([
            Template.GenericElement("100%  en la inversión x y 0%  en la inversión Y. ",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "PORTAFOLIO")]),
            Template.GenericElement("80%  en la Inversión X y 20%  en la Inversión Y.",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "PORTAFOLIO")]),
            Template.GenericElement("50%  en la Inversión X y 50%  en la Inversión Y. ",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "PORTAFOLIO")]),
            Template.GenericElement("20%  en la Inversión X y 80%  en la Inversión Y ",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "PORTAFOLIO")]),
            Template.GenericElement("0%  en la Inversión X y 100%  en la Inversión Y ",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "PORTAFOLIO")])
            ]))

    elif payload == 'PORTAFOLIO':
        page.send(sender_id, "Te mostrare unas gráficas con diferentes portafolios de inversión y sus rendimientos.")
        page.send(sender_id, "Debes elegir la opción con la que te sientas más cómodo, tómate tu tiempo")
        page.send(sender_id, Template.Generic([
            Template.GenericElement("Portafolio A",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "BENEFICIOS")]),
            Template.GenericElement("Portafolio B",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "BENEFICIOS")]),
            Template.GenericElement("Portafolio C",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "BENEFICIOS")]),
            Template.GenericElement("Portafolio D",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "BENEFICIOS")])
            ]))

    elif payload == 'BENEFICIOS':
        page.send(sender_id, "Excelente, ahora hablemos de los beneficios")
        page.send(sender_id, "¿En qué tiempo consideras que necesitarás toda o una parte de tu inversión?")
        page.send(sender_id, Template.Generic([
            Template.GenericElement("Corto plazo",
                subtitle="0 a 2 años",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "INVERSION_DEUDA")]),
            Template.GenericElement("Mediano plazo",
                subtitle="Más de 2 años, pero menos de 5 años",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "INVERSION_DEUDA")]),
            Template.GenericElement("Largo plazo",
                subtitle="5 años o más",
                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                buttons=[
                    Template.ButtonPostBack("seleccionar", "INVERSION_DEUDA")])
            ]))
    elif payload == 'INVERSION_DEUDA':
        page.send(sender_id, "Queremos saber si has invertido antes y en qué instrumentos")
        page.send(sender_id, "¿Has invertido en sociedades de inversión de deuda?",
              quick_replies=[QuickReply(title="Si", payload="INVERSION_RENTA_SI"),
                             QuickReply(title="No", payload="INVERSION_RENTA")],
              metadata="DEVELOPER_DEFINED_METADATA")

    else:
        page.send(sender_id, "Postback called")



@page.handle_read
def received_message_read(event):
    watermark = event.read.get("watermark")
    seq = event.read.get("seq")

    print("Received message read event for watermark %s and sequence number %s" % (watermark, seq))


@page.handle_account_linking
def received_account_link(event):
    sender_id = event.sender_id
    status = event.account_linking.get("status")
    auth_code = event.account_linking.get("authorization_code")

    print("Received account link event with for user %s with status %s and auth code %s "
          % (sender_id, status, auth_code))


def send_message(recipient_id, text):
    # If we receive a text message, check to see if it matches any special
    # keywords and send back the corresponding example. Otherwise, just echo
    # the text we received.
    special_keywords = {
        "image": send_image,
        "gif": send_gif,
        "audio": send_audio,
        "video": send_video,
        "file": send_file,
        "button": send_button,
        "generic": send_generic,
        "receipt": send_receipt,
        "quick reply": send_quick_reply,
        "read receipt": send_read_receipt,
        "typing on": send_typing_on,
        "typing off": send_typing_off,
        "account linking": send_account_linking
    }

    if text in special_keywords:
        special_keywords[text](recipient_id)
    else:
        page.send(recipient_id, text, callback=send_text_callback, notification_type=NotificationType.REGULAR)


def send_text_callback(payload, response):
    print("SEND CALLBACK")


def send_image(recipient):
    page.send(recipient, Attachment.Image(CONFIG['SERVER_URL'] + "/assets/rift.png"))


def send_gif(recipient):
    page.send(recipient, Attachment.Image(CONFIG['SERVER_URL'] + "/assets/instagram_logo.gif"))


def send_audio(recipient):
    page.send(recipient, Attachment.Audio(CONFIG['SERVER_URL'] + "/assets/sample.mp3"))


def send_video(recipient):
    page.send(recipient, Attachment.Video(CONFIG['SERVER_URL'] + "/assets/allofus480.mov"))


def send_file(recipient):
    page.send(recipient, Attachment.File(CONFIG['SERVER_URL'] + "/assets/test.txt"))


def send_button(recipient):
    """
    Shortcuts are supported
    page.send(recipient, Template.Buttons("hello", [
        {'type': 'web_url', 'title': 'Open Web URL', 'value': 'https://www.oculus.com/en-us/rift/'},
        {'type': 'postback', 'title': 'tigger Postback', 'value': 'DEVELOPED_DEFINED_PAYLOAD'},
        {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+16505551234'},
    ]))
    """
    page.send(recipient, Template.Buttons("hello", [
        Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
        Template.ButtonPostBack("trigger Postback", "DEVELOPED_DEFINED_PAYLOAD"),
        Template.ButtonPhoneNumber("Call Phone Number", "+16505551234")
    ]))


@page.callback(['DEVELOPED_DEFINED_PAYLOAD'])
def callback_clicked_button(payload, event):
    print(payload, event)


def send_generic(recipient):
    page.send(recipient, Template.Generic([
        Template.GenericElement("rift",
                                subtitle="Next-generation virtual reality",
                                item_url="https://www.oculus.com/en-us/rift/",
                                image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                                buttons=[
                                    Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
                                    Template.ButtonPostBack("tigger Postback", "DEVELOPED_DEFINED_PAYLOAD"),
                                    Template.ButtonPhoneNumber("Call Phone Number", "+16505551234")
                                ]),
        Template.GenericElement("touch",
                                subtitle="Your Hands, Now in VR",
                                item_url="https://www.oculus.com/en-us/touch/",
                                image_url=CONFIG['SERVER_URL'] + "/assets/touch.png",
                                buttons=[
                                    {'type': 'web_url', 'title': 'Open Web URL',
                                     'value': 'https://www.oculus.com/en-us/rift/'},
                                    {'type': 'postback', 'title': 'tigger Postback',
                                     'value': 'DEVELOPED_DEFINED_PAYLOAD'},
                                    {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+16505551234'},
                                ])
    ]))


def send_receipt(recipient):
    receipt_id = "order1357"
    element = Template.ReceiptElement(title="Oculus Rift",
                                      subtitle="Includes: headset, sensor, remote",
                                      quantity=1,
                                      price=599.00,
                                      currency="USD",
                                      image_url=CONFIG['SERVER_URL'] + "/assets/riftsq.png"
                                      )

    address = Template.ReceiptAddress(street_1="1 Hacker Way",
                                      street_2="",
                                      city="Menlo Park",
                                      postal_code="94025",
                                      state="CA",
                                      country="US")

    summary = Template.ReceiptSummary(subtotal=698.99,
                                      shipping_cost=20.00,
                                      total_tax=57.67,
                                      total_cost=626.66)

    adjustment = Template.ReceiptAdjustment(name="New Customer Discount", amount=-50)

    page.send(recipient, Template.Receipt(recipient_name='Peter Chang',
                                          order_number=receipt_id,
                                          currency='USD',
                                          payment_method='Visa 1234',
                                          timestamp="1428444852",
                                          elements=[element],
                                          address=address,
                                          summary=summary,
                                          adjustments=[adjustment]))


def send_quick_reply(recipient):
    """
    shortcuts are supported
    page.send(recipient, "What's your favorite movie genre?",
                quick_replies=[{'title': 'Action', 'payload': 'PICK_ACTION'},
                               {'title': 'Comedy', 'payload': 'PICK_COMEDY'}, ],
                metadata="DEVELOPER_DEFINED_METADATA")
    """
    page.send(recipient, "What's your favorite movie genre?",
              quick_replies=[QuickReply(title="Action", payload="PICK_ACTION"),
                             QuickReply(title="Comedy", payload="PICK_COMEDY")],
              metadata="DEVELOPER_DEFINED_METADATA")


@page.callback(['PICK_ACTION'])
def callback_picked_genre(payload, event):
    print(payload, event)


def send_read_receipt(recipient):
    page.mark_seen(recipient)


def send_typing_on(recipient):
    page.typing_on(recipient)


def send_typing_off(recipient):
    page.typing_off(recipient)


def send_account_linking(recipient):
    page.send(recipient, Template.AccountLink(text="Welcome. Link your account.",
                                              account_link_url=CONFIG['SERVER_URL'] + "/authorize",
                                              account_unlink_button=True))


def send_text_message(recipient, text):
    page.send(recipient, text, metadata="DEVELOPER_DEFINED_METADATA")
