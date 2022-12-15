import Constants as keys
from telegram.ext.updater import Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import (Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telebot import (TeleBot)


bot = TeleBot(keys.API_KEY)
print("Bot started...")

# variables to put into logs
answer1 = ""
answer2 = ""
answer3 = ""
answer4 = ""
answer5 = ""
HTX = ""
trackA = 0
trackB = 0
trackC = 0

# creation of the reply buttons that will be use in the reply markup

qn1 = [[KeyboardButton("Enterprise Security Architecture")], [KeyboardButton("Source Code Analysis")],
       [KeyboardButton("Cyber Threat Hunting & Intelligence")]]
qn2 = [[KeyboardButton("Cryptography")], [KeyboardButton("Vulnerability Research")],
       [KeyboardButton("Cyber Exercises")]]
qn3 = [[KeyboardButton("DevSecOps")], [KeyboardButton("Vulnerability Assessment & Penetration Testing")],
       [KeyboardButton("Digital Forensics")]]
qn4 = [[KeyboardButton("Embedded & IoT System Security")], [KeyboardButton("Adversary Simulation")],
       [KeyboardButton("Incident Response Management")]]
qn5 = [[KeyboardButton("System Security Architecture")], [KeyboardButton("Exploit Development")],
       [KeyboardButton("Malware Analysis")]]

# Create a log file at start
now = datetime.datetime.now()
sessionLog = now.strftime("%d%m%Y_%H%M%S")
print("[Debug] Creating " + sessionLog + " .txt in /logs/")
fullLog = open("logs/session//" + sessionLog + ".txt", "w")
fullLog.write(sessionLog + '\n')
fullLog.close()



# function called when user types /start
def start_command(update, context: CallbackContext):
    if update.message.chat.username is not None:
        username = update.message.chat.username.replace(" ", "")  # remove spaces
        # logFile = username + ".txt" + username.encode('utf-8') causing error currently (caused error can only
        # concatenate str (not "bytes") to str) DEBUG
        print("[Debug] Creating " + username + ".txt" + " in /logs directory")

        with open("logs//" + username + ".txt", "w", encoding='utf-8') as f:
            current_time = now.strftime("%H:%M:%S")
            f.write(str(current_time) + '\n')
        question1(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Your username is not detected. Please set a username before continuing.")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="1. Click on ≡ (Top Left Corner) \n2. Click on settings \n3. Click on username "
                                      "(under Account) \n4. Set a new username \n5. Click on /start to begin")


# functions for question 1 - 5

def question1(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="The next few questions will help you discover the HTX cybersecurity competency "
                                  "framework domain you are most interested in.")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Q1. Which topic is the most interesting to you?",
                             reply_markup=ReplyKeyboardMarkup(qn1))


def question2(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Q2. Select the topic that is most interesting to you.",
                             reply_markup=ReplyKeyboardMarkup(qn2))


def question3(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Q3. Pick the topic that interests you the most.",
                             reply_markup=ReplyKeyboardMarkup(qn3))


def question4(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Q4. Which topic interests you the most?",
                             reply_markup=ReplyKeyboardMarkup(qn4))


def question5(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Q5. Choose the topic that interests you the most?",
                             reply_markup=ReplyKeyboardMarkup(qn5))


# function for putting results in a graph and sending graph to user
def summary(update, context):
    username = update.message.chat.username.replace(" ", "")
    file = open("logs//" + username + ".txt", "r")
    data = file.read()
    # Count for answers in the txt file
    A = data.count("A")
    B = data.count("B")
    C = data.count("C")
    count = A + B + C
    # if user answer all 5 questions
    if count == 5:
        tracks = {'trackA': A, 'trackB': B, 'trackC': C}

        custom_style = Style(
            legend_font_size=25,
            title_font_size=35,
            value_font_size=35,
            colors=('#0F52BA', '#330066', '#87CEEB'),
            value_colors=('#FFFFFF', '#FFFFFF', '#000000')
        )
        # Creation of Bar Graph
        bar_chart = pygal.Pie(title=username, style=custom_style, print_values=True,
                              legend_at_bottom=True, legend_box_size=40)
        bar_chart.add('Systems & Development', tracks['trackA'])
        bar_chart.add('Resilience', tracks['trackB'])
        bar_chart.add('Operations', tracks['trackC'])

        # Render File to PNG
        bar_chart.render_to_png('logs//' + username + '.png')
        file = open('logs//' + username + '.png', "rb")

        # Send message and Image
        context.bot.send_message(chat_id=update.effective_chat.id, text="Here are your results!")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=file,
                               reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please click /start if you like to redo the survey.")

        # to prevent sending faulty graphs
    elif count > 5:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You have answered too many times \nPlease click on /start to redo.",
                                 reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        # reset the file
        with open("logs//" + username + ".txt", "w", encoding='utf-8') as f:
            current_time = now.strftime("%H:%M:%S")
            f.write(str(current_time) + '\n')


# function called when user type /help
def help_command(update):
    update.message.reply_text(
        "This bot would help you find your interest in Cybersecurity! Just click /start to start your interest finder "
        "and remember to say hi to the bot. "
        "\nThere is an option beside the textbox to show the buttons that you would need to reply to the chatbot.")


# every reply would go through this function
# if answered, option chose would be added into the username.txt file
def handle_message(update: Update, context: CallbackContext):
    global HTX, answer1, answer2, answer3, answer4, answer5
    # Question 0 ask if user is a HTX staff
    if "Yes" in update.message.text:
        HTX = "HTX Staff"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("HTX Staff\n")
            f.close()
        question1(update, context)

    elif "No" in update.message.text:
        HTX = "Visitor"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Visitor\n")
            f.close()
        question1(update, context)

        # Question 1
    if "Enterprise Security Architecture" in update.message.text:
        answer1 = "Enterprise Security Architecture"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q1. A\n")
            f.close()
        question2(update, context)

    elif "Source Code Analysis" in update.message.text:
        answer1 = "Source Code Analysis"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q1. B\n")
            f.close()
        question2(update, context)

    elif "Cyber Threat Hunting & Intelligence" in update.message.text:
        answer1 = "Cyber Threat Hunting & Intelligence"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q1. C\n")
            f.close()
        question2(update, context)

    # Question 2
    if "Cryptography" in update.message.text:
        answer2 = "Cryptography"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q2. A\n")
            f.close()
        question3(update, context)
    elif "Vulnerability Research" in update.message.text:
        answer2 = "Vulnerability Research"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q2. B\n")
            f.close()
        question3(update, context)
    elif "Cyber Exercises" in update.message.text:
        answer2 = "Cyber Exercises"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q2. C\n")
            f.close()
        question3(update, context)

    # Question 3
    if "DevSecOps" in update.message.text:
        answer3 = "DevSecOps"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q3. A\n")
            f.close()
        question4(update, context)
    elif "Vulnerability Assessment & Penetration Testing" in update.message.text:
        answer3 = "Vulnerability Assessment & Penetration Testing"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q3. B\n")
            f.close()
        question4(update, context)
    elif "Digital Forensics" in update.message.text:
        answer3 = "Digital Forensics"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q3. C\n")
            f.close()
        question4(update, context)

    # Question 4
    if "Embedded & IoT System Security" in update.message.text:
        answer4 = "Embedded & IoT System Security"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q4. A\n")
            f.close()
        question5(update, context)

    elif "Adversary Simulation" in update.message.text:
        answer4 = "Adversary Simulation"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q4. B\n")
            f.close()
        question5(update, context)

    elif "Incident Response Management" in update.message.text:
        answer4 = "Incident Response Management"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q4. C\n")
            f.close()
        question5(update, context)

    # Question 5
    if "System Security Architecture" in update.message.text:
        answer5 = "System Security Architecture"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q5. A\n")
            f.close()

    elif "Exploit Development" in update.message.text:
        answer5 = "Exploit Development"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q5. B\n")
            f.close()

    elif "Malware Analysis" in update.message.text:
        answer5 = "Malware Analysis"
        username = update.message.chat.username.replace(" ", "")
        with open('logs//' + username + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q5. C\n")
            f.close()

    # DEBUG
    print("[DEBUG] ", answer1, ", ", answer2, ", ", answer3, ", ", answer4, ", ", answer5)

    # Only write to file & call results()
    if answer1 and answer2 and answer3 and answer4 and answer5:
        f1 = open("logs/session//" + sessionLog + ".txt", "a")
        f1.write(username + "," + HTX + "," + answer1 + "," + answer2 + "," + answer3 + "," + answer4 + "," + answer5 +
                 "\n")
        f1.close()

        summary(update, context)


# error handler
def error(update, context):
    print(f"Update {update} caused error {context.error}")


# main
def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


main()
