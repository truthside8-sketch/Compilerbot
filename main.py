import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.environ.get("TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🚀 Dehradun Coder Bot Ready!\n\n"
        "python print('hi')\n"
        "java System.out.println(2+2);\n"
        "html <h1>Hello</h1>\n"
        "css body{background:yellow}"
    )

def run_code(update: Update, context: CallbackContext):
    text = update.message.text
    try:
        lang, code = text.split(' ', 1)
        lang = lang.lower()

        if lang in ['html', 'css']:
            if lang == 'css':
                code = f"<html><style>{code}</style><body><h1>CSS Preview</h1><p>Ye CSS hai</p></body></html>"
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(code)
            update.message.reply_document(open("index.html", 'rb'), caption="HTML File")
            return

        piston_lang = "python" if lang == "python" else "java"
        url = "https://emkc.org/api/v2/piston/execute"
        payload = {"language": piston_lang, "version": "*", "files": [{"content": code}]}
        r = requests.post(url, json=payload, timeout=15)
        output = r.json()['run']['output'] or r.json()['run'].get('stderr','No output')
        update.message.reply_text(f"Output:\n\n{output}")

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, run_code))
updater.start_polling()
updater.idle()
