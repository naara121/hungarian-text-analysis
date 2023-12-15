from datetime import datetime


class Logger:
    def log(self, level, message):
        text = f"[{level}] {datetime.now()}: {message}"

        with open("logs.txt", "a") as writer:
            writer.write(text + "\n")

        print(text)
