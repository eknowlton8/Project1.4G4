import requests
import json

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

# Function to display the leaderboard
def show_leaderboard():
    scores = load_scores()
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("Leaderboard:")
    for user, score in sorted_scores:
        print(f"{user}: {score} points")

# Function to give a hint
def give_hint(question_text):
    hint = question_text[:int(len(question_text)/2)] + "..."
    print(f"Here's a hint: {hint}")

# Main function to play the trivia game
def trivia_game():
    scores = load_scores()

    print("Welcome to the Trivia Game!\n")

    while True:
        # Fetch trivia question
        question = fetch_trivia()
        question_text = question['question']
        choices = question['incorrect_answers'] + [question['correct_answer']]
        correct_answer = question['correct_answer']

        # Display the question and choices
        print(f"Trivia Question: {question_text}")
        print("Choices:")
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")

        # Get user input for the answer
        user_answer = input("Your answer (type the choice number or the answer): ").strip()

        if user_answer.lower() == correct_answer.lower() or user_answer.isdigit() and choices[int(user_answer) - 1].lower() == correct_answer.lower():
            username = input("Enter your username: ").strip()
            print(f"Correct, {username}! Well done!")
            if username not in scores:
                scores[username] = 0
            scores[username] += 1
        else:
            print(f"Incorrect! The correct answer was: {correct_answer}")

        # Save scores
        save_scores(scores)

        # Ask if the user wants to continue or see the leaderboard
        action = input("\nWould you like to play again (yes/no), see the leaderboard (leaderboard), or quit (quit)? ").strip().lower()

        if action == 'no' or action == 'quit':
            break
        elif action == 'leaderboard':
            show_leaderboard()
        elif action == 'yes':
            continue
        elif action == 'hint':
            give_hint(question_text)

if __name__ == "__main__":
    trivia_game()
