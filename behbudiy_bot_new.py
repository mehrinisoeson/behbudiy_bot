#!/usr/bin/env python3
"""
Mahmudxo'ja Behbudiy nomidagi Telegram Bot
Stipendiya loyihasi uchun yaratilgan
Yangilangan: Yurisprudensiya bo'limi + Har kuni soat 9:00 da notification
"""

import logging
import random
import json
import os
from datetime import time as dt_time
import pytz

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    JobQueue,
)

# ── Token & sozlamalar ─────────────────────────────────────────────────────────
BOT_TOKEN   = "8734900557:AAFiniFbRysdia8OaQNt5oip1-iR67nGQ6g"   # @BotFather dan oling
TIMEZONE    = pytz.timezone("Asia/Tashkent")
NOTIF_HOUR  = 9    # soat 9:00
NOTIF_MIN   = 0
SUBS_FILE   = "subscribers.json"         # obunachi ID larni saqlash

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
#  OBUNACHI BOSHQARUV
# ══════════════════════════════════════════════════════════════════════════════

def load_subscribers() -> set:
    if os.path.exists(SUBS_FILE):
        with open(SUBS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_subscribers(subs: set):
    with open(SUBS_FILE, "w") as f:
        json.dump(list(subs), f)


# ══════════════════════════════════════════════════════════════════════════════
#  MA'LUMOTLAR BAZASI
# ══════════════════════════════════════════════════════════════════════════════

BEHBUDIY_INFO = {
    "hayot": """
📜 *Mahmudxo'ja Behbudiy (1875–1919)*

Mahmudxo'ja Behbudiy — Turkiston jadidchilik harakatining asoschisi, buyuk ma'rifatparvar, dramaturg, publitsist va huquqiy islohot tarafdori.

━━━━━━━━━━━━━━━━━━
*Tug'ilishi va yoshligi*
━━━━━━━━━━━━━━━━━━
1875-yilda Samarqand viloyatining Baxshitepa qishlog'ida (hozirgi Qo'shrabot tumani) ruhoniy oilasida tavallud topdi. Otasi Behbudxo'ja Solihxo'ja o'g'li — imom va mudarris. Ilk ta'limni otasidan va mahalliy maktabda oldi, so'ngra Buxorodda islom fanlari bo'yicha chuqur ta'lim oldi.

━━━━━━━━━━━━━━━━━━
🌍 *Sayohatlari va dunyoqarashining shakllanishi*
━━━━━━━━━━━━━━━━━━
• 1899–1900 — Buxoro, Eron va Hindistonga ilmiy safar
• 1900 — Usmonli Turkiyasi va Misrga bordi; u yerda zamonaviy maktablar, matbuot va huquqiy islohotlar bilan tanishdi
• 1903 — Makkaga haj safari; Qohira orqali qaytib, G'arb va Sharq madaniyatini o'rgandi
• 1904 — Rossiya shaharlari (Moskva, Sankt-Peterburg) va 1906-yil Qozon, Boku, Tiflisga sayohat

Bu sayohatlar Behbudiyning jadidchilik g'oyalarini shakllantirishda hal qiluvchi rol o'ynadi.

━━━━━━━━━━━━━━━━━━
✍️ *Ijodiy va ma'rifiy faoliyati*
━━━━━━━━━━━━━━━━━━
• 1904 — "Muxtasar tarixi islom" kitobini yozdi
• 1905 — "Kitobat ul-atfol" — yangi usul maktablari uchun alifbo darsligi
• 1906 — "Samarqand" gazetasida muharrir sifatida faoliyat boshladi
• 1907 — Samarqandda yangi usul maktabini tashkil etdi
• 1913 — "Padarkush" dramasini yozdi — O'rta Osiyodagi birinchi milliy drama!
• 1913 — "Ehtiyoji millat", "Ikki emas, to'rt til lozim" kabi mashhur maqolalarini yozdi
• 1914 — "Oyina" (Ko'zgu) jurnalini asos soldi; muharrir va bosh yozuvchi sifatida ishladi
• 1915 — "Oyina" 68-son chiqargandan so'ng Rossiya ma'murlari tomonidan yopildi
• 1917 — Turkiston Muxtoriyatini qo'llab-quvvatladi
• 1918 — "Haq olinur, berilmas!" maqolasini yozdi

━━━━━━━━━━━━━━━━━━
⚖️ *Siyosiy va huquqiy faoliyati*
━━━━━━━━━━━━━━━━━━
Behbudiy Rossiya imperiyasi Davlat Dumasida Turkiston manfaatlarini himoya qilish uchun mahalliy huquqshunoslar tayyorlash zarurligini ta'kidladi. Milliy muxtoriyat va qonun ustuvorligi g'oyalarini targ'ib qildi. 1917-yil inqilobidan so'ng Turkiston Muxtoriyati (Qo'qon Muxtoriyati) tashkilotchilari bilan hamkorlik qildi.

━━━━━━━━━━━━━━━━━━
*Vafoti*
━━━━━━━━━━━━━━━━━━
1919-yil mart oyida Buxoro amirligi hududi, Shahrisabzda qo'lga olinadi va Qarshi shahrida maxfiy ravishda qatl etildi. Behbudiyning haqiqiy qotillari kim bo'lganligi(Buxoro amiri yoki Turkistondagi Sovet hokimiyati) haligacha oydinlashmagan...

━━━━━━━━━━━━━━━━━━
🏛 *Merosi*
━━━━━━━━━━━━━━━━━━
Behbudiy O'zbekiston Respublikasida milliy qahramon sifatida e'tirof etilgan. Samarqandda uning nomidagi ko'cha, maktab va teatr mavjud. O'zbekiston Xalqaro Islomshunoslik Akademiyasi uning nomidagi maxsus stipendiyani ta'sis etgan.
""",
    "asarlar": """
📚 *Behbudiyning asosiy asarlari:*

🎭 *Dramaturgiya:*
• "Padarkush" (1911) — Turkistondagi birinchi milliy drama

📰 *Jurnalistika va publitsistika:*
• "Oyina" jurnali (1914–1915)
• "Samarqand" gazetasi
• "Hurriyat" gazetasi

📖 *Ilmiy va ta'limiy asarlar:*
• "Muxtasar tarixi islom" (1904)
• "Kitobat ul-atfol" (darslik, 1905)
• "Amaliyot ul-islom" (1903)

🌍 *Sayohatnomalar:*
• Hindiston, Turkiya, Misr bo'ylab sayohat taassurotlari
""",
    "goyalar": """
💡 *Behbudiyning asosiy g'oyalari:*

📚 *Ta'lim islohotlari:*
"Ikki til bilgan ikki insondir" — yangi usul maktablarini tashkil etdi

🤝 *Milliy birlik:*
Turkiston xalqlarini birlashtirish va uyg'otish uchun kurashdi

✍️ *Matbuot erkinligi:*
Milliy matbuot orqali xalqni ma'rifatga chorladi

🎭 *San'at va drama:*
"Padarkush" asari orqali jamiyatdagi illatlarni fosh etdi

⚖️ *Huquq va qonun:*
Millat uchun yuristlar tayyorlash, qonunchilikni o'rganish zarurligini ilk bor bayon etdi
""",
    "padarkush": """
🎭 *"Padarkush" dramasi haqida:*

📅 Yozilgan yil: 1911
Bosib chiqarilgan:1913
📌 Ahamiyati: O'rta Osiyodagi *birinchi milliy drama*

📖 *Syujet:*
Asarda Toshmurod ismli yigit o'qish o'rniga dangasalik, ichkilik va qimorbozlik bilan shug'ullanadi. Oxir-oqibat otasining o'limiga sabab bo'ladi — "padarkush" bo'ladi.

💬 *Muallif maqsadi:*
Asarning epigrafida: *"Ko'zing ko'radigan ko'r, qulog'ing eshitadigan kar bo'lma!"*

🎯 *Asosiy g'oya:*
Jaholatning fojiali oqibatlarini ko'rsatish orqali ta'lim va ma'rifatga chorlash.

🏛 *Tarixiy ahamiyati:*
Bu drama Turkiston teatr san'atining boshlanish nuqtasi hisoblanadi.
""",
}

IQTIBOSLAR = [
    ("Ey musulmonlar! Uyg'oning, maktab oching, o'qing, o'qiting!", "Behbudiyning nutqidan"),
    ("Bizning yoqimiz — ilm va ma'rifat.", "Oyina jurnalidan"),
    ("Millat farzandlarini tarbiyalash — kelajakni qurmoqdir.", "Mahmudxo'ja Behbudiy"),
    ("Ona tili — millatning ruhi.", "Behbudiyning maqolasidan"),
    ("Ilmsiz xalq — yetim xalq.", "Mahmudxo'ja Behbudiy"),
    ("Yangi usul maktablarsiz millat taraqqiyot ko'rmaydi.", "Behbudiyning maqolasidan"),
]

# ══════════════════════════════════════════════════════════════════════════════
#  ⚖️  YURISPRUDENSIYA — Behbudiy maqolalaridan huquqiy parchalar
# ══════════════════════════════════════════════════════════════════════════════

HUQUQ_MAQOLALAR = [
    {
        "sarlavha": "Yurist — zamonning faqihi",
        "matn": (
            "To'rt sana dorulfunun o'qub, andan huquqshunos, yurist — ta'bir joiz bo'lsa, "
            "zamona faqihi bo'lib chiqar. Sud mahkamalarinda, davlat doiralarinda kirib, "
            "har huquqshunos o'z muvakkili va o'z millati, o'z toifasi, o'z Vatani va "
            "o'z davlatining nafyiga so'ylashur, mudofaa qilur."
        ),
        "manba": "«Ehtiyoji millat» — «Samarqand» gazetasi, 1913 yil 12 iyul",
        "izoh": "🔍 Behbudiy yuristni millatning himoyachisi sifatida ta'riflagan. "
                "Bu bugungi huquqshunoslik etikasining asosini tashkil etadi.",
    },
    {
        "sarlavha": "Qonunni bilmaslik — millat zaifligining sababi",
        "matn": (
            "Endi zamon o'zgarib, boshqa millatlar ila mahlu bo'lduk, "
            "shariat va o'rf-odatimiz ustiga qonun va Ovrupa odatiga itoat qilmoqqa majburmiz. "
            "Ammo qonun va Ovrupa odatlarini bilmaganimiz uchun boyimiz bo'lsun, qozi va milliy "
            "hukamomiz va aholimiz bo'lsun — ko'b tashvish va zarar ko'rar. "
            "Zamoni sobiqda faqat shariat bilmoq kifoya etardi. Endi qonun va qonunni bilmoq ham lozimdir."
        ),
        "manba": "«Ehtiyoji millat» — «Samarqand» gazetasi, 1913 yil 12 iyul",
        "izoh": "⚡ Huquqiy savodxonlikning millat uchun naqadar zarurligini Behbudiy aniq ko'rsatgan. "
                "Bu fikr 110 yil o'tib ham o'z ahamiyatini yo'qotmagan.",
    },
    {
        "sarlavha": "Mudofaasiz millat",
        "matn": (
            "Davlat dumasi nari tursun, sudga va rasmiy mahkamalarga kirib, "
            "bizni mudofaa qiladurgon kishimiz yo'q."
        ),
        "manba": "«Ehtiyoji millat» — «Samarqand» gazetasi, 1913 yil 12 iyul",
        "izoh": "⚠️ Millat o'z huquqshunosi bo'lmasa, o'z manfaatini hech qayerda himoya eta olmaydi. "
                "Bu jumla bugun ham dolzarb.",
    },
    {
        "sarlavha": "Parlament vakili — huquqshunos bo'lmog'i shart",
        "matn": (
            "Davlat dumasinda biz Turkiston musulmonlaridan shunday huquqshunos vakil bo'lsa, "
            "bizni din va millatimiz nafyiga harakat qilur. Ammo shunday odam bizda yo'q."
        ),
        "manba": "«Ehtiyoji millat» — «Samarqand» gazetasi, 1913 yil 12 iyul",
        "izoh": "🏛 Behbudiy parlament vakilini huquqshunos bo'lishi kerakligini ta'kidlagan. "
                "Bu bugungi konstitutsionalizm nazariyasiga mos keluvchi ilg'or fikrdir.",
    },
    {
        "sarlavha": "Zamonu qonundan xabardor bo'lish",
        "matn": (
            "Anda borib nafyi uchun o'n sana o'qumoq kerak, "
            "zamоndan, qonundan xabardor bo'lmoq kerakdur."
        ),
        "manba": "«Ikki emas, to'rt til lozim» — «Oyina» jurnali, 1913 yil, 1-son",
        "izoh": "📖 Huquqiy bilim — doimiy ta'lim va izlanish natijasidir. "
                "Behbudiy bu haqiqatni asrimiz boshida bayon etgan.",
    },
    {
        "sarlavha": "Haq olinur, berilmas!",
        "matn": (
            "Bilingki, haq olinur, berilmas. Inchunin, muxtoriyat ham olinur, berilmas. "
            "Ya'ni muxtoriyatni Turkiston bolalarining o'zi birlashib, g'ayrat ila olurlar. "
            "Albatta, boshqalar tarafidan berilmas."
        ),
        "manba": "«Haq olinur, berilmas!» — «Hurriyat» gazetasi, 1918 yil, 26 yanvar",
        "izoh": "✊ Huquqlarni talab qilish — fuqarolik burchi. "
                "Behbudiyning bu fikri zamonaviy huquq falsafasining asosiy poydevorlaridan biridir.",
    },
    {
        "sarlavha": "Har xalqqa o'z qonuni — huquqiy plyuralizm",
        "matn": (
            "Sizlar turgun xalq ila birlashib muxtoriyat qilganda, "
            "siz ila turgun xalq uchun birgina nav' qonun bo'lmay, "
            "balki sizning tirikchilik va odatingizga muvofiq alohida siz uchun "
            "naf'lik qonunlar yozilur. Har bir xalqning odat va mazhabiga rioya qilinur."
        ),
        "manba": "«Haq olinur, berilmas!» — «Hurriyat» gazetasi, 1918 yil, 26 yanvar",
        "izoh": "🌐 Bu — zamonaviy qiyosiy huquqshunoslik va milliy huquq konsepsiyasining "
                "Behbudiy tomonidan ilk bora bayon etilishi. Plyuralizm va huquqiy tenglik g'oyasi.",
    },
    {
        "sarlavha": "Millat majlisi va qonun chiqarish tamoyili",
        "matn": (
            "Xulosa: muxtoriyatni millat majlisi har bir xalqning nafyini ko'zda tutub, "
            "qonun chiqarar."
        ),
        "manba": "«Haq olinur, berilmas!» — «Hurriyat» gazetasi, 1918 yil, 26 yanvar",
        "izoh": "🏛 Bu jumla parlament qonun chiqarish tamoyilining lo'nda ta'rifi: "
                "qonun xalq manfaatidan kelib chiqmog'i shart.",
    },
    {
        "sarlavha": "Meros huquqi va adolat — Faroiz",
        "matn": (
            "Shariat kitoblaridan «Faroiz» kitobida: "
            "«O'lukning molidan avvalon o'lukka kerakli, muvofiq sunnat va isrofsiz kafan qilib, "
            "dafn qilmoqqa sarf qilinsin, so'ngra qarzi berilur. So'ngra ortgan mollarni "
            "varasasiga — merosxo'rlariga muvofiq shariat taqsim qilinib berilur», deyilgan."
        ),
        "manba": "«Bizni kemiruvchi illatlar» — «Oyina» jurnali, 1915 yil, 13-son",
        "izoh": "⚖️ Behbudiy meros huquqini shariat va adolat nuqtai nazaridan tahlil qilgan. "
                "Merosxo'rlarning huquqlarini himoya qilish masalasi bugun ham dolzarbdir.",
    },
    {
        "sarlavha": "Zaif ijtimoiy guruhlar huquqlari — beva va etimlar",
        "matn": (
            "Ba'zi bir bechora sagir va mushtipor ayollar merosdan va haqlаridan noqis olurlar. "
            "Ba'zi qarzdorlarning haqqi xudoyi va xayrot sababi ila kuйib ketar. "
            "Bechora o'lukning zimmasi qarzdан qutulolmay qolur."
        ),
        "manba": "«Bizni kemiruvchi illatlar» — «Oyina» jurnali, 1915 yil, 13-son",
        "izoh": "🛡 Beva ayollar va etimlarning huquqlarini himoya qilish masalasini "
                "Behbudiy yuz yil avval ko'targan. Bu bugungi ijtimoiy huquq konsepsiyasining poydevoridir.",
    },
    {
        "sarlavha": "So'z erkinligi va matbuot huquqi",
        "matn": (
            "Haqiqiy matbuot hech kimni xotiriga qaramaydi. "
            "'Xotir qolmasin' kasali biz muslmonlarni barbod etdi."
        ),
        "manba": "«Tanqid — saralamoqdir» — «Oyina» jurnali, 1914 yil, 32-son",
        "izoh": "✍️ So'z erkinligi va tanqid huquqi — demokratik huquqiy tartibning asosi. "
                "Behbudiy bu haqda o'z davrida juda ochiq yozgan.",
    },
    {
        "sarlavha": "Mulkiy huquq va yer masalasi",
        "matn": (
            "Elli sana muqaddam yer sotilsa, bir muslim olardi, "
            "endi boshqalar olur. Mana, endi biz shu hol ilan yana yigirma–o'ttiz yil o'tkarsak, "
            "xalqimizning yarmidan ziyodasi vatansiz, yersiz darbadar bo'laturg'oni ma'lum va oshkordir."
        ),
        "manba": "«Bizni kemiruvchi illatlar» — «Oyina» jurnali, 1915 yil, 13-son",
        "izoh": "🏠 Mulk huquqi va yer egаligini himoya qilish masalasi — "
                "Behbudiy buni huquqiy muammo sifatida ko'targan birinchi ziyolilardandir.",
    },
]

# ── Viktorina ─────────────────────────────────────────────────────────────────
VIKTORINA = [
    {
        "savol": "🎯 Behbudiy qaysi yilda tug'ilgan?",
        "variantlar": ["1870", "1875", "1880", "1865"],
        "to'gri": 1,
        "izoh": "Mahmudxo'ja Behbudiy 1875-yilda Samarqand viloyatida tug'ilgan.",
    },
    {
        "savol": "📖 Behbudiyning mashhur dramasi qanday nomlanadi?",
        "variantlar": ["Alpomish", "Padarkush", "O'tkan kunlar", "Sarob"],
        "to'gri": 1,
        "izoh": "'Padarkush' (1913) — O'rta Osiyodagi birinchi milliy drama.",
    },
    {
        "savol": "📰 Behbudiy qaysi jurnalga asos solgan?",
        "variantlar": ["Mushtum", "Oyina", "Sadoi Turkiston", "Turan"],
        "to'gri": 1,
        "izoh": "'Oyina' jurnali 1914-yilda Samarqandda chiqarila boshlagan.",
    },
    {
        "savol": "⚖️ Behbudiy qaysi maqolasida yurist tayyorlash zarurligini yozgan?",
        "variantlar": ["Padarkush", "Ehtiyoji millat", "Tanqid saralamoqdir", "Yoshlarga murojaat"],
        "to'gri": 1,
        "izoh": "'Ehtiyoji millat' (1913) — millat uchun huquqshunos tayyorlash haqida.",
    },
    {
        "savol": "🏛 'Haq olinur, berilmas!' maqolasi qaysi gazetada chop etilgan?",
        "variantlar": ["Oyina", "Samarqand", "Hurriyat", "Turan"],
        "to'gri": 2,
        "izoh": "Maqola 1918-yil 26-yanvarda 'Hurriyat' gazetasida nashr etilgan.",
    },
    {
        "savol": "🎭 'Padarkush' qaysi yilda yozilgan?",
        "variantlar": ["1905", "1910", "1913", "1916"],
        "to'gri": 2,
        "izoh": "Drama 1913-yilda yozilgan va O'rta Osiyo teatrining boshlanishi hisoblanadi.",
    },
    {
        "savol": "🌍 Behbudiy qaysi harakatning yetakchisi bo'lgan?",
        "variantlar": ["Qo'qon xonligi", "Jadidchilik", "Bosmachi", "Sho'rolar"],
        "to'gri": 1,
        "izoh": "Jadidchilik — XIX asr oxiri XX asr boshidagi islohot va ma'rifat harakati.",
    },
    {
        "savol": "☠️ Behbudiy qaysi yilda shahid qilingan?",
        "variantlar": ["1917", "1918", "1919", "1920"],
        "to'gri": 2,
        "izoh": "Behbudiy 1919-yilda Shahrisabzda o'ldirilgan.",
    },
]

user_quiz_state = {}


# ══════════════════════════════════════════════════════════════════════════════
#  MENYU
# ══════════════════════════════════════════════════════════════════════════════

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 Hayoti va faoliyati",            callback_data="hayot")],
        [InlineKeyboardButton("📚 Asarlari",                        callback_data="asarlar"),
         InlineKeyboardButton("💡 G'oyalari",                       callback_data="goyalar")],
        [InlineKeyboardButton("🎭 Padarkush",                       callback_data="padarkush")],
        [InlineKeyboardButton("⚖️ Yuristlarga yo'l ko'rsatkich",   callback_data="huquq_menu")],
        [InlineKeyboardButton("💬 Iqtibos",                         callback_data="iqtibos"),
         InlineKeyboardButton("🧠 Viktorina",                       callback_data="viktorina_start")],
        [InlineKeyboardButton("🔔 Kunlik xabar (soat 9:00)",       callback_data="subscribe_info")],
        [InlineKeyboardButton("ℹ️ Bot haqida",                     callback_data="haqida")],
    ])


# ══════════════════════════════════════════════════════════════════════════════
#  COMMAND HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "⚖️📜 *Assalomu alaykum!*\n\n"
        "Ushbu bot *Mahmudxo'ja Behbudiy* — Turkiston jadidchilik harakatlarining buyuk namoyandasi "
        "haqida ma'lumot beradi.\n\n"
        "🆕 *Yangi bo'lim:* Behbudiyning huquq va qonun haqidagi fikrlari — "
        "*yuristlar uchun yo'l ko'rsatkich!*\n\n"
        "🔔 Har kuni soat *9:00* da (Toshkent vaqti) yuridik iqtibos olish uchun: /obuna\n\n"
        "Bo'limni tanlang:"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_menu_keyboard())


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subs    = load_subscribers()
    user_id = update.effective_user.id
    if user_id in subs:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Bekor qilish", callback_data="unsubscribe")]])
        await update.message.reply_text(
            "✅ Siz allaqachon obunachisiz!\nHar kuni soat *9:00* da iqtibos olasiz.",
            parse_mode="Markdown", reply_markup=kb,
        )
    else:
        subs.add(user_id)
        save_subscribers(subs)
        await update.message.reply_text(
            "🔔 *Obuna bo'ldingiz!*\n\n"
            "Har kuni soat *9:00* da (Toshkent vaqti) Behbudiyning "
            "huquq va qonun haqidagi fikrlaridan birini olasiz.\n\n"
            "Bekor qilish: /bekor",
            parse_mode="Markdown",
        )


async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subs    = load_subscribers()
    user_id = update.effective_user.id
    if user_id in subs:
        subs.discard(user_id)
        save_subscribers(subs)
        await update.message.reply_text("❌ Obuna bekor qilindi. Qayta: /obuna")
    else:
        await update.message.reply_text("Siz obunachi emassiz. Obuna bo'lish: /obuna")


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 *Asosiy menyu:*", parse_mode="Markdown", reply_markup=main_menu_keyboard())


# ══════════════════════════════════════════════════════════════════════════════
#  KUNLIK NOTIFICATION JOB
# ══════════════════════════════════════════════════════════════════════════════

async def send_daily_quote(context: ContextTypes.DEFAULT_TYPE):
    subs = load_subscribers()
    if not subs:
        return
    maqola = random.choice(HUQUQ_MAQOLALAR)
    text = (
        f"⚖️ *Behbudiydan kunlik huquqiy fikr*\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"📌 *{maqola['sarlavha']}*\n\n"
        f"_{maqola['matn']}_\n\n"
        f"📚 *Manba:* {maqola['manba']}\n\n"
        f"💡 {maqola['izoh']}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🔕 Bekor qilish: /bekor  |  📋 Menyu: /menu"
    )
    failed = []
    for uid in list(subs):
        try:
            await context.bot.send_message(chat_id=uid, text=text, parse_mode="Markdown")
        except Exception as e:
            logger.warning(f"Foydalanuvchi {uid} ga yuborib bo'lmadi: {e}")
            failed.append(uid)
    if failed:
        subs -= set(failed)
        save_subscribers(subs)


# ══════════════════════════════════════════════════════════════════════════════
#  CALLBACK HANDLER
# ══════════════════════════════════════════════════════════════════════════════

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data  = query.data

    back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")]])

    # ── Asosiy ma'lumot bo'limlari ─────────────────────────────────────────────
    if data in BEHBUDIY_INFO:
        await query.edit_message_text(BEHBUDIY_INFO[data], parse_mode="Markdown", reply_markup=back_kb)

    elif data == "iqtibos":
        ibora, manba = random.choice(IQTIBOSLAR)
        text = f"💬 *Behbudiy iqtibosi:*\n\n_{ibora}_\n\n— {manba}"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yana bir iqtibos", callback_data="iqtibos")],
            [InlineKeyboardButton("🔙 Menyu",            callback_data="back_main")],
        ])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

    # ══════════════════════════════════════════════════════════════════════════
    #  ⚖️ YURISPRUDENSIYA
    # ══════════════════════════════════════════════════════════════════════════
    elif data == "huquq_menu":
        text = (
            "⚖️ *Behbudiy — Yuristlarga yo'l ko'rsatkich*\n\n"
            "Behbudiy o'z maqolalarida huquq, qonun, sud, adolat, meros huquqi "
            "va mulkiy huquq masalalarini chuqur tahlil qilgan.\n\n"
            "Bu bo'lim *huquq talabalari va amaliyotchi yuristlar* uchun mo'ljallangan.\n\n"
            "📚 Jami *12 ta* yuridik iqtibos va tahlil mavjud:"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔀 Tasodifiy iqtibos",          callback_data="huquq_random")],
            [InlineKeyboardButton("📋 Barchasini o'qish (1→12)",   callback_data="huquq_list_0")],
            [InlineKeyboardButton("🔔 Har kuni 9:00 da olish",     callback_data="subscribe_btn")],
            [InlineKeyboardButton("🔙 Orqaga",                      callback_data="back_main")],
        ])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

    elif data == "huquq_random":
        m    = random.choice(HUQUQ_MAQOLALAR)
        text = (
            f"⚖️ *{m['sarlavha']}*\n\n"
            f"_{m['matn']}_\n\n"
            f"📚 *Manba:* {m['manba']}\n\n"
            f"💡 {m['izoh']}"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔀 Yana boshqasi", callback_data="huquq_random")],
            [InlineKeyboardButton("📋 Ro'yxat",       callback_data="huquq_list_0")],
            [InlineKeyboardButton("🔙 Orqaga",         callback_data="huquq_menu")],
        ])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

    elif data.startswith("huquq_list_"):
        idx   = int(data.split("_")[2])
        total = len(HUQUQ_MAQOLALAR)
        m     = HUQUQ_MAQOLALAR[idx]
        text  = (
            f"⚖️ *{idx+1}/{total} — {m['sarlavha']}*\n\n"
            f"_{m['matn']}_\n\n"
            f"📚 *Manba:* {m['manba']}\n\n"
            f"💡 {m['izoh']}"
        )
        nav = []
        if idx > 0:
            nav.append(InlineKeyboardButton("◀️ Oldingi", callback_data=f"huquq_list_{idx-1}"))
        if idx < total - 1:
            nav.append(InlineKeyboardButton("Keyingi ▶️", callback_data=f"huquq_list_{idx+1}"))
        kb = InlineKeyboardMarkup([nav, [InlineKeyboardButton("🔙 Orqaga", callback_data="huquq_menu")]])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

    # ── Obuna ─────────────────────────────────────────────────────────────────
    elif data == "subscribe_info":
        text = (
            "🔔 *Kunlik Huquqiy Iqtibos*\n\n"
            "Har kuni soat *9:00* da (Toshkent vaqti) "
            "Behbudiyning huquq va qonun haqidagi fikrlaridan "
            "bittasi Telegram orqali keladi.\n\n"
            "👨‍⚖️ *Kimlar uchun:* huquq talabalari, yuristlar, advokatlar, qozilar."
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Obuna bo'lish", callback_data="subscribe_btn")],
            [InlineKeyboardButton("🔙 Orqaga",        callback_data="back_main")],
        ])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

    elif data == "subscribe_btn":
        subs    = load_subscribers()
        user_id = query.from_user.id
        if user_id in subs:
            await query.edit_message_text(
                "✅ Siz allaqachon obunachisiz!\nHar kuni soat *9:00* da iqtibos keladi.\n\nBekor qilish: /bekor",
                parse_mode="Markdown", reply_markup=back_kb,
            )
        else:
            subs.add(user_id)
            save_subscribers(subs)
            await query.edit_message_text(
                "🔔 *Obuna bo'ldingiz!*\n\n"
                "Ertadan boshlab har kuni soat *9:00* da Behbudiyning "
                "huquqiy iqtibosini olasiz.\n\nBekor qilish: /bekor",
                parse_mode="Markdown", reply_markup=back_kb,
            )

    elif data == "unsubscribe":
        subs = load_subscribers()
        subs.discard(query.from_user.id)
        save_subscribers(subs)
        await query.edit_message_text("❌ Obuna bekor qilindi. Qayta: /obuna", reply_markup=back_kb)

    # ── Bot haqida ─────────────────────────────────────────────────────────────
    elif data == "haqida":
        text = (
            "ℹ️ *Bot haqida:*\n\n"
            "Bu bot *O'zbekiston Xalqaro Islom Akademiyasi* talabasi tomonidan "
            "Mahmudxo'ja Behbudiy nomidagi maxsus stipendiya doirasida yaratilgan.\n\n"
            "🎯 *Maqsad:* Behbudiy merosini IT orqali targ'ib qilish. "
            "Uning huquqiy qarashlari bugungi yuristlar uchun yo'l ko'rsatkich sifatida taqdim etish.\n\n"
            "⚙️ *Texnologiyalar:* Python · python-telegram-bot · pytz · JobQueue\n\n"
            "📬 Murojaat: @Mehriniso_Esonova"
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=back_kb)

    elif data == "back_main":
        await query.edit_message_text(
            "📋 *Asosiy menyu — bo'limni tanlang:*",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )

    # ══════════════════════════════════════════════════════════════════════════
    #  VIKTORINA
    # ══════════════════════════════════════════════════════════════════════════
    elif data == "viktorina_start":
        user_id = query.from_user.id
        user_quiz_state[user_id] = {"index": 0, "score": 0}
        await send_question(query, user_id)

    elif data.startswith("ans_"):
        user_id = query.from_user.id
        if user_id not in user_quiz_state:
            await query.edit_message_text("❗ Viktorinani qaytadan boshlang: /start")
            return
        chosen  = int(data.split("_")[1])
        state   = user_quiz_state[user_id]
        q       = VIKTORINA[state["index"]]
        correct = q["to'gri"]

        if chosen == correct:
            state["score"] += 1
            result_text = f"✅ *To'g'ri!*\n\n📝 {q['izoh']}"
        else:
            result_text = f"❌ *Noto'g'ri.*\n\nTo'g'ri javob: *{q['variantlar'][correct]}*\n\n📝 {q['izoh']}"

        state["index"] += 1
        if state["index"] >= len(VIKTORINA):
            score   = state["score"]
            total   = len(VIKTORINA)
            pct     = round(score / total * 100)
            emoji   = "🏆" if pct >= 80 else ("👍" if pct >= 50 else "📚")
            comment = (
                "Zo'r! Behbudiy bo'yicha bilimingiz a'lo!" if pct >= 80 else
                "Yaxshi! Yana o'qib bilimingizni oshiring."  if pct >= 50 else
                "Keling, Behbudiyni yaxshiroq o'rganamiz!"
            )
            text = (
                f"{result_text}\n\n━━━━━━━━━━━━━━━━━━\n"
                f"{emoji} *Viktorina yakunlandi!*\n\n"
                f"Natija: *{score}/{total}* ({pct}%)\n_{comment}_"
            )
            del user_quiz_state[user_id]
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Qayta boshlash", callback_data="viktorina_start")],
                [InlineKeyboardButton("🔙 Menyu",          callback_data="back_main")],
            ])
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Davom etish", callback_data="next_q")]])
            await query.edit_message_text(result_text, parse_mode="Markdown", reply_markup=kb)

    elif data == "next_q":
        user_id = query.from_user.id
        if user_id in user_quiz_state:
            await send_question(query, user_id)
        else:
            await query.edit_message_text("❗ /start orqali qaytadan boshlang.")


async def send_question(query, user_id: int):
    state   = user_quiz_state[user_id]
    idx     = state["index"]
    q       = VIKTORINA[idx]
    buttons = [
        [InlineKeyboardButton(f"{['A','B','C','D'][i]}. {v}", callback_data=f"ans_{i}")]
        for i, v in enumerate(q["variantlar"])
    ]
    text = (
        f"🧠 *Viktorina — savol {idx+1}/{len(VIKTORINA)}*\n"
        f"⭐ Hozircha: {state['score']} ball\n\n"
        f"{q['savol']}"
    )
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Menyudan foydalaning:", reply_markup=main_menu_keyboard())


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start",  start))
    app.add_handler(CommandHandler("menu",   menu_command))
    app.add_handler(CommandHandler("obuna",  subscribe_command))
    app.add_handler(CommandHandler("bekor",  unsubscribe_command))

    # Buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    # Text fallback
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))

    # ── Har kuni soat 9:00 da notification ──────────────────────────────────
    job_queue: JobQueue = app.job_queue
    job_queue.run_daily(
        send_daily_quote,
        time=dt_time(hour=NOTIF_HOUR, minute=NOTIF_MIN, tzinfo=TIMEZONE),
        name="daily_huquq_quote",
    )

    print("⚖️📜 Behbudiy boti ishga tushdi!")
    print(f"🔔 Kunlik notification: har kuni soat {NOTIF_HOUR:02d}:{NOTIF_MIN:02d} (Toshkent vaqti)")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
