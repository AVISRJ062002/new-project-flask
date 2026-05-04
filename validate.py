#!/usr/bin/env python3
"""
DevOps CI/CD Project Validator
Validates that all components are properly configured and ready for deployment
"""

import os
import sys
import subprocess
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(message):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"{message}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"{description}: {filepath} - NOT FOUND")
        return False

def check_file_content(filepath, content_check, description):
    """Check if file contains expected content"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if content_check in content:
                print_success(f"{description}")
                return True
            else:
                print_error(f"{description} - Content not found")
                return False
    except Exception as e:
        print_error(f"{description} - Error: {e}")
        return False

def check_command(command, description):
    """Check if a command is available"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, timeout=5)
        if result.returncode == 0:
            print_success(f"{description}")
            return True
        else:
            print_warning(f"{description} - Command failed")
            return False
    except Exception as e:
        print_error(f"{description} - {e}")
        return False

def main():
    print_header("🚀 DevOps CI/CD Project Validator")
    
    results = {
        'files': 0,
        'checks': 0,
        'passed': 0,
        'failed': 0
    }
    
    # Check project structure
    print_header("📁 Project Structure Validation")
    
    files_to_check = [
        ('app.py', 'Flask Application'),
        ('requirements.txt', 'Python Dependencies'),
        ('Dockerfile', 'Docker Configuration'),
        ('Jenkinsfile', 'Jenkins Pipeline'),
        ('templates/index.html', 'HTML Template'),
        ('static/style.css', 'CSS Styling'),
        ('docker-compose.yml', 'Docker Compose'),
        ('.dockerignore', 'Docker Ignore'),
        ('README.md', 'README Documentation'),
        ('SETUP_GUIDE.md', 'Setup Guide'),
    ]
    
    for filepath, description in files_to_check:
        if check_file_exists(filepath, description):
            results['passed'] += 1
        else:
            results['failed'] += 1
        results['checks'] += 1
    
    # Check file contents
    print_header("📋 File Content Validation")
    
    content_checks = [
        ('app.py', 'from flask import Flask', 'Flask import in app.py'),
        ('app.py', 'app.run(host="0.0.0.0", port=5000)', 'Port 5000 configuration'),
        ('requirements.txt', 'Flask==2.3.2', 'Flask version specified'),
        ('Dockerfile', 'FROM python:3.9', 'Python 3.9 base image'),
        ('Dockerfile', 'EXPOSE 5000', 'Port 5000 exposed'),
        ('Jenkinsfile', 'stage(\'Clone', 'Jenkins Clone stage'),
        ('Jenkinsfile', 'stage(\'Build', 'Jenkins Build stage'),
        ('templates/index.html', '<!DOCTYPE html>', 'HTML DOCTYPE'),
        ('static/style.css', 'background: linear-gradient', 'Gradient background CSS'),
        ('docker-compose.yml', 'services:', 'Docker Compose services'),
    ]
    
    for filepath, content, description in content_checks:
        if check_file_content(filepath, content, description):
            results['passed'] += 1
        else:
            results['failed'] += 1
        results['checks'] += 1
    
    # Check Python syntax
    print_header("🐍 Python Syntax Validation")
    
    try:
        with open('app.py', 'r') as f:
            code = f.read()
            compile(code, 'app.py', 'exec')
            print_success("Python syntax in app.py is valid")
            results['passed'] += 1
    except SyntaxError as e:
        print_error(f"Syntax error in app.py: {e}")
        results['failed'] += 1
    results['checks'] += 1
    
    # Check system commands
    print_header("💻 System Commands Availability")
    
    commands = [
        ('python --version', 'Python is installed'),
        ('pip --version', 'pip is installed'),
        ('docker --version', 'Docker is installed'),
        ('git --version', 'Git is installed'),
    ]
    
    for command, description in commands:
        if check_command(command, description):
            results['passed'] += 1
        else:
            results['failed'] += 1
        results['checks'] += 1
    
    # Python packages
    print_header("📦 Python Packages Validation")
    
    try:
        import flask
        print_success(f"Flask is installed (version {flask.__version__})")
        results['passed'] += 1
    except ImportError:
        print_warning("Flask is not installed - run: pip install -r requirements.txt")
        results['failed'] += 1
    results['checks'] += 1
    
    # Final report
    print_header("📊 Validation Summary")
    
    print(f"Total Checks: {results['checks']}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.END}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.END}")
    
    success_rate = (results['passed'] / results['checks'] * 100) if results['checks'] > 0 else 0
    print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    # Recommendations
    print_header("🚀 Next Steps")
    
    if results['failed'] == 0:
        print_success("All checks passed! Your project is ready for deployment.")
        print("\nRecommended commands:")
        print(f"{Colors.BLUE}1. Test locally: python app.py{Colors.END}")
        print(f"{Colors.BLUE}2. Build Docker: docker build -t cicd-app:latest .{Colors.END}")
        print(f"{Colors.BLUE}3. Run container: docker run -d --name cicd-app-container -p 5000:5000 cicd-app:latest{Colors.END}")
        print(f"{Colors.BLUE}4. Test endpoint: curl http://localhost:5000{Colors.END}")
        print(f"{Colors.BLUE}5. Push to Docker Hub: docker push YOUR_USERNAME/cicd-app:latest{Colors.END}")
    else:
        print_warning("Some checks failed. Please review the issues above.")
        print("\nTo fix common issues:")
        print(f"{Colors.YELLOW}• Install Flask: pip install -r requirements.txt{Colors.END}")
        print(f"{Colors.YELLOW}• Verify Docker: docker --version{Colors.END}")
        print(f"{Colors.YELLOW}• Check file permissions: ls -la app.py{Colors.END}")
    
    print("\n" + "="*60)
    
    return 0 if results['failed'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
