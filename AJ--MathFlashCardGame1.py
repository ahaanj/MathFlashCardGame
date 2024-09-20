
# Description: This is a math game made to quiz you on the math operations of
#              addition, subtraction, multiplication and the optional division.
#              The program will keep track of your score and also a provide
#              a log of all your questions answered. 



# Import necessary modules from the tkinter library
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Radiobutton, Label
from tkinter import scrolledtext
import random

# Initialize the main window
def create_main_window():
    window = Tk()
    window.title("Math Flashcards")
    window.geometry('1024x768')  
    return window
window = create_main_window()
   
# Global variables to track question statistics
total_questions = 0
correct_questions = 0
incorrect_questions = 0
game_over = False

# BooleanVar to track if division is enabled
division_var = BooleanVar()
division_var.set(False)

# Create a checkbox for enabling/disabling division
division_checkbox = Checkbutton(window, text="Enable Division", \
                                variable=division_var)
division_checkbox.grid(row=4, column=1, pady=10)

# Function to log a question with its user answer and correctness
def log_question(question, user_answer=None, correct=False):
    global correctLbl1
    
    # Split the question into parts (operands and operator)
    parts = question.replace(" ", "").split('+') + question.replace(" ", "").split('-') + question.replace(" ", "").split('*') + question.replace(" ", "").split('/')
    
    parts = [part for part in parts if part] # Remove empty parts
    
    if len(parts) != 3:
        formatted_question = question # If not a valid question, keep it as is
    else:
        num1, op, num2 = parts[0], parts[1], parts[2]

        formatted_question = ""
        # Format the question based on the operator
        if op == '+':
            formatted_question = f"{num1} + {num2}"
        elif op == '-':
            formatted_question = f"{num1} - {num2}"
        elif op == '*':
            formatted_question = f"{num1} * {num2}"
        elif op == '/':
            formatted_question = f"{num1} / {num2}"

    log_entry = ""
    if user_answer is not None:  # Check for None instead of if user_answer
        if correct:
            # Log if answer is correct 
            log_entry = f"Q: {formatted_question} | Answer: {user_answer} (Correct)\n"
            # Display correct answer with green background
            correctLbl1['text'] = 'Correct'
            correctLbl1['background'] = 'Green'
            correctLbl1.grid(row=3, column=0, columnspan=2, pady=5)
        else:
            # Log if answer is incorrect 
            log_entry = f"Q: {formatted_question} | Answer: {user_answer} (Incorrect)\n"
            # Display correct answer with green background
            correctLbl1['text'] = 'Incorrect'
            correctLbl1['background'] = 'Red'
            correctLbl1.grid(row=3, column=0, columnspan=2, pady=5)
    else:
        # Log the question without an answer
        log_entry = f"Q: {formatted_question}\n"
        
    # Insert the log entry at the beginning of the scrolled text widget
    question_log.insert("1.0", log_entry)

# Function to update the displayed statistics
def update_stats():
    stats_text.set(
        f"Total Questions Answered: {total_questions}\n"
        f"Questions Correct: {correct_questions}\n"
        f"Questions Incorrect: {incorrect_questions}\n"
        f"Fraction of Questions Right: {correct_questions}/{total_questions}\n"
        f"Percentage Mark: {f'{(correct_questions / total_questions) *100:.2f}'if total_questions != 0 else '0.00'}%"
    )
    
# Function to include or exclude division based on checkbox state
def include_division():
    global division_enabled, division_var
    print(f"Division enabled: {division_enabled}")
    generate_flashcard()


# Function to generate a math flashcard
def generate_flashcard():
    global game_over, level, division_var

    if game_over:
        return

    level_val = level.get()
    # Notify user if no level has been selected
    if level_val == 0:
        result_label["text"] = "Please select a level first and press Start"
        result_label["foreground"] = "red"
        return
    else:
        result_label["text"] = ""  # Clear the error message
        
    # Define possible operations based on whether division is enabled
    if division_var.get():
        possible_operations = ['+', '-', '*', '/']
    else:
        possible_operations = ['+', '-', '*']

    # Randomly select an operation
    operation = random.choice(possible_operations)

    # Generate random numbers based on the selected level
    if level_val == 1:
        num1 = random.randint(1, 3)
        num2 = random.randint(1, 3)
        max_divisor = 3
    elif level_val == 2:
        num1 = random.randint(1, 6)
        num2 = random.randint(1, 6)
        max_divisor = 6
    elif level_val == 3:
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        max_divisor = 9
    elif level_val == 4:
        num1 = random.randint(1, 12)
        num2 = random.randint(1, 12)
        max_divisor = 12
    elif level_val == 5:
        num1 = random.randint(-12, 12)
        num2 = random.randint(-12, 12)
        max_divisor = 12
    else:
        return 
    # Construct the question based on the selected operation
    if operation == '+':
        question = f"{num1} + {num2} = ?"
    elif operation == '-':
        question = f"{num1} - {num2} = ?"
    elif operation == '*':
        question = f"{num1} * {num2} = ?"
    elif operation == '/':

        divisor = random.randint(1, max_divisor)
        dividend = divisor * random.randint(1, max_divisor)
        question = f"{dividend} / {divisor} = ?"

    # Update the flashcard label with the generated question
    flashcard_label.configure(text=question)


# Function to check the user's answer
# Function to check the user's answer and update game statistics
def check_answer():
    # Access global variables
    global total_questions,correct_questions,incorrect_questions,level,game_over

    # Get the selected level value from the GUI
    level_val = level.get()

    # Check if a level is selected, if not, display an error message
    if level_val == 0:
        result_label["text"] = "Please select a level first and press Start"
        result_label["foreground"] = "red"
        return
    else:
        result_label["text"] = ""

    # Hide the correct label from the previous question
    correctLbl1.grid_forget()

    # Check if the game is over, display appropriate message
    if game_over:
        result_label["text"] = "Game Over! Click 'Restart Game' to play again."
        result_label["foreground"] = "red"
        return

    # Check if the game has started by verifying if a flashcard is displayed
    if not flashcard_label.cget("text"):
        result_label["text"] = "Please start the game first"
        result_label["foreground"] = "red"
        return

    # Get the user's answer from the entry widget and strip any extra spaces
    user_answer = answer_entry.get().strip()

    # Check if the user has entered an answer
    if not user_answer:
        result_label["text"] = "Please enter an answer"
        result_label["foreground"] = "red"
        return

    # Try to convert the user's answer to an integer, display an error
    # if it's not a valid number
    try:
        user_answer = int(user_answer)
    except ValueError:
        result_label["text"] = "Please enter a valid number"
        result_label["foreground"] = "red"
        return

    # Extract the expression from the flashcard text
    question_text = flashcard_label.cget("text")
    question_expression = question_text.replace("= ?", "")

    # Check for division by zero in the expression
    if '/' in question_expression:
        divisor_index = question_expression.index('/')
        divisor = int(question_expression[divisor_index + 1:].strip())
        if divisor == 0:
            result_label["text"] = "Cannot divide by zero"
            result_label["foreground"] = "red"
            return

    # Try to evaluate the correct answer from the expression, handle
    # ZeroDivisionError
    try:
        correct_answer = eval(question_expression)
    except ZeroDivisionError:
        result_label["text"] = "Cannot divide by zero"
        result_label["foreground"] = "red"
        return

    # Compare user's answer with the correct answer and update statistics
    if user_answer == correct_answer:
        correct_questions += 1
        log_question(question_text, user_answer, correct=True)
        correctLbl1['text'] = 'Correct'
        correctLbl1['background'] = 'Green'
        correctLbl1.grid(row=3, column=0, columnspan=2, pady=5)
    else:
        incorrect_questions += 1
        log_question(question_text, user_answer)
        correctLbl1['text'] = 'Incorrect'
        correctLbl1['background'] = 'Red'
        correctLbl1.grid(row=3, column=0, columnspan=2, pady=5)

    # Update total questions count, game statistics, and generate a new
    # flashcard
    total_questions += 1
    update_stats()
    generate_flashcard()


# Function to end the game and update related variables and GUI elements
def end_game():
    # Access global variable
    global game_over
    # Set the game_over flag to True
    game_over = True
    # Update the flashcard label to indicate the end of the game
    flashcard_label.configure(text="Game Over!")
    # Disable the start and check buttons to prevent further interaction
    start_button["state"] = "disabled"
    check_button["state"] = "disabled"
    # Clear the result label
    result_label["text"] = ""

# Function to reset game counts and prepare for a new game
def reset_counts():
    # Access global variables
    global total_questions,correct_questions,incorrect_questions,game_over,level

    # Get the selected level value from the GUI
    level_val = level.get()
    # Check if a level is selected, if not, display an error message
    if level_val == 0:
        result_label["text"] = "Please select a level first and press Start"
        result_label["foreground"] = "red"
        return
    else:
        result_label["text"] = ""

    # Reset game-related counts and flags
    total_questions = 0
    correct_questions = 0
    incorrect_questions = 0
    game_over = False

    # Clear the result label
    result_label["text"] = ""
    # Enable the start and check buttons for a new game
    start_button["state"] = "normal"
    check_button["state"] = "normal"

    # Clear the flashcard label and question log
    flashcard_label.configure(text="")
    question_log.delete(1.0, END)

    # Reset a specific counter variable related to the generation of flashcards
    generate_flashcard.questions_answered = 0

    # Hide the correct label from the previous question
    correctLbl1.grid_forget()

    # Generate a new flashcard and update game statistics
    generate_flashcard()
    update_stats()

# Function to restart the game, resetting counts and preparing for a new game
def restart_game():
    # Access global variables
    global total_questions, correct_questions, incorrect_questions, game_over

    # Reset game-related counts and flags
    total_questions = 0
    correct_questions = 0
    incorrect_questions = 0
    game_over = False

    # Get the selected level value from the GUI
    level_val = level.get()
    # Check if a level is selected, if not, display an error message
    if level_val == 0:
        result_label["text"] = "Please select a level first and press Start"
        result_label["foreground"] = "red"
        return
    else:
        result_label["text"] = ""

    # Hide the correct label from the previous question
    correctLbl1.grid_forget()

    # Update game statistics
    update_stats()

    # Clear the flashcard label and question log
    flashcard_label.configure(text="")
    question_log.delete(1.0, END)

    # Generate a new flashcard
    generate_flashcard()

    # Clear the result label
    result_label["text"] = ""


# Function to create the main window for the application
def create_main_window():
    # Create a Tkinter window
    window = Tk()
    # Set the title of the window
    window.title("Math Flashcards")
    return window

# Function to create the label for displaying flashcards in the window
def create_flashcard_label(window):
    # Create a Label widget with specified font and grid settings
    label = Label(window, text="", font=("Arial", 18))
    label.grid(row=0, column=0, columnspan=2, pady=10)
    return label

# Function to create the entry widget for user answers in the window
def create_answer_entry(window):
    # Create an Entry widget with specified width, font, and grid settings
    entry = Entry(window, width=5, font=("Arial", 16))
    entry.grid(row=1, column=0, padx=5)
    return entry

# Function to create the Start button in the window
def create_start_button(window):
    # Create a Button widget with specified text, background color, and
    # command (linked function)
    button = Button(window, text="Start", bg="lightblue", command=start_game)
    button.grid(row=1, column=1, padx=5)
    return button

# Function to create the Check Answer button in the window
def create_check_button(window):
    # Create a Button widget with specified text and command (linked function)
    button = Button(window, text="Check Answer", command=check_answer)
    button.grid(row=2, column=0, columnspan=2, pady=10)
    return button

# Function to create the Reset Counts button in the window
def create_reset_button(window):
    # Create a Button widget with specified text and command (linked function)
    button = Button(window, text="Reset Counts", command=reset_counts)
    button.grid(row=2, column=1, pady=10)

# Function to create the Restart Game button in the window
def create_restart_button(window):
    # Create a Button widget with specified text and command (linked function)
    button = Button(window, text="Restart Game", command=restart_game)
    button.grid(row=9, column=0, columnspan=2, pady=10)
    return button

# Function to create the label for displaying results in the window
def create_result_label(window):
    # Create a Label widget with specified font and grid settings
    label = Label(window, text="", font=("Arial", 14))
    label.grid(row=3, column=0, columnspan=2)
    return label

# Function to start the game by generating a new flashcard if the game is not
# over
def start_game():
    # Access the global variable
    global game_over
    # Check if the game is already over; if yes, exit the function
    if game_over:
        return
    # If the game is not over, generate a new flashcard to continue the game
    generate_flashcard()

# Function to create a question log in the window
def create_question_log(window):
    # Create a Label for the question log with specified text and font
    label = Label(window, text="Question Log", font=("Arial", 16))
    label.grid(row=5, column=0, columnspan=2, pady=5)

    # Create a ScrolledText widget for the question log with specified width
    # and height
    txt = scrolledtext.ScrolledText(window, width=40, height=10)
    txt.grid(row=6, column=0, columnspan=2, pady=10)

    # Return the ScrolledText widget, allowing it to be accessed outside the
    # function
    return txt


# Function to create radio buttons for selecting complexity levels in the window
def create_radio_buttons(window):
    # Create a Label for the radio buttons with specified text and font
    label = Label(window, text="Select Complexity Level", font=("Arial", 14))
    label.grid(row=7, column=0, columnspan=4, pady=5, sticky='w')

    # Create RadioButtons for different complexity levels with corresponding
    # values and the shared 'level' variable
    rad1 = Radiobutton(window, text='Level 1 (1-3)', value=1, variable=level)
    rad2 = Radiobutton(window, text='Level 2 (1-6)', value=2, variable=level)
    rad3 = Radiobutton(window, text='Level 3 (1-9)', value=3, variable=level)
    rad4 = Radiobutton(window, text='Level 4 (1-12)', value=4, variable=level)
    rad5 = Radiobutton(window, text='Level 5 (negative numbers)', value=5, \
                       variable=level)
    
    # Grid placement for each RadioButton with sticky and padx settings
    rad1.grid(row=8, column=0, sticky='w', padx=(5, 0))
    rad2.grid(row=8, column=1, sticky='w', padx=(5, 0))
    rad3.grid(row=8, column=2, sticky='w', padx=(5, 0))
    rad4.grid(row=8, column=3, sticky='w', padx=(5, 0))
    rad5.grid(row=8, column=4, sticky='w', padx=(5, 0))

# Function to create a label displaying game statistics in the window
def create_stats_label(window):
    # Create a Label for the statistics with specified text and font
    stats_label = Label(window, text="Statistics", font=("Arial", 14))
    stats_label.grid(row=11, column=0, columnspan=2, pady=5)

    # Create a Label for displaying the actual statistics using the
    # 'stats_text' variable
    stats_display = Label(window, textvariable=stats_text, font=("Arial", 12))
    stats_display.grid(row=12, column=0, columnspan=2)

    # Call the update_stats() function to initialize and display the initial
    # statistics
    update_stats()



# These lines of code initialize and create GUI elements for a math flashcards
# application.
# They include labels, entry widgets, buttons, and a scrolled text widget.
# The elements are associated with corresponding variables for further
# interaction and display.
flashcard_label = create_flashcard_label(window)
answer_entry = create_answer_entry(window)
start_button = create_start_button(window)
check_button = create_check_button(window)
reset_button = create_reset_button(window)
restart_button = create_restart_button(window)
result_label = create_result_label(window)
question_log = create_question_log(window)

# Create a label for displaying correctness feedback with a green background
# and bold Arial font.
correctLbl1 = Label(window, text="Correct", background='green', \
                    font=("Arial Bold", 20))

# Create an IntVar to store the selected complexity level.
level = IntVar()

# Call the function to create radio buttons for selecting complexity levels
# in the window.
create_radio_buttons(window)

# Create a StringVar for displaying game statistics and call the function to
# create a stats label in the window.
stats_text = StringVar()
create_stats_label(window)

# Call the function to update and display initial game statistics.
update_stats()

# Run the Tkinter main event loop to start the GUI application.
window.mainloop()



