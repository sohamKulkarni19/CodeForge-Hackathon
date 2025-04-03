import os
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
import re
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "stop_sequences": [
    "Lumos",
  ],
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction="You are a conversational ai report generator, your job is to extract all the following information from the user: 1) Problem description: affected equipments, materials or machines affected because of this, date and time of the problem occurance, location, the person who found the problem. 2) Action taken 3) Initial impact assessment 4)Investigation details: Investigation team with their names, ids, department, sequence of events done in the investigation, investigation outcome, 5) corrective and preventive actions, and their outcomes, 6) Review and Approval(who has reviewed and apporved it) and summarize it and only print it in the format of a json file, do not print the summary as normal text. do not ask all the questions at once, let the user type and ask follow up questions based on left out details one at a time. Once you're done with summarizing, make sure to say Lumos",
)

history = []

print('Bot: Hi how can i help you? say Lumos to end the conversation.')

while True:
    user_input = input("You: ")
    if user_input == "Lumos" or user_input == "lumos":
        break
    chat_session = model.start_chat(
        history=history
    )

    response= chat_session.send_message(user_input)

    model_response = response.text
    print(f'Bot: {model_response}')
    print()
    history.append({'role':'user','parts':[user_input]})
    history.append({'role':'model','parts':[model_response]})

response_text = history[-3]['parts'][0]
json_string = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)
data = json.loads(json_string)
pdf_filename = "report.pdf"
c = canvas.Canvas(pdf_filename, pagesize=letter)
c.setFont("Helvetica", 12)

# Write content to PDF
y = 750  
for key, value in data.items():
    c.drawString(100, y, f"{key}: {value}")
    y -= 20 

c.save()
print(f"PDF generated: {pdf_filename}")