from twilio.rest import Client

account_sid = 'AC34177b5ffbdd2235561ae28ba3a08bd8'
auth_token = '1b9668ef64104bbf87f2be776ba6b307'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
  content_variables='{"1":"12/1","2":"3pm"}',
  to='whatsapp:+917020985029'
)

print(message.sid)