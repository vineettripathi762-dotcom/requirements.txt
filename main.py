import os
import telebot
from telebot import types
import google.generativeai as genai

# 🔑 यहाँ सीधे अपनी चाबियाँ डालें
TELEGRAM_TOKEN = '8632640696:AAHUgNS8qgWLZcrdYpB5ZTdEGlMAwVQfYj0E'
GEMINI_API_KEY = 'AQ.Ab8RN6IPNlsf8vzUhpwbcB7IGsVPi5tZSLS66zftMyeKNRiPfw'

genai.configure(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)
model = genai.GenerativeModel('gemini-pro')

# /start कमांड का स्वागत संदेश और मुख्य मेनू (Main Menu)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_ai = types.KeyboardButton('🤖 AI से पूछें (Ask AI)')
    btn_books = types.KeyboardButton('📚 पुस्तकें (Books)')
    btn_videos = types.KeyboardButton('🎥 वीडियो क्लासेज (Videos)')
    btn_grammar = types.KeyboardButton('✍️ व्याकरण (Grammar)')
    
    markup.add(btn_ai, btn_books, btn_videos, btn_grammar)
    
    welcome_text = (
        "👋 आपका स्वागत है शिक्षा AI बॉट में!\n\n"
        "यह बॉट संस्कृत, हिंदी, उर्दू और अंग्रेजी सहित सभी भाषाओं में आपकी मदद कर सकता है। "
        "नीचे दिए गए विकल्पों का चयन करें:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# बटन के अनुसार रिस्पॉन्स
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    chat_id = message.chat.id
    text = message.text

    if text == '🤖 AI से पूछें (Ask AI)':
        bot.send_message(chat_id, "💬 आप मुझसे संस्कृत, हिंदी, उर्दू या अंग्रेजी में कोई भी शैक्षणिक सवाल पूछ सकते हैं। अपना सवाल टाइप करके भेजें:")
        
    elif text == '📚 पुस्तकें (Books)':
        # पुस्तकों के लिए इनलाइन कीबोर्ड (Inline Buttons)
        inline_markup = types.InlineKeyboardMarkup()
        inline_markup.add(types.InlineKeyboardButton("संस्कृत व्याकरण पुस्तक", url="https://example.com"))
        inline_markup.add(types.InlineKeyboardButton("NCERT हिंदी पुस्तक", url="https://example.com"))
        inline_markup.add(types.InlineKeyboardButton("English Grammar Book", url="https://example.com"))
        
        bot.send_message(chat_id, "📖 यहाँ कुछ महत्वपूर्ण पुस्तकों की सूची दी गई है। डाउनलोड करने के लिए क्लिक करें:", reply_markup=inline_markup)

    elif text == '🎥 वीडियो क्लासेज (Videos)':
        inline_markup = types.InlineKeyboardMarkup()
        inline_markup.add(types.InlineKeyboardButton("संस्कृत सम्भाषण वीडियो", url="https://youtube.com"))
        inline_markup.add(types.InlineKeyboardButton("English Speaking Course", url="https://youtube.com"))
        
        bot.send_message(chat_id, "📺 वीडियो लेक्चर्स देखने के लिए नीचे दिए गए लिंक्स पर जाएं:", reply_markup=inline_markup)

    elif text == '✍️ व्याकरण (Grammar)':
        inline_markup = types.InlineKeyboardMarkup()
        inline_markup.add(types.InlineKeyboardButton("संस्कृत व्याकरण (संधि, कारक)", callback_data="g_sanskrit"))
        inline_markup.add(types.InlineKeyboardButton("हिंदी व्याकरण (समास, अलंकार)", callback_data="g_hindi"))
        inline_markup.add(types.InlineKeyboardButton("Urdu Grammar (क़वाइद)", callback_data="g_urdu"))
        inline_markup.add(types.InlineKeyboardButton("English Grammar (Tenses)", callback_data="g_english"))
        
        bot.send_message(chat_id, "✍️ किस भाषा का व्याकरण पढ़ना चाहते हैं? चुनें:", reply_markup=inline_markup)

    else:
        # अगर कोई सीधा सवाल पूछता है, तो AI मॉडल उसे प्रोसेस करेगा
        try:
            bot.send_chat_action(chat_id, 'typing')
            # AI को निर्देश देना कि वह शिक्षक की तरह व्यवहार करे
            prompt = f"You are an expert multilingual education assistant. Answer the following student query accurately in the language it is asked (especially supporting Sanskrit, Hindi, Urdu, and English): {text}"
            response = model.generate_content(prompt)
            bot.reply_to(message, response.text)
        except Exception as e:
            bot.reply_to(message, "⚠️ क्षमा करें, अभी AI सर्वर व्यस्त है। कृपया कुछ देर बाद प्रयास करें।")

# इनलाइन बटन (Callback Query) को हैंडल करना
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "g_sanskrit":
        bot.send_message(call.message.chat.id, "🕉️ **संस्कृत व्याकरण:**\n1. संधि प्रकरण\n2. शब्दरूप और धातुरूप\n3. कारक विभक्ति।")
    elif call.data == "g_hindi":
        bot.send_message(call.message.chat.id, "📖 **हिंदी व्याकरण:**\n1. संज्ञा, सर्वनाम, क्रिया\n2. समास और संधि\n3. रस, छंद, अलंकार।")
    elif call.data == "g_urdu":
        bot.send_message(call.message.chat.id, "✍️ **Urdu Grammar (क़वाइद):**\n1. Lafz aur Uske Bhed (लफ्ज़ और उसके भेद)\n2. Ism aur Sifat (इस्म और सिफ़त)\n3. Genders & Tenses.")
    elif call.data == "g_english":
        bot.send_message(call.message.chat.id, "🇬🇧 **English Grammar:**\n1. Parts of Speech\n2. Tenses & Voice\n3. Direct & Indirect Speech.")

# बॉट को चालू रखना
print("🤖 आपका शिक्षा AI बॉट सफलतापूर्वक लाइव हो गया है...")
bot.infinity_polling()
  
