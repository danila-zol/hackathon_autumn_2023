import json

if __name__ == "__main__":

    with open("src/telegram_bot/api_key.json") as f:
        api_key = json.load(f)["api_key"]