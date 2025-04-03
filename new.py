import os
import google.generativeai as genai
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, scrolledtext

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
    system_instruction="You are a conversational ai report generator, your job is to extract all the following information from the user: 1) Problem description: affected equipments, materials or machines affected because of this, date and time of the problem occurance, location, the person who found the problem. 2) Action taken 3) Initial impact assessment 4)Investigation details: Investigation team with their names, ids, department, sequence of events done in the investigation, investigation outcome, 5) corrective and preventive actions, and their outcomes and summarize it into organized format. do not ask all the questions at once, let the user type and ask follow up questions based on left out details one at a time. Once you're done with summarizing, say Lumos",
)

class QuestionInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Report Generator AI")
        self.root.geometry("800x600")

        self.bg_color = "#2C3E50"
        self.accent_color = "#3498DB"
        self.text_color = "#ECF0F1"
        self.button_color = "#E74C3C"

        self.root.configure(bg=self.bg_color)

        style = ttk.Style()
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Helvetica", 12))
        style.configure("Question.TLabel", background=self.bg_color, foreground=self.accent_color, font=("Helvetica", 18, "bold"))
        style.configure("TButton", font=("Helvetica", 11, "bold"))

        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill="both", expand=True)

        self.question_frame = ttk.Frame(self.main_frame)
        self.question_frame.pack(fill="x", pady=(0, 20))

        self.question_label = ttk.Label(self.question_frame, text="Bot: Hi how can I help you?", style="Question.TLabel")
        self.question_label.pack()

        self.answer_frame = ttk.Frame(self.main_frame)
        self.answer_frame.pack(fill="x", pady=20)

        ttk.Frame(self.answer_frame, width=150).pack(side="left", fill="y")

        self.answer_entry = tk.Entry(self.answer_frame, width=50, bg="#34495E", fg=self.text_color, font=("Helvetica", 12), insertbackground=self.text_color, relief="flat")
        self.answer_entry.pack(side="left", padx=(0, 10))

        self.submit_button = tk.Button(self.answer_frame, text="Submit", command=self.submit_answer, bg=self.button_color, fg=self.text_color, font=("Helvetica", 11, "bold"), relief="flat", activebackground="#C0392B", activeforeground=self.text_color)
        self.submit_button.pack(side="left")

        ttk.Frame(self.answer_frame, width=150).pack(side="left", fill="y")

        self.history_frame = ttk.Frame(self.main_frame)
        self.history_frame.pack(fill="both", expand=True)

        ttk.Label(self.history_frame, text="History", font=("Helvetica", 16, "bold")).pack()

        self.history_text = scrolledtext.ScrolledText(self.history_frame, height=15, bg="#34495E", fg=self.text_color, font=("Helvetica", 11), relief="flat", wrap=tk.WORD)
        self.history_text.pack(fill="both", expand=True, pady=10)

        self.history = []

        self.root.bind('<Return>', lambda event: self.submit_answer())

    def submit_answer(self):
        user_input = self.answer_entry.get().strip()
        if user_input:
            self.history_text.insert(tk.END, f"You: {user_input}\n")
            self.history_text.see(tk.END)
            self.answer_entry.delete(0, tk.END)

            chat_session = model.start_chat(history=self.history)
            response = chat_session.send_message(user_input)
            model_response = response.text

            self.history_text.insert(tk.END, f"Bot: {model_response}\n{'-'*50}\n")
            self.history_text.see(tk.END)
            self.question_label.config(text=f"Bot: {model_response}")

            self.history.append({'role': 'user', 'parts': [user_input]})
            self.history.append({'role': 'model', 'parts': [model_response]})

def main():
    root = tk.Tk()
    app = QuestionInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()