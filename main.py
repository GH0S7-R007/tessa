import csv
import openai

# Set your OpenAI API key
openai.api_key = "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"


# Define a function to check CSV file for answers
def check_csv_file(prompt):
    with open('data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if prompt in row[0].lower():
                # Return answer from CSV file
                return row[1] if len(row) > 1 else None
        # Return None if prompt not found in CSV file
        return None


# Define a function to store new prompts and responses in CSV file
def store_in_csv(prompt, response):
    with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([prompt, response])


# Define a function to generate responses
def generate_response(prompt):
    # Check CSV file for answers
    response = check_csv_file(prompt)
    if response:
        return response
    else:
        # Fallback to OpenAI API if no relevant answers in CSV file
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        generated_text = response['choices'][0]['text']
        return generated_text


# Main loop to keep the chat bot running
while True:
    # Capture user input
    user_input = input("Question from User: ").lower()

    # Check if user wants to quit
    if user_input.lower() in ['quit', 'exit']:
        print("Goodbye!")
        break

    # Check if user wants to train the bot
    if user_input.lower() in ['train', 'add']:
        prompt = input("Enter any question to train me: ")
        response = input("Enter an answer for this. then i can keep in my mind: ")

        # Store prompt and response in CSV file
        store_in_csv(prompt, response)

        print("Thanks! noted this question.")
    else:
        # Generate response based on user input
        response = generate_response(user_input)
        print("Tessa: ", response)
