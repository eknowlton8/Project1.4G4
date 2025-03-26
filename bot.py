import discord
import requests
import json
from discord.ext import commands, tasks
from datetime import datetime

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# File to store scores
score_file = 'scores.json'

# Fetch trivia questions from Open Trivia Database API
def fetch_trivia():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)
    question_data = response.json()
    question = question_data['results'][0]
    return question

# Load scores from the JSON file
def load_scores():
    try:
        with open(score_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save scores to the JSON file
def save_scores(scores):
    with open(score_file, 'w') as f:
        json.dump(scores, f, indent=4)

# Send a trivia question and start tracking
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    post_trivia.start()  # Start posting trivia at regular intervals

# Post trivia question every 24 hours (change as needed)
@tasks.loop(hours=24)
async def post_trivia():
    channel = bot.get_channel(YOUR_CHANNEL_ID)  # Replace with your channel ID
    question = fetch_trivia()
    question_text = question['question']
    choices = question['incorrect_answers'] + [question['correct_answer']]
    correct_answer = question['correct_answer']
    trivia_data = {
        'question': question_text,
        'choices': choices,
        'correct_answer': correct_answer
    }
    await channel.send(f"Trivia Question: {question_text}")
    await channel.send(f"Choices: {', '.join(choices)}")
    await channel.send("Respond with the correct answer to earn points!")
    bot.trivia_data = trivia_data

# Command to submit answers
@bot.command()
async def answer(ctx, *, user_answer):
    correct_answer = bot.trivia_data['correct_answer']
    scores = load_scores()

    if user_answer.lower() == correct_answer.lower():
        await ctx.send(f"Correct, {ctx.author.name}! Well done!")
        if ctx.author.name not in scores:
            scores[ctx.author.name] = 0
        scores[ctx.author.name] += 1
    else:
        await ctx.send(f"Incorrect, {ctx.author.name}. The correct answer was: {correct_answer}")

    save_scores(scores)

# Command to show the leaderboard
@bot.command()
async def leaderboard(ctx):
    scores = load_scores()
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    leaderboard_message = "Leaderboard:\n"
    for user, score in sorted_scores:
        leaderboard_message += f"{user}: {score} points\n"
    await ctx.send(leaderboard_message)

# Command to give a hint
@bot.command()
async def hint(ctx):
    question = bot.trivia_data['question']
    await ctx.send(f"Here's a hint for you: {question[:int(len(question)/2)]}...")

# Run the bot
bot.run('YOUR_BOT_TOKEN')  # Replace with your bot's token
