import gradio as gr
import os
from google import genai
from google.genai import types
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
personalities = {
    "Friendly😊": "You are a helpful and friendly study assistant.",
    "Academic🎓": "You are a rigorous academic researcher.",
    "Mentor💡": "You are an experienced mentor.",
    "Motivational🔥": "You are a motivational coach."
}
def study_assistant(question, persona_name):
    system_prompt = personalities.get(persona_name, "You are a helpful assistant.")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7
            ),
            contents=question
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
# We tell Gradio to look for the 'style.css' file we created
with gr.Blocks(css="style.css", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📚 AI Study Assistant")
    with gr.Column():
        question_input = gr.Textbox(lines=4, label="Your Question")
        persona_dropdown = gr.Radio(choices=list(personalities.keys()), value="Friendly 😊", label="Assistant Personality")
        submit_btn = gr.Button("Get Expert Answer 🚀", variant="primary")
        
    output_text = gr.Textbox(label="AI Response", interactive=False)

    submit_btn.click(fn=study_assistant, inputs=[question_input, persona_dropdown], outputs=output_text)

if __name__ == "__main__":
    demo.launch()
