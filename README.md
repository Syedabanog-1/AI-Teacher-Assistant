:

🎯 Objective

The objective of this project is to build an interactive AI-based Teacher Assistant that creates a student profile and answers subject-related questions according to the student’s academic level using OpenAI models.

✨ Features

Student Profile Creation
Collects student details like name, academic institute, class, and subject in a structured format.

Automatic Academic Level Detection
Determines academic level (Primary, Secondary, Matric, Intermediate, Graduation, etc.) based on class number.

AI-Powered Q&A
Students can ask subject-related questions, and AI responds according to their academic level.

Dynamic Options

Ask a Question

Change Subject

Change Student

Quit Session

OpenAI Integration
Uses GPT models to generate context-aware, academic-level-specific answers.

⚙️ Workflow

Program starts → Student Profile is collected.

Profile is displayed in JSON format.

User gets options (Ask Question / Change Subject / Change Student / Quit).

If a question is asked → AI responds using the student’s profile context.

If subject or student is changed → System updates the profile.

Loop continues until user quits.

📊 Flow Chart Diagram
         ┌─────────────────────┐
         │   Start Program     │
         └─────────┬──────────┘
                   │
                   ▼
     ┌────────────────────────────┐
     │ Collect Student Profile    │
     └─────────┬─────────────────┘
               │
               ▼
     ┌────────────────────────────┐
     │  Show Options Menu         │
     │  1) Ask Q  2) Change Sub   │
     │  3) Change Student  4)Quit │
     └─────────┬─────────────────┘
               │
 ┌─────────────┼───────────────────────┐
 │             │                       │
 ▼             ▼                       ▼
Ask Question  Change Subject      Change Student
 │             │                       │
 ▼             ▼                       ▼
Send Q to AI  Update Subject      Update Profile
 │             │                       │
 ▼             ▼                       ▼
Return Answer ─────────────────────────┘
               │
               ▼
        Quit Option Selected?
               │
        ┌──────┴──────┐
        │             │
       Yes           No
        │             │
        ▼             └──► Go Back to Options
┌─────────────────────┐
│   End Program       │
└─────────────────────┘

https://github.com/user-attachments/assets/99c51d02-7357-45af-813c-e427dcf70905
https://ai-teacher-assistant-shcyauotifsqnzxhzer5kb.streamlit.app/



