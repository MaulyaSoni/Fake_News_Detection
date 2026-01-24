import os
import sys
import pickle
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Config:
    """Configuration management for the application"""
    
    # Model paths
    MODELS_DIR = "models"
    EMBEDDER_MODEL_PATH = os.path.join(MODELS_DIR, "sentence_embedder.pkl")
    CLASSIFIER_MODEL_PATH = os.path.join(MODELS_DIR, "newmodel.pkl")
    
    # LLM Configuration
    DEFAULT_LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
    BACKUP_LLM_MODEL = "HuggingFaceH4/zephyr-7b-beta"
    
    # Analysis thresholds
    HIGH_CONFIDENCE_THRESHOLD = 80.0
    MEDIUM_CONFIDENCE_THRESHOLD = 60.0
    HIGH_RISK_THRESHOLD = 40
    MEDIUM_RISK_THRESHOLD = 70
    
    # Text processing
    MAX_TEXT_LENGTH = 10000  # Maximum characters for analysis
    MIN_TEXT_LENGTH = 50     # Minimum characters for analysis
    
    @classmethod
    def validate_paths(cls) -> Dict[str, bool]:
        """Validate that all required model paths exist"""
        paths = {
            'embedder': os.path.exists(cls.EMBEDDER_MODEL_PATH),
            'classifier': os.path.exists(cls.CLASSIFIER_MODEL_PATH),
            'models_dir': os.path.exists(cls.MODELS_DIR)
        }
        return paths
    
    @classmethod
    def get_env_var(cls, var_name: str, default: Any = None) -> Any:
        """Get environment variable with fallback"""
        return os.getenv(var_name, default)

class TextProcessor:
    """Utility class for text processing and validation"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text for analysis"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove non-printable characters except common punctuation
        import re
        text = re.sub(r'[^\x20-\x7E\n\t]', '', text)
        
        return text.strip()
    
    @staticmethod
    def validate_text(text: str) -> Dict[str, Any]:
        """Validate text for analysis"""
        if not text or not text.strip():
            return {
                'valid': False,
                'error': 'Text is empty',
                'length': 0
            }
        
        cleaned_text = TextProcessor.clean_text(text)
        length = len(cleaned_text)
        
        if length < Config.MIN_TEXT_LENGTH:
            return {
                'valid': False,
                'error': f'Text is too short (minimum {Config.MIN_TEXT_LENGTH} characters)',
                'length': length
            }
        
        if length > Config.MAX_TEXT_LENGTH:
            return {
                'valid': False,
                'error': f'Text is too long (maximum {Config.MAX_TEXT_LENGTH} characters)',
                'length': length
            }
        
        return {
            'valid': True,
            'error': None,
            'length': length,
            'cleaned_text': cleaned_text
        }
    
    @staticmethod
    def truncate_text(text: str, max_length: int = Config.MAX_TEXT_LENGTH) -> str:
        """Truncate text to maximum length"""
        if len(text) <= max_length:
            return text
        
        return text[:max_length-3] + "..."

class ModelManager:
    """Utility class for managing ML models"""
    
    @staticmethod
    def load_model(model_path: str, model_type: str = "unknown") -> Any:
        """Load a pickle model with error handling"""
        try:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            logger.info(f"Successfully loaded {model_type} model from {model_path}")
            return model
            
        except Exception as e:
            logger.error(f"Error loading {model_type} model: {str(e)}")
            raise
    
    @staticmethod
    def save_model(model: Any, model_path: str, model_type: str = "unknown") -> bool:
        """Save a model to disk"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            
            logger.info(f"Successfully saved {model_type} model to {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving {model_type} model: {str(e)}")
            return False

class AnalysisLogger:
    """Utility class for logging analysis results"""
    
    def __init__(self, log_file: str = "analysis_log.json"):
        self.log_file = log_file
        self.logs = []
        self._load_logs()
    
    def _load_logs(self):
        """Load existing logs from file"""
        try:
            if os.path.exists(self.log_file):
                import json
                with open(self.log_file, 'r') as f:
                    self.logs = json.load(f)
        except Exception as e:
            logger.warning(f"Could not load analysis logs: {str(e)}")
            self.logs = []
    
    def log_analysis(self, news_text: str, ml_result: Dict[str, Any], 
                    flags: List[str], credibility_score: Dict[str, Any]):
        """Log an analysis result"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'text_length': len(news_text),
            'prediction': ml_result.get('label'),
            'confidence': ml_result.get('confidence'),
            'credibility_score': credibility_score.get('credibility_score'),
            'risk_level': credibility_score.get('risk_level'),
            'flag_count': len(flags),
            'flags': flags[:5]  # Store first 5 flags to save space
        }
        
        self.logs.append(log_entry)
        self._save_logs()
    
    def _save_logs(self):
        """Save logs to file"""
        try:
            import json
            with open(self.log_file, 'w') as f:
                json.dump(self.logs[-1000:], f)  # Keep last 1000 entries
        except Exception as e:
            logger.warning(f"Could not save analysis logs: {str(e)}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get analysis statistics"""
        if not self.logs:
            return {
                'total_analyses': 0,
                'avg_confidence': 0,
                'fake_count': 0,
                'real_count': 0,
                'high_risk_count': 0
            }
        
        total = len(self.logs)
        confidences = [log['confidence'] for log in self.logs if log['confidence']]
        fake_count = sum(1 for log in self.logs if log['prediction'] == 'FAKE')
        real_count = sum(1 for log in self.logs if log['prediction'] == 'REAL')
        high_risk_count = sum(1 for log in self.logs if log['risk_level'] == 'HIGH')
        
        return {
            'total_analyses': total,
            'avg_confidence': sum(confidences) / len(confidences) if confidences else 0,
            'fake_count': fake_count,
            'real_count': real_count,
            'high_risk_count': high_risk_count,
            'fake_percentage': (fake_count / total) * 100 if total > 0 else 0
        }

class SystemChecker:
    """Utility class for system health checks"""
    
    @staticmethod
    def check_system_health() -> Dict[str, Any]:
        """Perform comprehensive system health check"""
        health_status = {
            'overall_status': 'healthy',
            'checks': {},
            'recommendations': []
        }
        
        # Check model files
        model_paths = Config.validate_paths()
        health_status['checks']['models'] = {
            'status': 'healthy' if all(model_paths.values()) else 'warning',
            'details': model_paths
        }
        
        if not all(model_paths.values()):
            health_status['recommendations'].append("Missing model files. Check models directory.")
            health_status['overall_status'] = 'warning'
        
        # Check environment variables
        hf_token = Config.get_env_var('HUGGINGFACEHUB_API_TOKEN')
        health_status['checks']['llm_api'] = {
            'status': 'healthy' if hf_token else 'warning',
            'has_token': bool(hf_token)
        }
        
        if not hf_token:
            health_status['recommendations'].append("Set HUGGINGFACEHUB_API_TOKEN for LLM features.")
            health_status['overall_status'] = 'warning'
        
        # Check disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage(".")
            free_gb = free // (1024**3)
            
            health_status['checks']['disk_space'] = {
                'status': 'healthy' if free_gb > 1 else 'warning',
                'free_gb': free_gb
            }
            
            if free_gb < 1:
                health_status['recommendations'].append("Low disk space. Consider cleaning up.")
                health_status['overall_status'] = 'warning'
                
        except Exception as e:
            health_status['checks']['disk_space'] = {
                'status': 'error',
                'error': str(e)
            }
            health_status['overall_status'] = 'error'
        
        return health_status

# Global instances
analysis_logger = AnalysisLogger()
system_checker = SystemChecker()

# Convenience functions
def get_system_info() -> Dict[str, Any]:
    """Get comprehensive system information"""
    return {
        'python_version': sys.version,
        'platform': sys.platform,
        'config': {
            'models_dir': Config.MODELS_DIR,
            'llm_model': Config.DEFAULT_LLM_MODEL,
            'max_text_length': Config.MAX_TEXT_LENGTH
        },
        'health': system_checker.check_system_health(),
        'statistics': analysis_logger.get_statistics()
    }

def setup_environment():
    """Setup the application environment"""
    # Create necessary directories
    os.makedirs(Config.MODELS_DIR, exist_ok=True)
    
    # Check system health
    health = system_checker.check_system_health()
    
    if health['overall_status'] == 'error':
        logger.error("System health check failed")
        return False
    
    if health['overall_status'] == 'warning':
        logger.warning("System health check passed with warnings")
        for rec in health['recommendations']:
            logger.warning(f"Recommendation: {rec}")
    
    logger.info("Environment setup completed successfully")
    return True
