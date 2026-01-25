# # # import sys
# # # import os
# # # import streamlit as st

# # # # --------------------------------------------------
# # # # Path setup
# # # # --------------------------------------------------
# # # PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # if PROJECT_ROOT not in sys.path:
# # #     sys.path.insert(0, PROJECT_ROOT)

# # # # --------------------------------------------------
# # # # Imports (UPDATED)
# # # # --------------------------------------------------
# # # from core.predictor import predict_news
# # # from core.evaluator import evaluate_news

# # # # --------------------------------------------------
# # # # Page Config
# # # # --------------------------------------------------
# # # st.set_page_config(
# # #     page_title="Fake News Detector",
# # #     page_icon="📰",
# # #     layout="centered"
# # # )

# # # # --------------------------------------------------
# # # # Styling
# # # # --------------------------------------------------
# # # st.markdown("""
# # # <style>
# # #     body { background-color: #020617; }
# # #     .result-box {
# # #         background-color: #020617;
# # #         padding: 20px;
# # #         border-radius: 10px;
# # #         border-left: 5px solid #FFD700;
# # #         margin: 12px 0;
# # #     }
# # #     .main-title {
# # #         text-align: center;
# # #         color: #FFD700;
# # #         font-size: 2.4rem;
# # #         font-weight: bold;
# # #     }
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # --------------------------------------------------
# # # # Header
# # # # --------------------------------------------------
# # # st.markdown('<div class="main-title">📰 FAKE NEWS DETECTOR</div>', unsafe_allow_html=True)
# # # st.markdown(
# # #     '<p style="text-align:center;color:#E5E7EB;">ML + Logical Reasoning + Real-Time Verification</p>',
# # #     unsafe_allow_html=True
# # # )

# # # # --------------------------------------------------
# # # # Tabs
# # # # --------------------------------------------------
# # # tabs = st.tabs(["Analyze News", "Evaluation"])

# # # # ==================================================
# # # # TAB 1 — ANALYZE NEWS
# # # # ==================================================
# # # with tabs[0]:

# # #     news = st.text_area(
# # #         "Enter news article or claim",
# # #         height=260,
# # #         placeholder="Paste the news article or claim you want to analyze..."
# # #     )

# # #     col1, col2, col3 = st.columns([1, 2, 1])
# # #     with col2:
# # #         analyze_clicked = st.button("🔍 Analyze", use_container_width=True)

# # #     if analyze_clicked:
# # #         if not news.strip():
# # #             st.warning("Please enter some news text.")
# # #         else:
# # #             with st.spinner("Analyzing with ML + real-world verification..."):
# # #                 ml_result = predict_news(news)
# # #                 final_result = evaluate_news(news, ml_result)

# # #             # ------------------------------
# # #             # Prediction
# # #             # ------------------------------
# # #             st.markdown(f"""
# # #             <div class="result-box">
# # #                 <h3 style="color:#FFD700;">🎯 Final Verdict</h3>
# # #                 <p><strong>Classification:</strong> {final_result['final_verdict']}</p>
# # #                 <p><strong>Truth Score:</strong> {final_result['truth_score']}%</p>
# # #             </div>
# # #             """, unsafe_allow_html=True)

# # #             # ------------------------------
# # #             # Flags
# # #             # ------------------------------
# # #             if final_result["flags"]:
# # #                 st.markdown(f"""
# # #                 <div class="result-box">
# # #                     <h3 style="color:#EF4444;">⚠️ Detected Red Flags</h3>
# # #                     <ul>
# # #                         {''.join(f"<li>{f}</li>" for f in final_result["flags"])}
# # #                     </ul>
# # #                 </div>
# # #                 """, unsafe_allow_html=True)

# # #             # ------------------------------
# # #             # Real-time Evidence
# # #             # ------------------------------
# # #             if final_result["realtime_articles"]:
# # #                 st.markdown(f"""
# # #                 <div class="result-box">
# # #                     <h3 style="color:#3B82F6;">📰 Real-Time Evidence</h3>
# # #                     <ul>
# # #                         {''.join(
# # #                             f"<li><strong>{a['title']}</strong> — {a['source']}</li>"
# # #                             for a in final_result["realtime_articles"][:5]
# # #                         )}
# # #                     </ul>
# # #                 </div>
# # #                 """, unsafe_allow_html=True)

# # #            # ------------------------------
# # #             # Reasoning Breakdown
# # #             # ------------------------------
# # #             reason = final_result.get("reason", {})

# # #             st.markdown(f"""
# # #             <div class="result-box">
# # #                 <h3 style="color:#8B5CF6;">🧠 Logical Reasoning</h3>
# # #                 <ul>
# # #                     <li>ML Confidence: {reason.get('ml', 0)}%</li>
# # #                     <li>Heuristic Risk Penalty: {reason.get('heuristics', 0)}%</li>
# # #                     <li>Evidence Support Bonus: {reason.get('evidence_support', 0)}%</li>
# # #                 </ul>
# # #             </div>
# # #             """, unsafe_allow_html=True)


# # # # ==================================================
# # # # TAB 2 — EVALUATION
# # # # ==================================================
# # # with tabs[1]:
# # #     st.markdown("""
# # #     <div class="result-box">
# # #         <h3 style="color:#FFD700;">📊 Model Evaluation</h3>
# # #         <ul>
# # #             <li>Accuracy / Precision / Recall</li>
# # #             <li>Confusion Matrix</li>
# # #             <li>Error Analysis</li>
# # #         </ul>
# # #     </div>
# # #     """, unsafe_allow_html=True)
# # import sys, os
# # import streamlit as st

# # PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # sys.path.insert(0, PROJECT_ROOT)

# # from core.predictor import predict_news
# # from core.evaluator import evaluate_news

# # st.set_page_config(page_title="Fake News Detector", layout="centered")

# # st.title("📰 Fake News Detection System")
# # st.caption("ML-based misinformation analysis with logical reasoning")

# # news = st.text_area("Enter news text", height=260)

# # if st.button("Analyze"):
# #     if not news.strip():
# #         st.warning("Please enter text")
# #     else:
# #         ml_result = predict_news(news)
# #         final_result = evaluate_news(news, ml_result)

# #         st.subheader("🎯 Final Verdict")
# #         st.write("**Classification:**", final_result["final_verdict"])
# #         st.write("**Truth Score:**", final_result["truth_score"], "%")

# #         if final_result["flags"]:
# #             st.subheader("⚠️ Red Flags")
# #             for f in final_result["flags"]:
# #                 st.write("-", f)

# #         st.subheader("🧠 Reasoning")
# #         st.json(final_result["reason"])
# import joblib

# model = joblib.load(r"D:\Fake_news_Detection\models\final_fake_news_model.pkl")
# print(type(model))
# embedder = joblib.load(r"D:\Fake_news_Detection\models\final_sentence_embedder.pkl")
# print(type(embedder))
import sys
import os
import streamlit as st

# --------------------------------------------------
# Fix Python path so Streamlit can find /core
# --------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.predictor import predict_news

# st.write("PYTHON PATH:", sys.path)

st.set_page_config(
    page_title="Fake News Detection System",
    layout="centered"
)

st.title("📰 Fake News Detection (AI-Powered)")
st.write("Semantic + Calibrated ML model")

news_text = st.text_area(
    "Paste News Article / Headline",
    height=220,
    placeholder="Enter news text here..."
)

if st.button("Analyze"):
    if not news_text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            result = predict_news(news_text)

        st.subheader("🎯 Final Verdict")
        st.write(f"**Classification:** {result['verdict']}")
        st.write(f"**Confidence:** {result['confidence']}%")

        st.subheader("📊 Probability Breakdown")
        st.write(f"Fake: {result['fake_prob']}%")
        st.write(f"Real: {result['real_prob']}%")

        if result:
            st.success("Prediction Complete")

            st.write(f"**Classification:** {result['verdict']}")
            st.write(f"🟥 Fake Probability: {result['fake_prob']}%")
            st.write(f"🟩 Real Probability: {result['real_prob']}%")
            st.write(f"🔥 Confidence: {result['confidence']}%")

