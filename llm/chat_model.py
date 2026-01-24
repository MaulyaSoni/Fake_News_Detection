import os
from typing import Dict, Any, List, Optional
from langchain_huggingface import HuggingFaceEndpoint
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from .prompt_templates import PromptTemplates

class NewsChatModel:
    """LangChain integration for news analysis and explanation"""
    
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        """
        Initialize the chat model
        
        Args:
            model_name: HuggingFace model identifier
        """
        self.model_name = model_name
        self.llm = None
        self.templates = PromptTemplates()
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the HuggingFace model via LangChain"""
        try:
            # Check for HuggingFace API token
            api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
            if not api_token:
                print("Warning: HUGGINGFACEHUB_API_TOKEN not found in environment variables")
                print("Please set your HuggingFace API token to use the LLM features")
                return
            
            # Initialize the model
            self.llm = HuggingFaceEndpoint(
                repo_id=self.model_name,
                temperature=0.2,  # Lower temperature for more consistent responses
                max_new_tokens=512,  # Reasonable length for explanations
                top_p=0.9,
                repetition_penalty=1.1,
                huggingfacehub_api_token=api_token
            )
            
            print(f"Successfully initialized model: {self.model_name}")
            
        except Exception as e:
            print(f"Error initializing model: {e}")
            self.llm = None
    
    def is_available(self) -> bool:
        """Check if the model is available for use"""
        return self.llm is not None
    
    def explain_news(self, news_text: str, prediction: str, confidence: float, 
                    flags: List[str], credibility_score: Dict[str, Any]) -> str:
        """
        Generate comprehensive explanation using the LLM
        
        Args:
            news_text: The news article text
            prediction: ML model prediction (FAKE/REAL)
            confidence: Confidence score from ML model
            flags: List of logical red flags
            credibility_score: Credibility analysis results
            
        Returns:
            Generated explanation text
        """
        if not self.is_available():
            return self._fallback_explanation(prediction, confidence, flags)
        
        try:
            # Generate the prompt
            prompt = self.templates.get_analysis_prompt(
                news_text, prediction, confidence, flags, credibility_score
            )
            
            # Get response from LLM
            messages = [
                SystemMessage(content="You are an expert AI system specializing in misinformation detection and media literacy analysis."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm(messages)
            return response.content
            
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return self._fallback_explanation(prediction, confidence, flags)
    
    def get_simple_explanation(self, news_text: str, prediction: str, confidence: float) -> str:
        """
        Generate a simple explanation without detailed analysis
        
        Args:
            news_text: The news article text
            prediction: ML model prediction (FAKE/REAL)
            confidence: Confidence score from ML model
            
        Returns:
            Generated simple explanation
        """
        if not self.is_available():
            return self._fallback_explanation(prediction, confidence, [])
        
        try:
            prompt = self.templates.get_explanation_prompt(news_text, prediction, confidence)
            
            messages = [
                SystemMessage(content="You are an AI expert in misinformation detection."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm(messages)
            return response.content
            
        except Exception as e:
            print(f"Error generating simple explanation: {e}")
            return self._fallback_explanation(prediction, confidence, [])
    
    def get_media_literacy_guidance(self, flags: List[str]) -> str:
        """
        Generate media literacy educational content
        
        Args:
            flags: List of detected red flags
            
        Returns:
            Educational guidance text
        """
        if not self.is_available():
            return self._fallback_media_literacy(flags)
        
        try:
            prompt = self.templates.get_media_literacy_prompt(flags)
            
            messages = [
                SystemMessage(content="You are a media literacy educator."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm(messages)
            return response.content
            
        except Exception as e:
            print(f"Error generating media literacy guidance: {e}")
            return self._fallback_media_literacy(flags)
    
    def get_fact_checking_guidance(self, news_text: str) -> str:
        """
        Generate fact-checking guidance
        
        Args:
            news_text: The news article text
            
        Returns:
            Fact-checking guidance text
        """
        if not self.is_available():
            return self._fallback_fact_checking()
        
        try:
            prompt = self.templates.get_fact_checking_prompt(news_text)
            
            messages = [
                SystemMessage(content="You are a professional fact-checker."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm(messages)
            return response.content
            
        except Exception as e:
            print(f"Error generating fact-checking guidance: {e}")
            return self._fallback_fact_checking()
    
    def _fallback_explanation(self, prediction: str, confidence: float, flags: List[str]) -> str:
        """Fallback explanation when LLM is not available"""
        explanation = f"Based on the analysis, this news article is classified as {prediction} with {confidence}% confidence.\n\n"
        
        if flags:
            explanation += "Key concerns identified:\n"
            for flag in flags:
                explanation += f"• {flag}\n"
        else:
            explanation += "No major red flags were detected in the analysis.\n"
        
        explanation += "\nNote: Detailed AI explanation is currently unavailable. Please verify information independently."
        
        return explanation
    
    def _fallback_media_literacy(self, flags: List[str]) -> str:
        """Fallback media literacy guidance"""
        guidance = "To improve your media literacy skills:\n\n"
        guidance += "1. Always check the source of information\n"
        guidance += "2. Look for evidence and supporting facts\n"
        guidance += "3. Be cautious of emotional language\n"
        guidance += "4. Verify claims with multiple reliable sources\n"
        guidance += "5. Consider the author's expertise and bias\n"
        
        if flags:
            guidance += "\nSpecific concerns to watch for:\n"
            for flag in flags:
                guidance += f"• {flag}\n"
        
        return guidance
    
    def _fallback_fact_checking(self) -> str:
        """Fallback fact-checking guidance"""
        return """To fact-check information effectively:

1. Identify the main claims in the article
2. Search for these claims on reliable fact-checking websites
3. Check original sources and primary documents
4. Look for expert opinions and scientific consensus
5. Be wary of anonymous sources or vague attributions
6. Consider the date and context of the information
7. Check if other reputable news outlets are reporting the same story

Recommended fact-checking resources:
- Snopes, PolitiFact, FactCheck.org
- Reuters Fact Check, Associated Press Fact Check
- Google Fact Check Explorer
- Official government and institutional websites"""

# Create global instance
chat_model = NewsChatModel()

# Convenience functions for direct import
def explain_news(news_text: str, prediction: str, confidence: float, 
                flags: List[str], credibility_score: Dict[str, Any]) -> str:
    """Convenience function for news explanation"""
    return chat_model.explain_news(news_text, prediction, confidence, flags, credibility_score)

def get_simple_explanation(news_text: str, prediction: str, confidence: float) -> str:
    """Convenience function for simple explanation"""
    return chat_model.get_simple_explanation(news_text, prediction, confidence)

def get_media_literacy_guidance(flags: List[str]) -> str:
    """Convenience function for media literacy guidance"""
    return chat_model.get_media_literacy_guidance(flags)

def get_fact_checking_guidance(news_text: str) -> str:
    """Convenience function for fact-checking guidance"""
    return chat_model.get_fact_checking_guidance(news_text)

def is_llm_available() -> bool:
    """Check if LLM is available"""
    return chat_model.is_available()
