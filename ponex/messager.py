from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
with open('keys.csv') as file:
    content = file.readlines()
    account_sid = content[0]
    auth_token = content[1]
client = Client(account_sid, auth_token)

def send_message_with_image(message, image_url, phone_number):
    message = client.messages \
                    .create(
                        media_url=image_url,
                        body=message,
                        from_='+18644005538',
                        to=phone_number
                    )
    print(message.sid)