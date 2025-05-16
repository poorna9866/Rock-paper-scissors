from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "supersecret"  

choices = ['rock', 'paper', 'scissors']
emojis = {
    "win": "🏆",
    "lose": "😵",
    "tie": "🤝"
}

def determine_winner(user, computer):
   
    if user == computer:
        return "It's a tie!", emojis["tie"]
    elif (user == 'rock' and computer == 'scissors') or \
         (user == 'paper' and computer == 'rock') or \
         (user == 'scissors' and computer == 'paper'):
        return "You win!", emojis["win"]
    else:
        return "You lose!", emojis["lose"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
   
    if 'rounds' not in session:
        return redirect(url_for('index')) 
    
    user_choice = request.form['choice']
    computer_choice = random.choice(choices)
    result_text, emoji = determine_winner(user_choice, computer_choice)
    
  
    if result_text == "You win!":
        session['user_wins'] += 1
    elif result_text == "You lose!":
        session['computer_wins'] += 1

    session['current_round'] += 1

   
    if session['current_round'] > session['rounds']:
        return redirect(url_for('final_result'))
    
    return render_template(
        'index.html',
        user_choice=user_choice,
        computer_choice=computer_choice,
        result=result_text,
        emoji=emoji,
        current_round=session['current_round'],
        total_rounds=session['rounds']
    )

@app.route('/new_game')
def new_game():
    
    session.clear()  
    return redirect(url_for('index'))

@app.route('/set_rounds', methods=['POST'])
def set_rounds():
   
    session['rounds'] = int(request.form['rounds'])  
    session['current_round'] = 1  
    session['user_wins'] = 0
    session['computer_wins'] = 0
    return redirect(url_for('index'))

@app.route('/final_result')
def final_result():
    
    user_wins = session['user_wins']
    computer_wins = session['computer_wins']
    
    if user_wins > computer_wins:
        winner = "You win the game! 🎉"
    elif computer_wins > user_wins:
        winner = "Computer wins the game! 😵"
    else:
        winner = "It's a tie! 🤝"
    
    return render_template(
        'final_result.html',
        winner=winner,
        user_wins=user_wins,
        computer_wins=computer_wins
    )

if __name__ == '__main__':
    app.run(debug=True)
