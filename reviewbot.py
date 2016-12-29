
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import json
import logging
import os
import requests
import subprocess
import time
import urllib
from datetime import datetime
from functools import partial
from json import JSONDecoder
from pytz import timezone
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Chat, User, Message, Update, ChatMember, UserProfilePhotos, File, ReplyMarkup, TelegramObject
from urllib.request import urlopen
from urllib.parse import quote_plus, urlencode
from uuid import uuid4

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
def __repr__(self):
    return str(self)

config = configparser.ConfigParser()
config.read('bot.ini')

updater = Updater(token=config['KEYS']['bot_api'])
myusername = config['ADMIN']['username']
jenkinsconfig = config['JENKINS']['on']
gerritconfig = config['GERRIT']['on']

if jenkinsconfig == "yes":
    jenkins = config['JENKINS']['url']
    user = config['JENKINS']['user']
    password = config['JENKINS']['password']
    token = config['JENKINS']['token']
    job = config['JENKINS']['job']
if gerritconfig == "yes":
    gerrituser = config['GERRIT']['user']
    gerriturl = config['GERRIT']['url']
    protocol = config['GERRIT']['protocol']

dispatcher = updater.dispatcher


hereyago = "Here's a list of commands for you to use:\n"
build_help = "\n/build to start the build process\n"
changelog_help = "/changelog 'text' to set the changelog\n"
sync_help = "/sync to set sync to on/off\n"
clean_help = "/clean to set clean to on/off\n"
repopick_a_help = "\n/repopick to set repopick on or off\n"
repopick_b_help = "-- /repopick `changes` to pick from gerrit on build\n"
open_a_help = "\n/open to see all open changes\n"
open_b_help = "-- /open `projects` to see open changes for certain projects\n"
pickopen_help = "\n/pickopen to pick all open changes on gerrit\n"
link_help = "\n/link 'change numbers' to get a link to changes on gerrit\n"
help_help = "\n/help to see this message\n--/help 'command' to see information about that command :)" # love this lmao help_help

jenkinsbuildhelp = build_help + clean_help + changelog_help + sync_help
gerritbuildhelp = pickopen_help + repopick_a_help + repopick_b_help
gerrithelp = link_help + open_a_help + open_b_help
notmaster = "Sup *not* master. \n"
master = "Sup" + myusername + "\n"



def start(bot, update):
    if update.message.chat.type == "private":

        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Hi. I'm Hunter's Jenkins Bot! You can use me to do lots of cool stuff, assuming your name is @hunter_bruhh! If not, then I'm not much use to you right now! Maybe he'll implement some cool stuff later!")
        if jenkinsconfig == "yes" and gerritconfig == "yes":
            helpall = jenkinsbuildhelp + gerritbuildhelp + gerrithelp + help_help
        if jenkinsconfig == "yes" and gerritconfig != "yes":
            helpall = jenkinsbuildhelp + help_help
        if jenkinsconfig != "yes" and gerritconfig == "yes":
            helpall = gerrithelp + help_help
            
        bot.sendMessage(chat_id=update.message.chat_id,
                            text=helpall)

def help_message(bot, update, args):
    jenkinsbuildlist = ["build", "changelog", "sync", "clean"]
    gerritlist = ["open", "link"]
    gerritbuildlist = ["pickopen", "repopick"]
    standardlist = ["ban", "unban", "kick", "note"]

    args_length = len(args)
    if jenkinsconfig == "yes" and gerritconfig == "yes":
        masterlist = jenkinsbuildlist + gerritbuildlist + gerritlist
        helpall = gerrithelp + jenkinsbuildhelp + gerritbuildhelp + help_help
    if jenkinsconfig == "yes" and gerritconfig != "yes":
        masterlist = jenkinsbuildlist
        helpall = jenkinsbuildhelp + help_help
    if jenkinsconfig != "yes" and gerritconfig == "yes":
        masterlist = gerritlist
        helpall = gerrithelp + help_help
    if args_length != 0:
        if args_length > 1:
            for x in masterlist:
                try:
                    helpme
                except NameError:
                    helpmeplox = "Please use only ask about one command. A list of commands to ask about would be:\n"
            helpmeplox = helpmeplox + x + ",\n"
            helpme = helpmeplox
        else:
            if args[0] in masterlist:
                if args[0] == "build":
                    helpme = build_help
                if args[0] == "changelog":
                    helpme = changelog_help
                if args[0] == "sync":
                    helpme = sync_help
                if args[0] == "clean":
                    helpme = clean_help
                if args[0] == "repopick":
                    helpme = repopick_a_help + repopick_b_help
                if args[0] == "pickopen":
                    helpme = pickopen_help
                if args[0] == "open":
                    helpme = open_a_help + open_b_help
                if args[0] == "link":
                    helpme = link_help
            else:
                helpme = "That's not a command to ask about."
        bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
        time.sleep(1)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=helpme)
    else:
        bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
        time.sleep(1)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=helpall)
                        
if jenkinsconfig == "yes":
    def pickopen(bot, update):
        if update.message.from_user.id == int(config['ADMIN']['id']):
            bot.sendChatAction(chat_id=update.message.chat_id,
                               action=ChatAction.TYPING)
            curl = "curl -H 'Accept-Type: application/json' " + protocol + "://" + gerrituser + "@" + gerriturl + "/changes/?q=status:open | sed '1d' > open.json"
            command = subprocess.Popen(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            with open('open.json', encoding='utf-8') as data_file:
                data = json.load(data_file)
            dict_length = len(data)
            for i in range(dict_length):
                try:
                    cnumbers
                except NameError:
                    cnumbers = ""
                cnumbers = cnumbers + " " + str(data[i]['_number'])
            print(cnumbers)
            text = "I will pick all open changes: " + cnumbers
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=text,
                            parse_mode="Markdown")
            global rpick
            cnumbers.replace(" ", "%20")
            cnumbers_url = cnumbers.replace(" ", "%20")
            rpick = cnumbers_url

def choosebuild(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        keyboard = [[InlineKeyboardButton("Without Paramaters", callback_data='build')],

                    [InlineKeyboardButton("With Parameters", callback_data='buildWithParameters')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose a build style:', reply_markup=reply_markup)

def sync(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        keyboard = [[InlineKeyboardButton("YES", callback_data='syncon')],

                    [InlineKeyboardButton("NO", callback_data='syncoff')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Would you like to sync on a new build?:', reply_markup=reply_markup)

def clean(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        keyboard = [[InlineKeyboardButton("YES", callback_data='cleanon')],

                    [InlineKeyboardButton("NO", callback_data='cleanoff')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Would you like to clean on a new build?:', reply_markup=reply_markup)

def buildwithparams(bot, update, query):
    query = update.callback_query
    bot.sendMessage(chat_id=query.message.chat_id,
                    text="You have selected the 'buildWithParameters option, this will include a custom changelog with your build, and will specify whether to sync & clean or not",
                    parse_mode="Markdown")
    user_id = update.callback_query.from_user.id
    try:
        cg
    except NameError:
        bot.sendMessage(chat_id=query.message.chat_id,
                        text="You have selected the 'buildWithParameters option, but the changelog is empty. Please use /changelog + 'text' to provide a changlog for your users.",
                        parse_mode="Markdown")
        return 1
    try:
        syncparam
    except NameError:
        bot.sendMessage(chat_id=query.message.chat_id,
                text="You have selected the 'buildWithParameters option, but have not specified whether you would like to sync before building. Please use /sync to do so.",
                parse_mode="Markdown")
        return 1
    try:
        cleanparam
    except NameError:
        bot.sendMessage(chat_id=query.message.chat_id,
                text="You have selected the 'buildWithParameters option, but have not specified whether you would like to clean before building. Please use /clean to do so.",
                parse_mode="Markdown")
        return 1
    try:
        repopickstatus
    except NameError:
        bot.sendMessage(chat_id=query.message.chat_id,
                        text="You have selected the 'buildWithParameters option, but repopick isn't turned on or off. Turn it on or off with /repopick",
                        parse_mode="Markdown")
        return 1
    if repopickstatus == "true":
        try:
            rpick
        except NameError:
            bot.sendMessage(chat_id=query.message.chat_id,
                            text="You have selected the 'buildWithParameters option, repopick is on, but it's empty. Please use /repopick + 'changes' to pick changes from gerrit, or turn repopick off with /repopick",
                            parse_mode="Markdown")
            return 1
    if cg:
        if syncparam:
            if cleanparam:
                cg = quote_plus(cg)
                command_string = jenkins + "/job/" + job + "/buildWithParameters?token=" + token + "&changelog=" + cg + "&SYNC=" + syncparam + "&CLEAN=" + cleanparam + "&repopicks=" + rpick
                command = "curl --user " + user + ":" + password + " " + "'" + command_string + "'"
                print (command)
                if user_id == int(config['ADMIN']['id']):
                    bot.sendChatAction(chat_id=query.message.chat_id,
                                       action=ChatAction.TYPING)
                    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    output = output.stdout.read().decode('utf-8')
                    output = '`{0}`'.format(output)

                    bot.sendMessage(chat_id=query.message.chat_id,
                                    text=output,
                                    parse_mode="Markdown")
            else:
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="You have selected the 'buildWithParameters option, but have not specified whether you would like to clean before building. Please use /clean to do so.",
                                parse_mode="Markdown")
        else:
            bot.sendMessage(chat_id=query.message.chat_id,
                            text="You have selected the 'buildWithParameters option, but have not specified whether you would like to sync before building. Please use /sync to do so.",
                            parse_mode="Markdown")
    else:
        bot.sendMessage(chat_id=query.message.chat_id,
                            text="You have selected the 'buildWithParameters option, but the changelog is empty. Please use /changelog + 'text' to provide a changlog for your users.",
                            parse_mode="Markdown")


def buildwithoutparams(bot, update, query):
    user_id = update.callback_query.from_user.id
    command_string = jenkins + "/job/" + job + "/buildWithParameters?token=" + token
    command = "curl --user " + user + ":" + password + " " + "'" + command_string + "'"
    print (command)
    if user_id == int(config['ADMIN']['id']):
        bot.sendChatAction(chat_id=query.message.chat_id,
                           action=ChatAction.TYPING)
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = output.stdout.read().decode('utf-8')
        output = '`{0}`'.format(output)

        bot.sendMessage(chat_id=query.message.chat_id,
                        text=output, parse_mode="Markdown")

def changelog(bot, update, args):
        if update.message.from_user.id == int(config['ADMIN']['id']):
            global cg
            str_args = ' '.join(args)
            if str_args != "":
                update.message.reply_text('Changelog updated: ' + "'" + str_args + "'")
                cgs = '%20'.join(args)
                cg = cgs
                print ("Changelog set to " + "'" + cg + "'")
            else:
                bot.sendMessage(chat_id=update.message.chat_id,
                                text="You cannot provide an empty changelog.",
                                parse_mode="Markdown")

def repopick(bot, update, args):
        if update.message.from_user.id == int(config['ADMIN']['id']):
            global rpick

            str_args = ' '.join(args)
            if str_args != "":
                update.message.reply_text('I will pick changes: ' + "'" + str_args + "'")
                rpicks = '%20'.join(args)
                rpick = rpicks
                print ("Repopick set to" + "'" + rpick + "'")
            else:
                keyboard = [[InlineKeyboardButton("ON", callback_data='repopickon')],

                            [InlineKeyboardButton("OFF", callback_data='repopickoff')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text('Turn repopick ON or OFF:', reply_markup=reply_markup)

def button(bot, update, direct=True):
        user_id = update.callback_query.from_user.id
        if user_id == int(config['ADMIN']['id']):
            query = update.callback_query

            selected_button = query.data
            global cleanparam
            global syncparam
            global repopickstatus
            if selected_button == 'buildWithParameters':
                bot.editMessageText(text="Selected option: With Paramaters",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                buildwithparams(bot, update, query)
            if selected_button == 'build':
                bot.editMessageText(text="Selected option: Without Paramaters",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                buildwithoutparams(bot, update, query)
            if selected_button == 'syncon':
                bot.editMessageText(text="Selected option: YES",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                syncparam = "true"
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="Sync set to true",
                                parse_mode="Markdown")
            if selected_button == 'syncoff':
                bot.editMessageText(text="Selected option: NO",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                syncparam = "false"
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="Sync set to false",
                                parse_mode="Markdown")
            if selected_button == 'cleanon':
                bot.editMessageText(text="Selected option: YES",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                cleanparam = "true"
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="Clean set to true",
                                parse_mode="Markdown")
            if selected_button == 'cleanoff':
                bot.editMessageText(text="Selected option: NO",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                cleanparam = "false"
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="Clean set to false",
                                parse_mode="Markdown")
            if selected_button == 'repopickon':
                bot.editMessageText(text="Selected option: ON",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                repopickstatus = "true"
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="repopick set to ON",
                                parse_mode="Markdown")
            if selected_button == 'repopickoff':
                bot.editMessageText(text="Selected option: OFF",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                repopickstatus = "false"
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="repopick set to OFF",
                                parse_mode="Markdown")
        else:
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="You trying to spam me bro?",
                                parse_mode="Markdown")
        return False


if jenkinsconfig == "yes":
    pickopen_handler = CommandHandler('pickopen', pickopen)
    sync_handler = CommandHandler('sync', sync)
    clean_handler = CommandHandler('clean', clean)
    build_handler = CommandHandler('build', choosebuild)
    repopick_handler = CommandHandler('repopick', repopick, pass_args=True)
    changelog_handler = CommandHandler('changelog', changelog,  pass_args=True)

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_message, pass_args=True)

if jenkinsconfig == "yes":
    dispatcher.add_handler(pickopen_handler)
    dispatcher.add_handler(sync_handler)
    dispatcher.add_handler(clean_handler)
    dispatcher.add_handler(build_handler)
    dispatcher.add_handler(repopick_handler)
    dispatcher.add_handler(changelog_handler)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()