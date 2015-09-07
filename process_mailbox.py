from mailbox import mbox
import pandas as pd

def store_content(message, body=None):
    if not body:
        body = message.get_payload(decode=True)
    if len(message):
        contents = {
            "subject": message["subject"] or "",
            "body": body,
            "from": message["from"],
            "to": message["to"],
            "date": message["date"],
            "labels": message["X-Gmail-Labels"],
            "epilogue": message.epilogue,
        }
        return df.append(contents, ignore_index=True)

# Create empty DataFrame with relevant columns
df = pd.DataFrame(
    columns=("subject", "body", "from", "to", "date", "labels", "epilogue")
)

# Import downloaded mbox file
box = mbox("Takeout/Mail/All mail including Spam and Trash.mbox")

fails = []
for message in box:
    try:
        if message.get_content_type() == 'text/plain':
            df = store_content(message)
        elif message.is_multipart():
            # Grab any plaintext from multipart messages
            for part in message.get_payload():
                if part.get_content_type() == 'text/plain':
                    df = store_content(message, part.get_payload(decode=True))
                    break
    except:
        fails.append(message)
