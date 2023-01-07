from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
import os

def add_expense(msg):
    try:
        expense_name = msg.split(" ")[2]
        expense_value = msg.split(" ")[1]
        expense_data = [expense_name, expense_value]
        print(expense_name, expense_value)
        df = pd.DataFrame(data=[expense_data])
        df.to_csv('expenses/expenses.csv', mode='a', index=None, header=False)
        return "Se agrego gasto correctamente"
    except:
        return "Error al agregar gasto"

def make_report():
    try:
        expenses_csv = pd.read_csv("expenses/expenses.csv")
        total_expense = 0
        message = ""
        for expense in expenses_csv.values:
            message += expense[0] + " - $" + str(expense[1]) + "\n"
            total_expense += expense[1]
        return message + "\nGasto total - $" + str(total_expense)
    except:
        return "Error al hacer reporte"

def reset_expenses():
    try:
        os.remove("expenses/expenses.csv")
        new_csv = pd.DataFrame(columns=["expense_name", "expense_value"], data=[])
        new_csv.to_csv("expenses/expenses.csv", index=None)
        return "Gastos reiniciados"
    except:
        "Error al reiniciar gastos"

app = Flask(__name__)

@app.route("/wasms", methods=['POST'])
def wa_sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message

    msg = request.form.get('Body').lower()  # Reading the message from the whatsapp

    resp = MessagingResponse()
    reply = resp.message()

    if "agregar" in msg.lower():
        reply.body(add_expense(msg))
    elif "reporte" in msg.lower():
        reply.body(make_report())
    elif "reiniciar gastos" in msg.lower():
        reply.body(reset_expenses())
    else:
        reply.body("Comando no encontrado")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)