# 🚀 TenderIQ - AI-Powered Tender Comparison & Analysis Platform

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?style=for-the-badge&logo=mysql)
![Status](https://img.shields.io/badge/Status-Active%20Development-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

---

# 📖 Overview

TenderIQ is an **AI-powered Tender Comparison & Analysis Platform** designed to automate the process of evaluating multiple tender documents
using Natural Language Processing (NLP) and semantic similarity techniques.

The system enables users to upload tender documents in **PDF, DOCX, and TXT** formats, automatically extracts and preprocesses document content, performs **transformer-based semantic clause comparison** using Sentence Transformers, identifies similarities and differences, assesses procurement risks, and generates structured comparison reports with executive summaries and actionable recommendations.

Built using **Python, Flask, MySQL, Sentence Transformers, Scikit-learn, and HTML, CSS, JS**, TenderIQ transforms a traditionally manual and time-consuming tender review process into an intelligent, efficient, and data-driven decision support system for procurement teams.

> **Project Status:** 🚧 Version 1.0

---

# ⭐ Key Highlights

- AI-assisted Tender Comparison
- Transformer-based Semantic Analysis
- Clause-Level Matching
- Procurement Risk Assessment
- Automated Executive Summary
- Rule-based Recommendation Engine
- Interactive Analytics Dashboard
- Secure Flask Backend
- MySQL Database Integration
- Professional Comparison Reports

# 🎯 Problem Statement

Organizations and procurement teams often receive multiple tender documents that contain hundreds of technical, commercial, and legal clauses.

Traditional tender evaluation is:

- Time-consuming and resource-intensive
- Prone to human errors and inconsistent decisions
- Difficult to scale for large or multiple documents
- Unable to understand semantic similarities between clauses

TenderIQ addresses these challenges by automating document comparison using NLP-powered semantic analysis, enabling faster, more accurate, and data-driven procurement decisions.

---

# ✨ Features

## 🔐 Core Features

- Secure User Authentication
- User Registration & Login
- Password Hashing using Bcrypt
- Session Management
- Multi-format Document Upload (PDF, DOCX, TXT)
- Automatic Document Storage
- Document Text Extraction
- Text Cleaning & Preprocessing

---

## 🤖 AI & NLP Engine

- Transformer-based Sentence Embeddings
- Semantic Clause Comparison
- Cosine Similarity Analysis
- Weighted Similarity Calculation
- Clause-Level Matching
- Confidence Score Generation
- Procurement Risk Assessment
- Automated Executive Summary
- Rule-based Recommendation Engine
- Procurement Insights Generation
- Interactive Analytics Dashboard

---

## 📊 Reporting

- Detailed Comparison Reports
- Clause-Level Analysis
- Similarity Statistics
- Procurement Risk Visualization
- Dashboard Analytics
- Printable Report Generation

---

# 📈 Project Statistics

| Statistic | Value |
|-----------|-------|
| Python Modules | 20+ |
| Database Tables | 3 |
| Supported File Formats | 3 |
| NLP Model | all-MiniLM-L6-v2 |
| Risk Levels | 5 |
| Dashboard Widgets | 4 |
| Comparison Type | Semantic Clause-Level |
| Authentication | Secure Session-Based |
| Report Generation | Automated |

# Screenshots

## Home Page

![Home](screenshots/home.png)

---

## Login Page

![Login](screenshots/login.png)

---

## Registration Page

![Register](screenshots/register.png)

---

## Dashboard

![Dashboard](screenshots/dashboard.png)

---

## Comparison Report

![Comparison Report](screenshots/comparison_report.png)

---

## View Tenders
![Tender Details](screenshots/view_tenders.png)

---

# 📊 Performance Metrics

| Metric | Value |
|---------|-------|
| Supported Document Formats | PDF, DOCX, TXT |
| NLP Model | Sentence Transformers (all-MiniLM-L6-v2) |
| Similarity Technique | Semantic Cosine Similarity |
| Comparison Level | Clause-Level |
| Risk Classification Levels | 5 |
| Dashboard Analytics | 4 Interactive Widgets |
| Authentication | Secure Session-based |
| Database | MySQL |
| Report Generation | Automated |

---

# ⚙ System Workflow

Authentication
      │
      ▼
Upload Tender Documents
      │
      ▼
Extract Text
      │
      ▼
Text Preprocessing
      │
      ▼
Clause Segmentation
      │
      ▼
Sentence Embedding Generation
      │
      ▼
Semantic Similarity Analysis
      │
      ▼
Clause-Level Matching
      │
      ▼
Weighted Similarity Calculation
      │
      ▼
Procurement Risk Assessment
      │
      ▼
Automated Executive Summary
      │
      ▼
Analytics Dashboard
      │
      ▼
Comparison Report

---

# 🏗 Project Architecture

Frontend (HTML • CSS • JavaScript)
                │
                ▼
Flask Routes
                │
                ▼
Business Services
                │
                ▼
Document Processing Engine
                │
                ▼
NLP Engine
                │
                ▼
Sentence Transformer
                │
                ▼
Semantic Comparison Engine
                │
                ▼
Risk Assessment Engine
                │
                ▼
Recommendation Engine
                │
                ▼
Report Generation Engine
                │
                ▼
MySQL Database

---

# 💻 Tech Stack

## Backend
- Python
- Flask

## Database
- MySQL
- PyMySQL

## AI / NLP
- Sentence Transformers
- all-MiniLM-L6-v2
- Transformers

## Machine Learning
- Scikit-learn
- Cosine Similarity
- NumPy
- PyTorch

## Document Processing
- pdfplumber
- docx2txt

## Frontend
- HTML5
- CSS3
- JavaScript

## Authentication
- Flask Sessions
- Bcrypt

## Developer Tools
- Git
- GitHub
- VS Code

---

# 📦 Requirements

```
Flask
python-dotenv
PyMySQL
bcrypt
pdfplumber
docx2txt
scikit-learn
sentence-transformers
transformers
torch
numpy
requests
```

Or install directly

```bash
pip install -r requirements.txt
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/Astik97/TenderIQ.git

cd TenderIQ
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create

```
.env
```

Example

```
MYSQL_HOST=localhost

MYSQL_USER=root

MYSQL_PASSWORD=your_password

MYSQL_DATABASE=tenderiq

SECRET_KEY=your_secret_key
```

---

## Import Database

Import

```
database/tender_system_db_comparison_reports.sql,
database/tender_system_db_tenders.sql,
database/tender_system_db_users.sql
```

into MySQL.

---

## Run Project

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

# ✅ Completed Features

- User Authentication & Authorization
- Secure Password Hashing
- Multi-format Document Upload
- PDF, DOCX & TXT Processing
- Automatic Text Extraction
- Text Cleaning & Preprocessing
- Clause Segmentation
- Transformer-based Sentence Embeddings
- Semantic Similarity Analysis
- Cosine Similarity Calculation
- Clause-Level Matching
- Weighted Similarity Scoring
- Procurement Risk Assessment
- Automated Executive Summary
- Rule-based Recommendation Engine
- Interactive Analytics Dashboard
- Comparison Report Generation
- MySQL Database Integration

## 🔮 Future Roadmap

- Docker Containerization
- AWS Cloud Deployment
- OCR Support for Scanned Documents
- Multi-language Tender Comparison
- Role-Based Access Control (RBAC)
- LLM-powered Clause Explanation
- Vendor Ranking System
- Contract Compliance Checking
- Email Notifications
- AI Procurement Chat Assistant

---

# 🔒 Security

TenderIQ follows secure backend development practices including:

- Password Hashing using Bcrypt
- Session-based Authentication
- Environment Variable Configuration
- Parameterized SQL Queries
- Secure MySQL Connectivity
- Protected User Sessions

---

# 🧪 Testing

The application has been manually tested for:

- User Authentication
- Session Management
- Document Upload
- PDF/DOCX/TXT Processing
- Semantic Similarity Validation
- Clause-Level Comparison
- Report Generation
- MySQL Database Operations

---

# 🤝 Contribution

Contributions, suggestions, and feedback are always welcome.

Feel free to fork the repository and submit a pull request.

---

# 👨‍💻 Author

**Astik Mohapatra**

🎓 B.Tech – Computer Science & Engineering

Government College of Engineering, Keonjhar

**Target Roles**

- Python Developer
- Flask Developer
- Backend Developer

📧 astikm7007@gmail.com

🔗 LinkedIn

https://linkedin.com/in/astik-mohapatra

🔗 GitHub

https://github.com/Astik97

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

Your support motivates future development of TenderIQ.

---