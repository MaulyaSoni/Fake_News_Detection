from typing import Dict, Any, List

class PromptTemplates:
    """Professional prompt templates for LLM reasoning"""
    
    @staticmethod
    def get_analysis_prompt(news_text: str, prediction: str, confidence: float, 
                          flags: List[str], credibility_score: Dict[str, Any]) -> str:
        """
        Generate comprehensive analysis prompt for the LLM
        
        Args:
            news_text: The news article text
            prediction: ML model prediction (FAKE/REAL)
            confidence: Confidence score from ML model
            flags: List of logical red flags
            credibility_score: Credibility analysis results
            
        Returns:
            Formatted prompt string
        """
        flags_text = '\n'.join([f"- {flag}" for flag in flags]) if flags else "None detected"
        
        prompt = f"""You are an expert AI system specializing in misinformation detection and media literacy analysis. Your task is to provide a comprehensive, balanced, and evidence-based analysis of the following news article.

## NEWS ARTICLE TO ANALYZE:
{news_text}

## MACHINE LEARNING ANALYSIS:
- **Prediction**: {prediction}
- **Confidence**: {confidence}%
- **Credibility Score**: {credibility_score['credibility_score']}/100
- **Risk Level**: {credibility_score['risk_level']}

## LOGICAL RED FLAGS DETECTED:
{flags_text}

## ANALYSIS REQUIREMENTS:
Please provide a detailed analysis covering:

1. **Content Assessment**: Evaluate the factual claims, sources, and evidence presented
2. **Language Analysis**: Examine tone, emotional appeals, and rhetorical devices
3. **Source Credibility**: Assess the reliability of mentioned sources and authorities
4. **Contextual Analysis**: Consider the broader context and plausibility
5. **Manipulation Tactics**: Identify any propaganda or persuasion techniques
6. **Final Recommendation**: Clear verdict with reasoning

## OUTPUT FORMAT:
Provide your analysis in a structured, professional manner with clear headings. Be objective and evidence-based. If the article appears to be fake news, explain the specific indicators. If it appears legitimate, explain why it passes credibility checks.

## IMPORTANT GUIDELINES:
- Be thorough but concise
- Focus on verifiable facts and logical reasoning
- Avoid speculation without evidence
- Consider multiple perspectives
- Provide actionable insights for media literacy

Begin your analysis now:"""
        
        return prompt
    
    @staticmethod
    def get_explanation_prompt(news_text: str, prediction: str, confidence: float) -> str:
        """
        Generate simplified explanation prompt
        
        Args:
            news_text: The news article text
            prediction: ML model prediction (FAKE/REAL)
            confidence: Confidence score from ML model
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an AI expert in misinformation detection.

News Article:
{news_text}

ML Prediction:
Label: {prediction}
Confidence: {confidence}%

Explain clearly why this news is likely REAL or FAKE. Focus on the key indicators and provide a concise, easy-to-understand explanation."""
        
        return prompt
    
    @staticmethod
    def get_media_literacy_prompt(flags: List[str]) -> str:
        """
        Generate media literacy education prompt
        
        Args:
            flags: List of detected red flags
            
        Returns:
            Formatted prompt string
        """
        flags_text = '\n'.join([f"- {flag}" for flag in flags]) if flags else "None detected"
        
        prompt = f"""You are a media literacy educator. Based on the following red flags detected in a news article, provide educational guidance for readers to improve their critical thinking skills.

DETECTED RED FLAGS:
{flags_text}

Please provide:
1. Explanation of why these tactics are concerning
2. How readers can spot similar patterns in the future
3. Tips for verifying information independently
4. General media literacy best practices

Make your response educational and empowering, not just critical."""
        
        return prompt
    
    @staticmethod
    def get_fact_checking_prompt(news_text: str) -> str:
        """
        Generate fact-checking guidance prompt
        
        Args:
            news_text: The news article text
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a professional fact-checker. For the following news article, provide guidance on how to verify its claims.

News Article:
{news_text}

Please outline:
1. Key claims that should be fact-checked
2. Reliable sources for verification
3. Search strategies for independent verification
4. Red flags that suggest caution
5. Steps readers can take to confirm the information

Focus on teaching the verification process rather than making definitive claims about truthfulness."""
        
        return prompt
