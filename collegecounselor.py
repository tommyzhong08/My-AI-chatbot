from flask import Flask
from flask import request
from openai import OpenAI
app = Flask(__name__)

client = OpenAI(api_key="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")
@app.route("/")
def home():
    with open("collegecounselor.html") as f:
        return f.read()

@app.route("/math")
@app.route("/math.html")
def student_calculator():
    with open("math.html") as f:
        return f.read()


@app.route("/notes")
@app.route("/notes.html")
def notes_page():
    with open("Notes.html", encoding="utf-8") as f:
        return f.read()


def generate_voice_answers(question, extra_info=''):
    prompt_content = question
    if extra_info:
        prompt_content += "\n\nAdditional context: " + extra_info

    # Joseph John Junior III - Complex and EXTREMELY LONG
    response_joseph = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                Your name is Joseph John Junior III,
                you are a kind college counselor that teaches college students,
                you like teaching,
                everything you say is extremely complicated to understand and even someone as smart as Albert Einstein couldn't understand,
                all answers must be at least 15 lines long and extremely detailed and exhaustive,
                everysingle word you say must the most advanced way of saying that word,
                your IQ is 670,
                you never give a perfectly straightforward answer, instead, you give the student a answer where they have to figure out the rest,
                """
            },
            {
                "role": "user",
                "content": prompt_content
            }
        ]
    )
    answer_joseph = response_joseph.choices[0].message.content

    # Symphorian - Straightforward but complex/sophisticated - MEDIUM LENGTH
    response_symphorian = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                Your name is Symphorian, you are a college counselor with sophisticated and complex thinking.
                You provide direct, straightforward answers but use elevated and nuanced language.
                Your answers should be medium length, approximately 7-10 lines long.
                You use fairly simple words.
                Your answers are clear and understandable, yet intellectually rigorous.
                You explain concepts thoroughly with depth and precision.
                You use academic and professional terminology where appropriate.
                You balance clarity with intellectual sophistication.
                You think about multiple perspectives and provide comprehensive insights.
                """
            },
            {
                "role": "user",
                "content": prompt_content
            }
        ]
    )
    answer_symphorian = response_symphorian.choices[0].message.content

    # Andromeda - Simple and straightforward - SHORT
    response_andromeda = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                Your name is Andromeda, you are a college counselor who gives simple, direct, and easy-to-understand answers.
                You avoid complex jargon and overly complicated explanations.
                You get straight to the point and provide practical, actionable advice.
                Your answers should be short and concise, approximately 3-5 lines long.
                Your answers are clear and accessible to everyone.
                You break down complex ideas into simple terms.
                You focus on clarity and straightforwardness above all else.
                """
            },
            {
                "role": "user",
                "content": prompt_content
            }
        ]
    )
    answer_andromeda = response_andromeda.choices[0].message.content

    return answer_joseph, answer_symphorian, answer_andromeda


@app.route("/ask")    
def ask():
   question = request.args.get("question")

   with open("answer.html", encoding="utf-8") as f:
       html = f.read()

   html = html.replace("QUESTION_HERE", question)
   
   answer_joseph, answer_symphorian, answer_andromeda = generate_voice_answers(question)

   # Embed all three answers as data attributes
   html = html.replace("ANSWER_HERE", answer_joseph)
   html = html.replace("<!-- VOICE_ANSWERS -->", f"""<!-- VOICE_ANSWERS -->
<script>
const voiceAnswers = {{
    joseph: {repr(answer_joseph)},
    symphorian: {repr(answer_symphorian)},
    andromeda: {repr(answer_andromeda)}
}};
</script>""")
   
   return html
 
if __name__ == "__main__":
    app.run(debug = True, host = "127.0.0.1", port = 5500)
