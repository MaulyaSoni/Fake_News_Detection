import streamlit as st
import sys
import os
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.predictor import predict_news
from core.news_reasoner import logical_analysis, get_credibility_score
from llm.chat_model import (
    explain_news, 
    get_simple_explanation, 
    get_media_literacy_guidance, 
    get_fact_checking_guidance,
    is_llm_available
)

# Configure Streamlit page
st.set_page_config(
    page_title="Fake News Detection System",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
def load_custom_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #666;
            text-align: center;
            margin-bottom: 2rem;
        }
        .prediction-real {
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            padding: 1rem;
            border-radius: 0.25rem;
        }
        .prediction-fake {
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 1rem;
            border-radius: 0.25rem;
        }
        .confidence-high {
            color: #28a745;
            font-weight: bold;
        }
        .confidence-medium {
            color: #ffc107;
            font-weight: bold;
        }
        .confidence-low {
            color: #dc3545;
            font-weight: bold;
        }
        .risk-low {
            background-color: #d4edda;
            color: #155724;
        }
        .risk-medium {
            background-color: #fff3cd;
            color: #856404;
        }
        .risk-high {
            background-color: #f8d7da;
            color: #721c24;
        }
        .metric-card {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 0.25rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_custom_css()
    
    # Header
    st.markdown('<div class="main-header">📰 Fake News Detection System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Advanced ML + LLM Analysis for Misinformation Detection</div>', unsafe_allow_html=True)
    
    # Sidebar with system info
    with st.sidebar:
        st.header("🔧 System Status")
        
        # Model status
        st.subheader("Model Status")
        st.success("✅ ML Models Loaded")
        
        llm_status = is_llm_available()
        if llm_status:
            st.success("✅ LLM Available")
        else:
            st.warning("⚠️ LLM Unavailable (Fallback Mode)")
        
        st.subheader("About")
        st.info("""
        This system combines:
        • Machine Learning Classification
        • Logical Pattern Analysis  
        • AI-Powered Explanations
        • Media Literacy Guidance
        """)
        
        st.subheader("Features")
        st.markdown("""
        - **Hybrid Analysis**: ML + LLM
        - **Explainable AI**: Detailed reasoning
        - **Risk Assessment**: Credibility scoring
        - **Educational**: Media literacy tips
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 News Analysis")
        
        # Text input area
        news_text = st.text_area(
            "Enter News Article:",
            height=200,
            placeholder="Paste the news article text here for analysis...",
            help="Enter the full text of the news article you want to analyze for authenticity."
        )
        
        # Analysis buttons
        button_col1, button_col2, button_col3 = st.columns(3)
        
        with button_col1:
            analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
        
        with button_col2:
            fact_check_button = st.button("🔎 Fact-Check Guide", use_container_width=True)
        
        with button_col3:
            literacy_button = st.button("📚 Media Literacy", use_container_width=True)
    
    with col2:
        st.header("📊 Quick Stats")
        
        # Placeholder for stats (will be updated after analysis)
        if 'last_analysis' in st.session_state:
            analysis = st.session_state.last_analysis
            st.metric("Articles Analyzed", st.session_state.get('articles_count', 0))
            st.metric("Avg. Confidence", f"{st.session_state.get('avg_confidence', 0):.1f}%")
            st.metric("Risk Level", analysis.get('credibility_score', {}).get('risk_level', 'N/A'))
        else:
            st.metric("Articles Analyzed", 0)
            st.metric("Avg. Confidence", "0%")
            st.metric("Risk Level", "N/A")
    
    # Handle analysis
    if analyze_button and news_text.strip():
        with st.spinner("🔄 Analyzing news article..."):
            try:
                # Perform ML prediction
                ml_result = predict_news(news_text)
                
                # Perform logical analysis
                flags = logical_analysis(news_text)
                credibility_score = get_credibility_score(flags)
                
                # Generate LLM explanation
                if is_llm_available():
                    explanation = explain_news(
                        news_text, 
                        ml_result['label'], 
                        ml_result['confidence'], 
                        flags, 
                        credibility_score
                    )
                else:
                    explanation = get_simple_explanation(
                        news_text, 
                        ml_result['label'], 
                        ml_result['confidence']
                    )
                
                # Store results in session state
                st.session_state.last_analysis = {
                    'ml_result': ml_result,
                    'flags': flags,
                    'credibility_score': credibility_score,
                    'explanation': explanation
                }
                
                # Update statistics
                if 'articles_count' not in st.session_state:
                    st.session_state.articles_count = 0
                    st.session_state.total_confidence = 0
                
                st.session_state.articles_count += 1
                st.session_state.total_confidence += ml_result['confidence']
                st.session_state.avg_confidence = st.session_state.total_confidence / st.session_state.articles_count
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                return
    
    # Display results
    if 'last_analysis' in st.session_state:
        analysis = st.session_state.last_analysis
        display_results(analysis)
    
    # Handle fact-checking guide
    if fact_check_button and news_text.strip():
        with st.spinner("🔄 Generating fact-checking guide..."):
            try:
                guidance = get_fact_checking_guidance(news_text)
                st.subheader("🔎 Fact-Checking Guidance")
                st.info(guidance)
            except Exception as e:
                st.error(f"❌ Error generating guidance: {str(e)}")
    
    # Handle media literacy guide
    if literacy_button:
        with st.spinner("🔄 Generating media literacy guide..."):
            try:
                flags = logical_analysis(news_text) if news_text.strip() else []
                guidance = get_media_literacy_guidance(flags)
                st.subheader("📚 Media Literacy Guidance")
                st.info(guidance)
            except Exception as e:
                st.error(f"❌ Error generating guidance: {str(e)}")

def display_results(analysis: Dict[str, Any]):
    """Display analysis results in a professional format"""
    
    ml_result = analysis['ml_result']
    flags = analysis['flags']
    credibility_score = analysis['credibility_score']
    explanation = analysis['explanation']
    
    # Results container
    st.header("📋 Analysis Results")
    
    # Prediction section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        prediction_class = "prediction-real" if ml_result['label'] == "REAL" else "prediction-fake"
        st.markdown(f'<div class="{prediction_class}"><h3>Prediction: {ml_result["label"]}</h3></div>', unsafe_allow_html=True)
    
    with col2:
        confidence_class = get_confidence_class(ml_result['confidence'])
        st.markdown(f'<p class="{confidence_class}">Confidence: {ml_result["confidence"]}%</p>', unsafe_allow_html=True)
    
    with col3:
        risk_class = f"risk-{credibility_score['risk_level'].lower()}"
        st.markdown(f'<p class="{risk_class}">Risk Level: {credibility_score["risk_level"]}</p>', unsafe_allow_html=True)
    
    # Detailed metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Credibility Metrics")
        st.metric("Credibility Score", f"{credibility_score['credibility_score']}/100")
        st.metric("Red Flags Detected", credibility_score['flag_count'])
        st.metric("High Risk Flags", credibility_score['high_risk_flags'])
        st.metric("Medium Risk Flags", credibility_score['medium_risk_flags'])
    
    with col2:
        st.subheader("🚨 Logical Red Flags")
        if flags:
            for i, flag in enumerate(flags, 1):
                st.warning(f"{i}. {flag}")
        else:
            st.success("✅ No major red flags detected")
    
    # AI Explanation
    st.subheader("🤖 AI Explanation")
    with st.expander("View Detailed Analysis", expanded=True):
        st.markdown(explanation)
    
    # Action buttons
    st.subheader("🎯 Next Steps")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Copy Report", use_container_width=True):
            report_text = generate_report(analysis)
            st.code(report_text, language=None)
    
    with col2:
        if st.button("🔄 New Analysis", use_container_width=True):
            del st.session_state.last_analysis
            st.rerun()
    
    with col3:
        if st.button("📧 Share Results", use_container_width=True):
            st.info("Share functionality coming soon!")

def get_confidence_class(confidence: float) -> str:
    """Get CSS class for confidence level"""
    if confidence >= 80:
        return "confidence-high"
    elif confidence >= 60:
        return "confidence-medium"
    else:
        return "confidence-low"

def generate_report(analysis: Dict[str, Any]) -> str:
    """Generate a text report of the analysis"""
    ml_result = analysis['ml_result']
    flags = analysis['flags']
    credibility_score = analysis['credibility_score']
    
    report = f"""
FAKE NEWS DETECTION REPORT
=========================

PREDICTION: {ml_result['label']}
Confidence: {ml_result['confidence']}%
Risk Level: {credibility_score['risk_level']}
Credibility Score: {credibility_score['credibility_score']}/100

RED FLAGS DETECTED ({len(flags)}):
"""
    
    for i, flag in enumerate(flags, 1):
        report += f"{i}. {flag}\n"
    
    report += f"\nFLAG BREAKDOWN:
- High Risk: {credibility_score['high_risk_flags']}
- Medium Risk: {credibility_score['medium_risk_flags']}
- Low Risk: {credibility_score['low_risk_flags']}

RECOMMENDATION: {'Proceed with caution' if ml_result['label'] == 'FAKE' else 'Appears legitimate, but verify independently'}
"""
    
    return report

if __name__ == "__main__":
    main()
