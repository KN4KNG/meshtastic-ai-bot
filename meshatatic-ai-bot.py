import meshtastic.serial_interface
from pubsub import pub
import time
from groq import Groq
from groq.types.chat import ChatCompletionUserMessageParam, ChatCompletionSystemMessageParam
import math

# Replace with your Groq API key
API_KEY = 'YOUR_API_KEY_HERE'

# Initialize the Groq client
client = Groq(api_key=API_KEY)

# Specify the channel to send and receive messages on
CHANNEL_ID = 2  # Change this to the desired channel ID

interface = meshtastic.serial_interface.SerialInterface()

def onReceive(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            if 'channel' in packet and packet['channel'] == CHANNEL_ID:
                message_bytes = packet['decoded']['payload']
                message_string = message_bytes.decode('utf-8')
                print(f"Received on channel {CHANNEL_ID}: {message_string}")
                response_message = get_ai_response(message_string)
                send_message_in_chunks(response_message)
            else:
                print(f"Packet received on a different channel.")
    except KeyError as e:
        print(f"Error processing packet: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def get_ai_response(message):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            model="mixtral-8x7b-32768",
            max_tokens=50,
            temperature=0.7
        )
        response_text = chat_completion.choices[0].message.content.strip()
        return response_text
    except Exception as e:
        print(f"Error from API: {e}")
        return "Sorry, I couldn't generate a response."

def send_message_in_chunks(message):
    try:
        total_chunks = math.ceil(len(message) / 220)
        for i in range(total_chunks):
            chunk = message[i*220:(i+1)*220]
            msgcount = str(i + 1) + "/" + str(total_chunks) + " "
            interface.sendText(msgcount + chunk, channelIndex=CHANNEL_ID)
            print(f"Sent on channel {CHANNEL_ID}: {msgcount + chunk}")
            time.sleep(1)  # Add a short delay to avoid overwhelming the interface
    except Exception as e:
        print(f"Error sending message: {e}")

# Subscribe to receive messages
pub.subscribe(onReceive, 'meshtastic.receive')

# Keep the script running
while True:
    time.sleep(1)
