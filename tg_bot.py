import os
import psycopg2
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# connect to our db
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


# /start
def start(update, context):
    update.message.reply_text('Hello, i can found for you any tasks!')


# help
def help(update, context):
    update.message.reply_text('All commands:\n'
                              '/start - start to work with bot\n'
                              '/help - show all commands\n'
                              '/tasks - show tasks')


# /tasks
def tasks(update, context):
    # get topic and complexity of the taks 
    user_data = context.user_data
    user_data['state'] = 'difficulty'
    update.message.reply_text('Choose complexity (from 800 to 3500):')


# answer on choose complexity
def difficulty(update, context):
    # save choosed complexity and save
    user_data = context.user_data
    user_data['difficulty'] = int(update.message.text)
    user_data['state'] = 'topic'
    update.message.reply_text('Choose topic:')


# answer on topic
def topic(update, context):
    # save choosed topic and save them
    user_data = context.user_data
    user_data['topic'] = update.message.text
    user_data['state'] = 'count'
    update.message.reply_text('How much tasks you want get (from 1 to 10):')


# answer on count of tasks
def count(update, context):
    # save choosed count of tasks and show result
    user_data = context.user_data
    count = int(update.message.text)
    difficulty = user_data['difficulty']
    topic = user_data['topic']
    # request on bd for get tasks
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE difficulty=%s AND topic=%s ORDER BY RANDOM() LIMIT")
