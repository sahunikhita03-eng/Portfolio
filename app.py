from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Add your proper resume text here once available!
RESUME_DATA = """
Name: Nikhil
Role: Software Developer & Designer
Experience: 
- Developed full-stack web applications using Python, Flask, React, and Node.js.
- Strong UI/UX design background focused on intuitive visual experiences.
Skills: HTML, CSS, JavaScript, Python, Flask, UI/UX Design, REST APIs, Git.
Education: Bachelor's in Computer Science.
Projects:
- Portfolio Dashboard: A modern, unscrollable portfolio with an integrated AI chatbot.
- E-Commerce Platform: Scalable backend with real-time inventory tracking.
Contact: nikhil@example.com
Other: I love creating colorful, immersive web experiences with beautiful micro-animations.
"""

SYSTEM_PROMPT = f"""
You are an AI assistant integrated into Nikhil's personal portfolio website. 
Your ONLY job is to answer questions strictly based on the following resume data. 
Do not hallucinate. If the user asks something not in the resume, politely explain that you do not have that information and suggest they contact Nikhil directly at his email.
Keep your answers concise, friendly, and professional.

Resume Data for Context:
{RESUME_DATA}
"""

@app.route('/')
def index():
      return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
      data = request.json
      user_message = data.get('message', '')

    if not user_message:
              return jsonify({"reply": "Please ask a question."})

    try:
              chat_completion = client.chat.completions.create(
                            messages=[
                                              {
                                                                    "role": "system",
                                                                    "content": SYSTEM_PROMPT,
                                              },
                                              {
                                                                    "role": "user",
                                                                    "content": user_message,
                                              }
                            ],
                            # We are using LLaMA 3.1 8b via Groq for high-speed portfolio answering
                            model="llama-3.1-8b-instant",
                            temperature=0.7,
                            max_tokens=256,
              )
              reply = chat_completion.choices[0].message.content
              return jsonify({"reply": reply})
except Exception as e:
          return jsonify({"reply": f"Sorry, I encountered an error communicating securely: {str(e)}"}), 500

if __name__ == '__main__':
      app.
