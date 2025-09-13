
import os
import chainlit as cl
from ai_teacher_assistant import StudentProfile, map_class_to_academic_level, build_system_prompt, teacher_answer_question

# A very small stateful UI. Chainlit will show a chat-like interface.

@cl.on_chat_start
async def start():
    await cl.Message("Welcome to AI Teacher Assistant (Chainlit UI). Click the button to set up a student profile.").send()


@cl.action(name="Create Profile")
async def create_profile_action(obj, **kwargs):
    # In a real UI you'd collect inputs with forms; chainlit's UI forms are omitted here for brevity.
    # We'll prompt the user to type a JSON profile in chat, then parse it.
    await cl.Message("Please type your profile as JSON, for example:\n{\n  \"student_name\": \"Aisha\",\n  \"academic_name\": \"City High\",\n  \"student_class\": 10,\n  \"subject\": \"Physics\"\n}\n").send()


@cl.on_message
async def main(message: str):
    text = message
    # Attempt to detect a JSON profile first
    try:
        data = json.loads(text)
        if all(k in data for k in ("student_name", "student_class", "subject")):
            profile = StudentProfile(
                student_name=data.get("student_name"),
                academic_name=data.get("academic_name", "Unknown"),
                student_class=int(data.get("student_class")),
                academic_level=map_class_to_academic_level(int(data.get("student_class"))),
                subject=data.get("subject"),
                age=data.get("age")
            )
            await cl.Message(f"Profile set: {profile}").send()
            return
    except Exception:
        pass

    # Otherwise treat the message as a question and respond
    # NOTE: chainlit handlers can call synchronous functions but prefer async; for simplicity we call sync function
    try:
        # 'profile' would normally be stored per-session; here we use a placeholder
        # If you want full session state, integrate with a small DB or chainlit's state storage (not shown here).
        dummy_profile = StudentProfile("Student", "Unknown", 10, "Matric", "General")
        answer = teacher_answer_question(dummy_profile, text)
        await cl.Message(answer).send()
    except Exception as e:
        await cl.Message(f"Error processing question: {e}").send()
