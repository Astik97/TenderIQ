# TenderIQ - AI-Powered Tender Comparison & Analysis System

## Overview

TenderIQ is an intelligent tender comparison and analysis platform designed to automate the evaluation of tender documents.

The system allows users to upload multiple tender documents in PDF, DOCX, and TXT formats, extract textual information, compare documents, analyze similarities and differences, and generate AI-powered insights and recommendations.

---

## Features

### Authentication Module

* User Registration
* User Login
* User Logout
* Session Management

### Tender Management

* Upload Multiple Tender Documents
* Support for PDF, DOCX, and TXT Files
* Secure File Storage
* MySQL Database Integration

### Document Processing

* Text Extraction from PDF Documents
* Text Extraction from DOCX Documents
* Text Extraction from TXT Files
* Data Storage for Future Analysis

### Comparison Engine (In Progress)

* Tender Similarity Analysis
* Tender Ranking
* Tender Recommendation
* AI-Powered Comparison Reports

### Future Enhancements

* NLP-Based Clause Extraction
* LLM-Based Tender Analysis
* PDF Report Generation
* Docker Deployment
* AWS Deployment

---

## Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### Database

* MySQL

### AI & NLP

* Scikit-Learn
* Sentence Transformers (Planned)
* Lightweight LLMs (Planned)

### Deployment

* Docker (Planned)
* AWS (Planned)

---

## Project Structure

tender-iq/

├── app.py

├── backend/

│   ├── routes/

│   ├── services/

│   └── utils/

├── templates/

├── static/

├── uploads/

├── requirements.txt

└── README.md

---

## Installation

Clone the repository:

git clone https://github.com/Astik97/TenderIQ.git

Move into project folder:

cd TenderIQ

Create virtual environment:

python -m venv venv

Activate virtual environment:

Windows:
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run application:

python app.py

---

## Current Status

Phase 1 Completed

* Flask Setup
* MySQL Integration
* Authentication System
* Dashboard
* Multi-file Upload System

Phase 2 In Progress

* Text Extraction
* Tender Comparison Engine
* NLP Integration
* AI Analysis Module

---

## Author

Astik Mohapatra

Final Year Project | AI-Powered Tender Comparison & Analysis System
