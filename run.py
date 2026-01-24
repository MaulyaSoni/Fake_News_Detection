#!/usr/bin/env python3
"""
Fake News Detection System - Main Entry Point
===============================================

This script provides a convenient way to run the fake news detection system
with proper environment setup and error handling.

Usage:
    python run.py                    # Run Streamlit app
    python run.py --check            # Check system health
    python run.py --setup           # Setup environment
    python run.py --test            # Run basic tests
"""

import sys
import os
import argparse
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.helpers import setup_environment, get_system_info, system_checker

def main():
    parser = argparse.ArgumentParser(description="Fake News Detection System")
    parser.add_argument('--check', action='store_true', help='Check system health')
    parser.add_argument('--setup', action='store_true', help='Setup environment')
    parser.add_argument('--test', action='store_true', help='Run basic tests')
    parser.add_argument('--info', action='store_true', help='Show system information')
    
    args = parser.parse_args()
    
    if args.setup:
        print("Setting up environment...")
        if setup_environment():
            print("Environment setup completed successfully!")
        else:
            print("Environment setup failed!")
        sys.exit(1)
        return
    
    if args.check:
        print("Checking system health...")
        health = system_checker.check_system_health()
        
        print(f"\nOverall Status: {health['overall_status'].upper()}")
        print("\nSystem Checks:")
        
        for check_name, check_data in health['checks'].items():
            status = check_data['status'].upper()
            print(f"  • {check_name}: {status}")
            
            if check_name == 'models' and 'details' in check_data:
                for model, exists in check_data['details'].items():
                    status_icon = "[OK]" if exists else "[MISSING]"
                    print(f"    - {model}: {status_icon}")
        
        if health['recommendations']:
            print("\nRecommendations:")
            for rec in health['recommendations']:
                print(f"  • {rec}")
        
        return
    
    if args.info:
        print("System Information:")
        info = get_system_info()
        
        print(f"\nPython Version: {info['python_version']}")
        print(f"Platform: {info['platform']}")
        
        print(f"\nConfiguration:")
        for key, value in info['config'].items():
            print(f"  • {key}: {value}")
        
        print(f"\nStatistics:")
        stats = info['statistics']
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  • {key}: {value:.2f}")
            else:
                print(f"  • {key}: {value}")
        
        return
    
    if args.test:
        print("Running basic tests...")
        try:
            # Test imports
            from core.predictor import predict_news
            from core.news_reasoner import logical_analysis
            from llm.chat_model import is_llm_available
            
            print("All imports successful")
            
            # Test basic functionality
            test_text = "This is a test news article for basic functionality testing."
            
            # Test logical analysis
            flags = logical_analysis(test_text)
            print(f"Logical analysis works - {len(flags)} flags detected")
            
            # Test LLM availability
            llm_available = is_llm_available()
            print(f"LLM status: {'Available' if llm_available else 'Unavailable (fallback mode)'}")
            
            # Test ML prediction (might fail if models not loaded)
            try:
                result = predict_news(test_text)
                print(f"ML prediction works - {result.get('label', 'Unknown')}")
            except Exception as e:
                print(f"ML prediction test failed: {str(e)}")
            
            print("\nBasic tests completed!")
            
        except ImportError as e:
            print(f"Import error: {str(e)}")
            print("Please run 'pip install -r requirements.txt' first")
            sys.exit(1)
        except Exception as e:
            print(f"Test error: {str(e)}")
            sys.exit(1)
        
        return
    
    # Default: Run Streamlit app
    print("Starting Fake News Detection System...")
    print("Opening web interface at http://localhost:8501")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        import subprocess
        import streamlit.web.cli as stcli
        
        # Run streamlit app
        sys.argv = ["streamlit", "run", "app/streamlit_app.py"]
        sys.exit(stcli.main())
        
    except KeyboardInterrupt:
        print("\nShutting down... Goodbye!")
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        print("\nTroubleshooting:")
        print("  • Make sure all dependencies are installed: pip install -r requirements.txt")
        print("  • Check system health: python run.py --check")
        print("  • Setup environment: python run.py --setup")
        sys.exit(1)

if __name__ == "__main__":
    main()
