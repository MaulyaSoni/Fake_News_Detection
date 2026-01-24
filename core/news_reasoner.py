import re
from typing import List, Dict, Any

class NewsReasoner:
    """Advanced logical analysis for fake news detection"""
    
    def __init__(self):
        # Define patterns for manipulation tactics
        self.urgency_patterns = [
            r'\bURGENT\b', r'\bBREAKING\b', r'\bIMMEDIATE\b', 
            r'\bALERT\b', r'\bCRITICAL\b', r'\bEMERGENCY\b'
        ]
        
        self.secrecy_patterns = [
            r'\bleaked\b', r'\bsecret\b', r'\bsilenced\b', 
            r'\bhidden\b', r'\bcovered up\b', r'\bclassified\b'
        ]
        
        self.exaggeration_patterns = [
            r'\d+%\s*(?:accurate|certain|guaranteed|proven)',
            r'\b100%\s*(?:true|accurate|proven|certain)',
            r'\bnever\s+before\b', r'\bunprecedented\b', r'\bmiracle\b'
        ]
        
        self.authority_patterns = [
            r'\bISRO\b', r'\bAadhaar\b', r'\bGovt\b', r'\bGovernment\b',
            r'\bNASA\b', r'\bWHO\b', r'\bUN\b', r'\bFBI\b', r'\bCIA\b'
        ]
        
        self.emotional_patterns = [
            r'\bshocking\b', r'\boutrageous\b', r'\bdisgusting\b',
            r'\bterrifying\b', r'\bheartbreaking\b', r'\bunbelievable\b'
        ]
        
        self.conspiracy_patterns = [
            r'\bthey\s+don\'t\s+want\s+you\s+to\s+know\b',
            r'\bthe\s+truth\s+is\s+being\s+hidden\b',
            r'\bmainstream\s+media\s+won\'t\s+report\b',
            r'\bwake\s+up\b', r'\bsheeple\b'
        ]
        
        self.source_credibility_patterns = [
            r'\bsources\s+say\b', r'\bexperts\s+claim\b', r'\bstudies\s+show\b',
            r'\bresearch\s+proves\b', r'\bscientists\s+confirm\b'
        ]
    
    def logical_analysis(self, news_text: str) -> List[str]:
        """
        Perform logical analysis to detect manipulation patterns
        
        Args:
            news_text: The news article text to analyze
            
        Returns:
            List of detected red flags
        """
        flags = []
        text_lower = news_text.lower()
        text_upper = news_text.upper()
        
        # Check for urgency tactics
        if any(re.search(pattern, text_upper) for pattern in self.urgency_patterns):
            flags.append("Uses urgency language to provoke emotional reaction")
        
        # Check for secrecy claims
        if any(re.search(pattern, text_lower) for pattern in self.secrecy_patterns):
            flags.append("Claims secrecy or hidden information without verifiable sources")
        
        # Check for statistical exaggeration
        if any(re.search(pattern, text_lower) for pattern in self.exaggeration_patterns):
            flags.append("Uses exaggerated statistical claims or absolute certainty")
        
        # Check for authority name-dropping
        if any(re.search(pattern, news_text) for pattern in self.authority_patterns):
            flags.append("Mentions authoritative institutions to build false credibility")
        
        # Check for emotional manipulation
        if any(re.search(pattern, text_lower) for pattern in self.emotional_patterns):
            flags.append("Uses emotionally charged language to manipulate reader response")
        
        # Check for conspiracy language
        if any(re.search(pattern, text_lower) for pattern in self.conspiracy_patterns):
            flags.append("Uses conspiracy-style language suggesting hidden agendas")
        
        # Check for vague sourcing
        vague_sources = 0
        for pattern in self.source_credibility_patterns:
            matches = re.findall(pattern, text_lower)
            vague_sources += len(matches)
        
        if vague_sources >= 2:
            flags.append("Relies heavily on vague or unspecified sources")
        
        # Additional logical checks
        if len(news_text.split()) < 50:
            flags.append("Article is unusually short, lacking detailed context")
        
        # Check for excessive capitalization
        caps_ratio = sum(1 for c in news_text if c.isupper()) / len(news_text) if len(news_text) > 0 else 0
        if caps_ratio > 0.15:  # More than 15% capital letters
            flags.append("Excessive use of capitalization for emphasis")
        
        # Check for multiple exclamation marks
        if news_text.count('!!!') > 0 or news_text.count('!') > 3:
            flags.append("Excessive punctuation indicating emotional manipulation")
        
        return flags
    
    def get_credibility_score(self, flags: List[str]) -> Dict[str, Any]:
        """
        Calculate a credibility score based on detected flags
        
        Args:
            flags: List of detected red flags
            
        Returns:
            Dictionary with credibility metrics
        """
        # Weight different types of flags
        high_risk_flags = [
            "Uses urgency language to provoke emotional reaction",
            "Uses conspiracy-style language suggesting hidden agendas",
            "Uses exaggerated statistical claims or absolute certainty"
        ]
        
        medium_risk_flags = [
            "Claims secrecy or hidden information without verifiable sources",
            "Mentions authoritative institutions to build false credibility",
            "Uses emotionally charged language to manipulate reader response"
        ]
        
        low_risk_flags = [
            "Relies heavily on vague or unspecified sources",
            "Article is unusually short, lacking detailed context",
            "Excessive use of capitalization for emphasis",
            "Excessive punctuation indicating emotional manipulation"
        ]
        
        score = 100  # Start with perfect score
        risk_level = "LOW"
        
        for flag in flags:
            if flag in high_risk_flags:
                score -= 25
            elif flag in medium_risk_flags:
                score -= 15
            elif flag in low_risk_flags:
                score -= 10
        
        score = max(0, score)  # Don't go below 0
        
        if score >= 80:
            risk_level = "LOW"
        elif score >= 60:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
        
        return {
            "credibility_score": score,
            "risk_level": risk_level,
            "flag_count": len(flags),
            "high_risk_flags": len([f for f in flags if f in high_risk_flags]),
            "medium_risk_flags": len([f for f in flags if f in medium_risk_flags]),
            "low_risk_flags": len([f for f in flags if f in low_risk_flags])
        }

# Create global instance
reasoner = NewsReasoner()

def logical_analysis(news_text: str) -> List[str]:
    """Convenience function for logical analysis"""
    return reasoner.logical_analysis(news_text)

def get_credibility_score(flags: List[str]) -> Dict[str, Any]:
    """Convenience function for credibility scoring"""
    return reasoner.get_credibility_score(flags)
