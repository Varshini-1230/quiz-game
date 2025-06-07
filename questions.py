import streamlit as st
import pandas as pd

# ---------------------- Load Questions from CSV ---------------------- #
@st.cache_data
def load_quiz_data(csv_path):
    df = pd.read_csv(csv_path)
    quiz = []
    for _, row in df.iterrows():
        quiz.append({
            "question": row["question"],
            "options": [row["option1"], row["option2"], row["option3"], row["option4"]],
            "answer": row["answer"],
            "category": row["category"]
        })
    return quiz

quiz_data = load_quiz_data(r"C:\Users\Mahesh\Downloads\quiz game\questions.csv")

# ---------------------- Initialize Session State ---------------------- #
if "started" not in st.session_state:
    st.session_state.started = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = []

# ---------------------- UI Begins ---------------------- #
st.title("🧠 Quiz Game")

# ---------------------- Start Screen ---------------------- #
if not st.session_state.started:
    st.write("Welcome to the interactive quiz game! Test your knowledge across various topics.")
    st.image(r"C:\Users\Mahesh\Downloads\quiz gif.png", width=300)
    if st.button("🎯 Start Quiz"):
        st.session_state.started = True
        st.rerun()

# ---------------------- Quiz Logic ---------------------- #
else:
    if st.session_state.question_index < len(quiz_data):
        q = quiz_data[st.session_state.question_index]
        st.subheader(f"Q{st.session_state.question_index + 1}: {q['question']}")
        selected = st.radio("Choose one:", q["options"], key=st.session_state.question_index)

        if st.button("Submit Answer"):
            st.session_state.answers.append({
                "question": q["question"],
                "selected": selected,
                "correct": q["answer"]
            })

            if selected == q["answer"]:
                st.session_state.score += 1
                st.success("Correct! ✅")
            else:
                st.error(f"Wrong! ❌ The correct answer is **{q['answer']}**.")

            st.session_state.question_index += 1
            st.rerun()

    else:
        st.balloons()
        st.header("🎉 Quiz Completed!")
        st.markdown(f"### 🏁 Your Score: `{st.session_state.score} / {len(quiz_data)}`")

        with st.expander("📋 Review Your Answers"):
            for i, ans in enumerate(st.session_state.answers):
                st.write(f"**Q{i+1}: {ans['question']}**")
                st.write(f"Your Answer: `{ans['selected']}`")
                st.write(f"Correct Answer: `{ans['correct']}`")
                st.markdown("---")

        if st.button("🔁 Restart Quiz"):
            st.session_state.started = False
            st.session_state.score = 0
            st.session_state.question_index = 0
            st.session_state.answers = []
            st.rerun()
