from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Store the selected operation
operation_selected = None

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    global operation_selected
    # Get the incoming message text
    incoming_msg = request.values.get('Body', '').strip()
    
    # Create a Twilio MessagingResponse object to send a reply
    response = MessagingResponse()
    msg = response.message()
    
    # Check if an operation has been selected
    if operation_selected is None:
        if incoming_msg in ["1", "2", "3", "4"]:
            # Set the operation based on user input
            operation_selected = incoming_msg
            msg.body("Please enter two numbers separated by space (e.g., 3 4):")
        else:
            # If no valid operation is selected, prompt user again
            msg.body("Welcome to the Calculator Bot! Please select an operation:\n"
                     "1. Addition\n"
                     "2. Subtraction\n"
                     "3. Multiplication\n"
                     "4. Division")
    else:
        try:
            # Perform the selected operation on the provided numbers
            num1, num2 = map(float, incoming_msg.split())
            if operation_selected == "1":
                result = num1 + num2
                operation_name = "Addition"
            elif operation_selected == "2":
                result = num1 - num2
                operation_name = "Subtraction"
            elif operation_selected == "3":
                result = num1 * num2
                operation_name = "Multiplication"
            elif operation_selected == "4":
                if num2 == 0:
                    msg.body("Error: Division by zero is not allowed. Please try again.")
                    operation_selected = None
                    return str(response)
                result = num1 / num2
                operation_name = "Division"
            
            msg.body(f"Result of {operation_name} of {num1} and {num2} is: {result}")
            operation_selected = None
        except ValueError:
            msg.body("Invalid input. Please enter two numbers separated by space (e.g., 3 4).")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
