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

# ---------------- VERDICT STYLING ----------------
def verdict_style(verdict: str):
    styles = {
        "REAL": ("#08ff6f", "✅"),
        "LIKELY_REAL (as one article found)": ("#33b159", "🟡"),
        "UNVERIFIED": ("#f1c40f", "⚠️"),
        "LIKELY_FAKE (NO_VERIFIED_EVIDENCE)": ("#ce2c2c", "❓"),
        "FAKE": ("#ff1900", "❌"),
    }
    return styles.get(verdict, ("#95a5a6", "❓"))

# ---------------- UI ----------------
st.title("📰 Fake News Detection System")
st.write("Verify news claims using **NLI reasoning + real-time trusted evidence**")

text = st.text_area(
    "Enter news claim",
    height=140,
    placeholder="Example: India lost the 2007 T20 World Cup final against Pakistan"
)

# ---------------- VERIFY BUTTON ----------------
if st.button("🔍 Verify News"):

    # 1️⃣ Empty input handling
    if not text.strip():
        st.warning("⚠️ Please enter a news claim before verification.")
        st.stop()

    # 2️⃣ Loading animation
    with st.spinner("🧠 AI is analysing the claim using real-time evidence..."):
        time.sleep(0.6)
        result = evaluate_news(text)

    # ---------------- RESULTS ----------------
    verdict = result.get("verdict", "UNVERIFIED")
    flags = result.get("flags", [])
    evidence = result.get("evidence", [])
    nli = result.get("nli", {})

    color, emoji = verdict_style(verdict)

    # 3️⃣ Verdict display
    st.header("🎯 Final Verdict")
    st.markdown(
        f"""
        <div class="verdict-box" style="background-color:{color};">
            {emoji} {verdict.replace("_", " ")}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # 4️⃣ Explanation
    st.subheader("🧠 Reasoning Summary")
    if nli:
        st.write(
            f"• Supporting articles: **{nli.get('support', 0)}**  \n"
            f"• Contradicting articles: **{nli.get('contradict', 0)}**  \n"
            f"• Neutral mentions: **{nli.get('neutral', 0)}**"
        )
    else:
        st.write("No NLI reasoning available.")

    # 5️⃣ Red flags
    if flags:
        st.subheader("⚠️ Red Flags")
        for f in flags:
            st.write(f"- {f}")

    # 6️⃣ Evidence
    st.subheader("📰 Evidence")

    if not evidence:
        st.info("📭 No verified evidence found from trusted news sources.")
        # st.caption(
        #     "ℹ️ This does **not** mean the claim is false — it means no trusted outlet confirms it yet."
        # )
    else:
        for e in evidence:
            st.write(f"- {e.get('title', 'Unknown source')}")

