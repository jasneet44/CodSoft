from tkinter import *
from tkinter import ttk
import random

# Initialize main window
root = Tk()
root.geometry("800x400")
root.title("Rock Paper Scissors Game")
root.config(background="lightblue")

# Initialize counters for game results
computer_wins, user_wins, ties = 0, 0, 0

# Load images
image_dict = {
    "Rock": PhotoImage(file='images/dog.png'),
    "Paper": PhotoImage(file='images/girl.png'),
    "Scissors": PhotoImage(file='images/logo.png'),
    "Default": PhotoImage(file='images/fly.png')  # Add a default image
}

def decide_winner():
    global computer_wins
    global user_wins
    global ties

    # Choices
    choices = ["Rock", "Paper", "Scissors"]
    computer_choice = random.choice(choices)
    user_choice = selected_choice.get()

    # Determine the result
    if (computer_choice == "Rock" and user_choice == "Scissors") or \
       (computer_choice == "Paper" and user_choice == "Rock") or \
       (computer_choice == "Scissors" and user_choice == "Paper"):
        computer_wins += 1
        result_message = "Computer Wins"
    elif computer_choice == user_choice:
        ties += 1
        result_message = "It's a Tie"
    else:
        user_wins += 1
        result_message = "User Wins"

    # Update the result label
    result_label.config(text=result_message, bg="lightgray")

    # Update the images frame
    update_images_frame(computer_choice, user_choice)

    # Update the scoreboard
    update_scoreboard()

def update_images_frame(computer_choice, user_choice):
    # Update the images displayed in the images frame
    computer_image_label.config(image=image_dict[computer_choice])
    user_image_label.config(image=image_dict[user_choice])

def update_scoreboard():
    # Update the scoreboard table with current scores
    for row in tree.get_children():
        tree.delete(row)
    
    tree.insert("", "end", values=("Computer", computer_wins))
    tree.insert("", "end", values=("User", user_wins))
    tree.insert("", "end", values=("Ties", ties))

def stop_game():
    global computer_wins
    global user_wins
    global ties
    print(f"Computer wins {computer_wins} times and user wins {user_wins} times.")
    print(f"Also, the game tied {ties} times.")
    root.quit()

# Title label
title_label = Label(root, text="Rock Paper Scissors Game!!", bg="lightblue", font=('Helvetica', 18, 'bold'))
title_label.pack(pady=15)

# Final frame
final_frame = Frame(root, bg="lightblue", padx=20, pady=10,height=100)
final_frame.pack( fill=BOTH, padx=10, pady=10)

# Create frames for layout inside final_frame
left_frame = Frame(final_frame, bg="#EFC3CA", padx=20, pady=10, relief=RAISED, borderwidth=2)
left_frame.pack(side=LEFT, fill=BOTH, expand=True,padx=30)

center_frame = Frame(final_frame, bg="#FFDE59", padx=20, pady=10, relief=RAISED, borderwidth=2)
center_frame.pack(side=LEFT, fill=BOTH, expand=True,padx=30)

right_frame = Frame(final_frame, bg="#98DE7D", padx=20, pady=10, relief=RAISED, borderwidth=2)
right_frame.pack(side=LEFT, fill=BOTH, expand=True,padx=30)

# Variable for selected choice
selected_choice = StringVar()
selected_choice.set("Rock")  # Default choice

# Choice options
choices = [("Rock", image_dict["Rock"]), ("Paper", image_dict["Paper"]), ("Scissors", image_dict["Scissors"])]
for option, img in choices:
    Radiobutton(left_frame, text=option, variable=selected_choice, value=option, image=img, compound=LEFT, indicatoron=0, width=300, command=decide_winner, font=('Helvetica', 12, 'bold')).pack(pady=10)

# Result label
result_label = Label(left_frame, bg="lightgray", font=('Helvetica', 14), relief=RAISED, padx=10, pady=10)
result_label.pack(pady=10, fill=X)
result_label.config(text="Result", bg="lightgray")

# Create a table with two columns
tree = ttk.Treeview(right_frame, columns=("Category", "Score"), show='headings', height=6)
tree.heading("Category", text="Category", anchor=W)
tree.heading("Score", text="Score", anchor=W)
tree.column("Category", width=150, anchor=W)
tree.column("Score", width=100, anchor=W)
tree.pack(pady=10, padx=10)

# Stop button
Button(right_frame, text="Stop", bg="red", fg="white", font=('Helvetica', 12, 'bold'), command=stop_game, relief=RAISED, padx=10, pady=5).pack(pady=20)

# Create labels for displaying images with default images
computer_image_label = Label(center_frame, bg="#DE9E7D",relief=RIDGE,borderwidth=2, image=image_dict["Default"])
computer_image_label.pack(side=RIGHT, padx=10)

user_image_label = Label(center_frame, bg="#DE9E7D", relief=RIDGE,borderwidth=2,image=image_dict["Default"])
user_image_label.pack(side=LEFT, padx=10)

# Initialize the scoreboard
update_scoreboard()

# Run the application
root.mainloop()
