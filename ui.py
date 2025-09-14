<<<<<<< HEAD
import streamlit as st
import json
import os
from dataclasses import dataclass, asdict
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Teacher Assistant",
    page_icon="🧑‍🏫",
    layout="wide"
)

# Get API key - works for both local and cloud deployment
def get_api_key():
    # Try Streamlit secrets first (for cloud deployment)
    try:
        return st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        # Fallback to environment variable (for local development)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("❌ OPENAI_API_KEY not found. Please set it in environment variables or Streamlit secrets.")
            st.info("""
            **For Local Development:**
            1. Create a `.env` file in your project directory
            2. Add: `OPENAI_API_KEY=your_api_key_here`
            
            **For Streamlit Cloud:**
            1. Go to App Settings
            2. Add OPENAI_API_KEY in Secrets section
            """)
            st.stop()
        return api_key

def get_model_name():
    try:
        return st.secrets.get("MODEL_NAME", "gpt-4o-mini")
    except (KeyError, FileNotFoundError):
        return os.getenv("MODEL_NAME", "gpt-4o-mini")

# Initialize OpenAI client
try:
    client = OpenAI(api_key=get_api_key())
    MODEL_NAME = get_model_name()
except Exception as e:
    st.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
    st.stop()

@dataclass
class StudentProfile:
    Student_Name: str
    Academic_Name: str
    Academic_Level: str
    Class: int
    Subject: str

# Map Class → Academic Level
def get_academic_level(class_num: int) -> str:
    if 1 <= class_num <= 5:
        return "Primary"
    elif 6 <= class_num <= 8:
        return "Secondary"
    elif class_num == 9:
        return "Middle"
    elif class_num == 10:
        return "Matric"
    elif class_num in [11, 12]:
        return "Intermediate"
    elif 13 <= class_num <= 16:
        return "Graduation"
    elif class_num == 17:
        return "Master"
    elif class_num == 18:
        return "Ph.D"
    else:
        return "High Level"

# Ask OpenAI for Answer
def ask_openai(question: str, profile: StudentProfile) -> str:
    try:
        prompt = (
            f"The student profile is: {json.dumps(asdict(profile))}.\n"
            f"The student has asked: {question}\n"
            f"Please answer according to the student's Academic_Level ({profile.Academic_Level})."
        )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful teacher assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error getting response: {str(e)}"

# Initialize session state
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'current_option' not in st.session_state:
    st.session_state.current_option = "profile"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def main():
    # Header
    st.title("🧑‍🏫 AI Teacher Assistant")
    st.markdown("### Get personalized answers based on your academic level!")
    st.divider()
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("📋 Menu")
        
        # Navigation buttons
        if st.button("👤 Student Profile", use_container_width=True):
            st.session_state.current_option = "profile"
        
        if st.button("❓ Ask Question", use_container_width=True, disabled=st.session_state.profile is None):
            st.session_state.current_option = "ask"
            
        if st.button("📚 Change Subject", use_container_width=True, disabled=st.session_state.profile is None):
            st.session_state.current_option = "subject"
            
        if st.button("🔄 Change Student", use_container_width=True):
            st.session_state.current_option = "change_student"
            
        st.divider()
        
        # Current Profile Display
        if st.session_state.profile:
            st.subheader("📖 Current Profile")
            profile = st.session_state.profile
            st.info(f"""
            **Name:** {profile.Student_Name}
            **Institution:** {profile.Academic_Name}
            **Level:** {profile.Academic_Level}
            **Class:** {profile.Class}
            **Subject:** {profile.Subject}
            """)
        else:
            st.warning("⚠️ No profile created yet!")
    
    # Main content area
    if st.session_state.current_option == "profile" or st.session_state.profile is None:
        show_profile_section()
    elif st.session_state.current_option == "ask":
        show_ask_question_section()
    elif st.session_state.current_option == "subject":
        show_change_subject_section()
    elif st.session_state.current_option == "change_student":
        show_change_student_section()

def show_profile_section():
    st.header("👤 Student Profile")
    
    if st.session_state.profile is None:
        st.info("📝 Please create a student profile to get started!")
    
    with st.form("profile_form"):
        st.subheader("📋 Enter Student Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Student Name *",
                value=st.session_state.profile.Student_Name if st.session_state.profile else "",
                placeholder="Enter student name"
            )
            academic_name = st.text_input(
                "Academic Institution *",
                value=st.session_state.profile.Academic_Name if st.session_state.profile else "",
                placeholder="School/College/University name"
            )
        
        with col2:
            class_num = st.number_input(
                "Class *",
                min_value=1,
                max_value=20,
                value=st.session_state.profile.Class if st.session_state.profile else 10,
                help="Enter class number (1-20)"
            )
            subject = st.text_input(
                "Subject *",
                value=st.session_state.profile.Subject if st.session_state.profile else "",
                placeholder="Mathematics, Physics, Chemistry, etc."
            )
        
        # Academic level preview
        if class_num:
            level = get_academic_level(class_num)
            st.info(f"📊 Academic Level: **{level}**")
        
        submitted = st.form_submit_button("✅ Create/Update Profile", use_container_width=True)
        
        if submitted:
            if name and academic_name and subject:
                level = get_academic_level(class_num)
                st.session_state.profile = StudentProfile(
                    Student_Name=name,
                    Academic_Name=academic_name,
                    Academic_Level=level,
                    Class=class_num,
                    Subject=subject,
                )
                st.success("✅ Profile created/updated successfully!")
                st.balloons()
                
                # Show profile summary
                st.subheader("📘 Profile Summary")
                st.json(asdict(st.session_state.profile))
                
            else:
                st.error("❌ Please fill all required fields!")

def show_ask_question_section():
    st.header("❓ Ask Your Question")
    
    if st.session_state.profile:
        profile = st.session_state.profile
        st.success(f"🎯 Ready to answer questions for **{profile.Student_Name}** ({profile.Academic_Level} level)")
        
        with st.form("question_form"):
            question = st.text_area(
                f"Ask anything about {profile.Subject}:",
                placeholder=f"Type your {profile.Subject} question here...",
                height=100
            )
            
            ask_button = st.form_submit_button("🚀 Get Answer", use_container_width=True)
            
            if ask_button and question:
                with st.spinner("🤔 AI Teacher is thinking..."):
                    answer = ask_openai(question, profile)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'question': question,
                    'answer': answer,
                    'timestamp': st.session_state.get('chat_count', 0) + 1
                })
                st.session_state.chat_count = st.session_state.get('chat_count', 0) + 1
                
                # Display answer
                st.subheader("🧑‍🏫 Teacher's Answer:")
                st.markdown(f"**Question:** {question}")
                st.markdown("**Answer:**")
                st.info(answer)
        
        # Chat History
        if st.session_state.chat_history:
            st.divider()
            st.subheader("📚 Previous Questions & Answers")
            
            # Clear history button
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()
            
            # Display chat history
            for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
                with st.expander(f"Q{len(st.session_state.chat_history) - i + 1}: {chat['question'][:60]}..." if len(chat['question']) > 60 else f"Q{len(st.session_state.chat_history) - i + 1}: {chat['question']}"):
                    st.markdown(f"**❓ Question:** {chat['question']}")
                    st.markdown(f"**💡 Answer:** {chat['answer']}")

def show_change_subject_section():
    st.header("📚 Change Subject")
    
    if st.session_state.profile:
        current_subject = st.session_state.profile.Subject
        st.info(f"Current Subject: **{current_subject}**")
        
        with st.form("subject_form"):
            new_subject = st.text_input(
                "Enter New Subject:",
                value=current_subject,
                placeholder="Mathematics, Physics, Chemistry, etc."
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("✅ Update Subject", use_container_width=True):
                    if new_subject:
                        st.session_state.profile.Subject = new_subject
                        st.success(f"✅ Subject changed to: **{new_subject}**")
                        st.balloons()
                    else:
                        st.error("❌ Please enter a subject name!")
            
            with col2:
                if st.form_submit_button("🔄 Reset to Original", use_container_width=True):
                    st.session_state.profile.Subject = current_subject
                    st.info("Subject reset to original value")

def show_change_student_section():
    st.header("🔄 Change Student Profile")
    
    st.warning("⚠️ Creating a new student profile will clear the current profile and chat history.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Create New Profile", use_container_width=True):
            st.session_state.profile = None
            st.session_state.chat_history = []
            st.session_state.current_option = "profile"
            st.success("Ready to create new profile!")
            st.rerun()
    
    with col2:
        if st.button("📝 Edit Current Profile", use_container_width=True):
            st.session_state.current_option = "profile"
            st.rerun()
    
    with col3:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.current_option = "ask"
            st.rerun()
    
    # Show current profile for reference
    if st.session_state.profile:
        st.divider()
        st.subheader("📖 Current Profile")
        st.json(asdict(st.session_state.profile))

if __name__ == "__main__":
=======
import streamlit as st
import json
from dataclasses import dataclass, asdict
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="AI Teacher Assistant",
    page_icon="🧑‍🏫",
    layout="wide"
)

# Streamlit secrets se API key get karo
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    MODEL_NAME = st.secrets.get("MODEL_NAME", "gpt-4o-mini")
except KeyError:
    st.error("❌ OPENAI_API_KEY not found in secrets. Please add it in Streamlit Cloud settings.")
    st.stop()

@dataclass
class StudentProfile:
    Student_Name: str
    Academic_Name: str
    Academic_Level: str
    Class: int
    Subject: str

# Map Class → Academic Level
def get_academic_level(class_num: int) -> str:
    if 1 <= class_num <= 5:
        return "Primary"
    elif 6 <= class_num <= 8:
        return "Secondary"
    elif class_num == 9:
        return "Middle"
    elif class_num == 10:
        return "Matric"
    elif class_num in [11, 12]:
        return "Intermediate"
    elif 13 <= class_num <= 16:
        return "Graduation"
    elif class_num == 17:
        return "Master"
    elif class_num == 18:
        return "Ph.D"
    else:
        return "High Level"

# Ask OpenAI for Answer
def ask_openai(question: str, profile: StudentProfile) -> str:
    try:
        prompt = (
            f"The student profile is: {json.dumps(asdict(profile))}.\n"
            f"The student has asked: {question}\n"
            f"Please answer according to the student's Academic_Level ({profile.Academic_Level})."
        )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful teacher assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error getting response: {str(e)}"

# Initialize session state
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'current_option' not in st.session_state:
    st.session_state.current_option = "profile"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def main():
    # Header
    st.title("🧑‍🏫 AI Teacher Assistant")
    st.markdown("### Get personalized answers based on your academic level!")
    st.divider()
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("📋 Menu")
        
        # Navigation buttons
        if st.button("👤 Student Profile", use_container_width=True):
            st.session_state.current_option = "profile"
        
        if st.button("❓ Ask Question", use_container_width=True, disabled=st.session_state.profile is None):
            st.session_state.current_option = "ask"
            
        if st.button("📚 Change Subject", use_container_width=True, disabled=st.session_state.profile is None):
            st.session_state.current_option = "subject"
            
        if st.button("🔄 Change Student", use_container_width=True):
            st.session_state.current_option = "change_student"
            
        st.divider()
        
        # Current Profile Display
        if st.session_state.profile:
            st.subheader("📖 Current Profile")
            profile = st.session_state.profile
            st.info(f"""
            **Name:** {profile.Student_Name}
            **Institution:** {profile.Academic_Name}
            **Level:** {profile.Academic_Level}
            **Class:** {profile.Class}
            **Subject:** {profile.Subject}
            """)
        else:
            st.warning("⚠️ No profile created yet!")
    
    # Main content area
    if st.session_state.current_option == "profile" or st.session_state.profile is None:
        show_profile_section()
    elif st.session_state.current_option == "ask":
        show_ask_question_section()
    elif st.session_state.current_option == "subject":
        show_change_subject_section()
    elif st.session_state.current_option == "change_student":
        show_change_student_section()

def show_profile_section():
    st.header("👤 Student Profile")
    
    if st.session_state.profile is None:
        st.info("📝 Please create a student profile to get started!")
    
    with st.form("profile_form"):
        st.subheader("📋 Enter Student Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Student Name *",
                value=st.session_state.profile.Student_Name if st.session_state.profile else "",
                placeholder="Enter student name"
            )
            academic_name = st.text_input(
                "Academic Institution *",
                value=st.session_state.profile.Academic_Name if st.session_state.profile else "",
                placeholder="School/College/University name"
            )
        
        with col2:
            class_num = st.number_input(
                "Class *",
                min_value=1,
                max_value=20,
                value=st.session_state.profile.Class if st.session_state.profile else 10,
                help="Enter class number (1-20)"
            )
            subject = st.text_input(
                "Subject *",
                value=st.session_state.profile.Subject if st.session_state.profile else "",
                placeholder="Mathematics, Physics, Chemistry, etc."
            )
        
        # Academic level preview
        if class_num:
            level = get_academic_level(class_num)
            st.info(f"📊 Academic Level: **{level}**")
        
        submitted = st.form_submit_button("✅ Create/Update Profile", use_container_width=True)
        
        if submitted:
            if name and academic_name and subject:
                level = get_academic_level(class_num)
                st.session_state.profile = StudentProfile(
                    Student_Name=name,
                    Academic_Name=academic_name,
                    Academic_Level=level,
                    Class=class_num,
                    Subject=subject,
                )
                st.success("✅ Profile created/updated successfully!")
                st.balloons()
                
                # Show profile summary
                st.subheader("📘 Profile Summary")
                st.json(asdict(st.session_state.profile))
                
            else:
                st.error("❌ Please fill all required fields!")

def show_ask_question_section():
    st.header("❓ Ask Your Question")
    
    if st.session_state.profile:
        profile = st.session_state.profile
        st.success(f"🎯 Ready to answer questions for **{profile.Student_Name}** ({profile.Academic_Level} level)")
        
        with st.form("question_form"):
            question = st.text_area(
                f"Ask anything about {profile.Subject}:",
                placeholder=f"Type your {profile.Subject} question here...",
                height=100
            )
            
            ask_button = st.form_submit_button("🚀 Get Answer", use_container_width=True)
            
            if ask_button and question:
                with st.spinner("🤔 AI Teacher is thinking..."):
                    answer = ask_openai(question, profile)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'question': question,
                    'answer': answer,
                    'timestamp': st.session_state.get('chat_count', 0) + 1
                })
                st.session_state.chat_count = st.session_state.get('chat_count', 0) + 1
                
                # Display answer
                st.subheader("🧑‍🏫 Teacher's Answer:")
                st.markdown(f"**Question:** {question}")
                st.markdown("**Answer:**")
                st.info(answer)
        
        # Chat History
        if st.session_state.chat_history:
            st.divider()
            st.subheader("📚 Previous Questions & Answers")
            
            # Clear history button
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()
            
            # Display chat history
            for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
                with st.expander(f"Q{len(st.session_state.chat_history) - i + 1}: {chat['question'][:60]}..." if len(chat['question']) > 60 else f"Q{len(st.session_state.chat_history) - i + 1}: {chat['question']}"):
                    st.markdown(f"**❓ Question:** {chat['question']}")
                    st.markdown(f"**💡 Answer:** {chat['answer']}")

def show_change_subject_section():
    st.header("📚 Change Subject")
    
    if st.session_state.profile:
        current_subject = st.session_state.profile.Subject
        st.info(f"Current Subject: **{current_subject}**")
        
        with st.form("subject_form"):
            new_subject = st.text_input(
                "Enter New Subject:",
                value=current_subject,
                placeholder="Mathematics, Physics, Chemistry, etc."
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("✅ Update Subject", use_container_width=True):
                    if new_subject:
                        st.session_state.profile.Subject = new_subject
                        st.success(f"✅ Subject changed to: **{new_subject}**")
                        st.balloons()
                    else:
                        st.error("❌ Please enter a subject name!")
            
            with col2:
                if st.form_submit_button("🔄 Reset to Original", use_container_width=True):
                    st.session_state.profile.Subject = current_subject
                    st.info("Subject reset to original value")

def show_change_student_section():
    st.header("🔄 Change Student Profile")
    
    st.warning("⚠️ Creating a new student profile will clear the current profile and chat history.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Create New Profile", use_container_width=True):
            st.session_state.profile = None
            st.session_state.chat_history = []
            st.session_state.current_option = "profile"
            st.success("Ready to create new profile!")
            st.rerun()
    
    with col2:
        if st.button("📝 Edit Current Profile", use_container_width=True):
            st.session_state.current_option = "profile"
            st.rerun()
    
    with col3:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.current_option = "ask"
            st.rerun()
    
    # Show current profile for reference
    if st.session_state.profile:
        st.divider()
        st.subheader("📖 Current Profile")
        st.json(asdict(st.session_state.profile))

if __name__ == "__main__":
main()