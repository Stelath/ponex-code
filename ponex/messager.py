from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
with open('keys.csv') as file:
    content = file.readlines()
    account_sid = content[0]
    auth_token = content[1]
client = Client(account_sid, auth_token)

def send_message_with_image(message, phone_number):
    message = client.messages \
                    .create(
                        body=message,
                        messaging_service_sid='MGd9ef1388a610b4ff8886808e30003f4',
                        to=phone_number
                    )
    print(message.sid)