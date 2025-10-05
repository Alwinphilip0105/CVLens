# CVLens - AI-Powered Resume Analysis & Job Recommendations

<div align="center">

[![YouTube Video](https://img.youtube.com/vi/C9QOUXbKCKU/0.jpg)](https://youtu.be/C9QOUXbKCKU)

**🎥 [Watch Demo Video](https://youtu.be/C9QOUXbKCKU)**

</div>

## 🚀 About the Project

**CVLens** is an intelligent resume analysis platform that transforms your career journey with AI-powered insights. Our system combines advanced resume parsing, keyword extraction, and machine learning to provide personalized job recommendations and actionable resume improvement tips.

### ✨ Key Features

- **📄 Smart Resume Parser**: Automatically extracts personal details, skills, and experience from uploaded resumes
- **🎯 AI-Powered Job Recommendations**: Get personalized job matches with apply links and matching scores
- **💡 Resume Improvement Tips**: Receive detailed, actionable feedback to enhance your resume
- **🔍 Keyword Analysis**: Advanced keyword extraction and matching for better job targeting
- **📊 Real-time Analysis**: Instant processing with beautiful, interactive dashboards

### 🏗️ Architecture

Our system leverages a sophisticated n8n workflow pipeline that:

1. **Data Ingestion**: Receives user data and resume files from the frontend
2. **Resume Processing**: Parses and extracts key information using AI models
3. **Vector Embeddings**: Creates embeddings for both job data and user profiles using Pinecone
4. **Job Matching**: Uses similarity matching to find relevant job postings
5. **Response Generation**: Formats recommendations and resume tips for the user interface

### 🛠️ Technology Stack

- **Frontend**: Streamlit (Python)
- **Backend**: n8n Workflow Automation
- **Database**: Firebase Firestore
- **Vector Store**: Pinecone
- **AI/ML**: Google AI Models for embeddings and analysis
- **File Processing**: PyMuPDF for PDF parsing

### 📱 Dashboard Screenshots

#### Profile Analysis Page
- Upload and preview resume content
- Edit extracted personal details
- Configure job preferences and targets
- Set skills, locations, and job levels

#### Job Recommendations Page
- View AI-generated job matches
- See matching scores and apply links
- Expand job descriptions for detailed information
- Track application progress

#### Resume Tips Page
- Personalized improvement suggestions
- Detailed analysis of resume sections
- Actionable recommendations for enhancement
- Professional formatting guidance

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Poetry (for dependency management)
- Firebase project with Firestore enabled
- n8n instance for workflow automation

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd CVLens

# Install dependencies
poetry install
```

### Running the Application

```bash
# Start the Streamlit frontend
cd Frontend
streamlit run streamlit_app.py

# The application will be available at http://localhost:8501
```

## 🔧 Development

### Code Formatting

```bash
# Format all files
poetry run black .

# Format specific file
poetry run black filename.py

# Format notebook
poetry run black filename.ipynb
```

### Project Structure

```
CVLens/
├── Frontend/                 # Streamlit web application
│   ├── streamlit_app.py     # Main application file
│   └── utils/               # Utility modules
├── Resume_Parser/           # Resume processing logic
│   ├── resume_parser.py     # Core parsing functions
│   └── Test_Resumes/        # Sample resume files
├── pyproject.toml           # Poetry dependencies
└── README.md               # This file
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Workflow automation powered by [n8n](https://n8n.io/)
- Vector embeddings by [Pinecone](https://www.pinecone.io/)
- Resume parsing with [PyMuPDF](https://pymupdf.readthedocs.io/)

---

**Transform your career with AI-powered resume analysis and job recommendations! 🚀**
