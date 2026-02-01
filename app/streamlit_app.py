import sys
import os
import time
import streamlit as st

# ---------------- PATH FIX ----------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from core.evaluator import evaluate_news

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Fake News Detection",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.verdict-box {
    padding: 22px;
    border-radius: 14px;
    color: white;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
    animation: fadeIn 0.6s ease-in;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def verdict_style(verdict: str):
    styles = {
        "REAL": ("#2ecc71", "✅"),
        "LIKELY REAL": ("#27ae60", "🟢"),
        "UNVERIFIED": ("#f1c40f", "⚠️"),
        "UNVERIFIED (NO CONFIRMATION)": ("#e67e22", "🟠"),
        "FAKE": ("#e74c3c", "❌"),
    }
    return styles.get(verdict.upper(), ("#95a5a6", "❓"))

# ---------------- UI ----------------
st.title("📰 Fake News Detection System")
st.write("Verify news claims using **ML confidence + real-time trusted evidence**")

text = st.text_area(
    "Enter news claim",
    height=140,
    placeholder="FAKE NEWS Example: Pakistan won the cricket match against India"
)

# ---------------- VERIFY BUTTON ----------------
if st.button("🔍 Verify News"):

    # 1️⃣ Empty input handling
    if not text.strip():
        st.warning("⚠️ Please enter a news claim before verification.")
        st.stop()

    # 2️⃣ Loading animation
    with st.spinner("🧠 AI is analysing the news..."):
        time.sleep(0.8)
        result = evaluate_news(text)

    # ---------------- RESULTS ----------------
    verdict = result.get("final_verdict", "UNVERIFIED")
    ml_conf = result.get("ml_confidence", 0)
    flags = result.get("flags", [])
    evidence = result.get("evidence", [])

    color, emoji = verdict_style(verdict)

    # 3️⃣ Verdict display
    st.header("🎯 Final Verdict")
    st.markdown(
        f"""
        <div class="verdict-box" style="background-color:{color};">
            <br>
            {emoji} {verdict}<br><br>
            ML Confidence: {ml_conf:.1f} %
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # 4️⃣ Red flags
    if flags:
        st.subheader("⚠️ Red Flags")
        for f in flags:
            st.write(f"- {f}")

    # 5️⃣ Evidence handling
    st.subheader("📰 Evidence")

    if not evidence:
        st.info("📭 No verified evidence found from trusted news sources.")
    else:
        for e in evidence:
            if isinstance(e, dict):
                st.write(f"- {e.get('title', 'Unknown source')}")
            else:
                st.write(f"- {e}")

