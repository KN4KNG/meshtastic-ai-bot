# Meshtastic AI Bot

This repository contains a script for a Meshtastic AI Bot that uses the Groq API to generate responses to received messages to a Meshtastic channel using a computer and usb (Serial Interface) to a Meshtastic Node.

## Requirements

- Python 3.x
- Meshtastic
- Groq API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/meshtastic-ai-bot.git
   cd meshtastic-ai-bot

2. Install the required packages:
   ```bash
   pip install meshtastic pubsub groq

3. Replace the placeholder API key in the script with your actual Groq API key.

4. Set the Channel Number to Operate on. (Direct Messages not supported yet.)

## Usage

Run the script:
   ```bash
   python meshtastic-ai-bot.py
   ```

The bot will listen for incoming messages and respond using the Groq API.

## License

This project is licensed under the MIT License.

