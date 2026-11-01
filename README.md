AI Shopping Assistant

1. Clone Repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd agent

2. Create Virtual Environment

python3 -m venv .venv
source .venv/bin/activate

3. Install Requirements

pip install --upgrade pip
pip install -r requirements.txt

4. Configure Environment Variables

Create ".env" in the project root:

GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-3.8-flash

TAVILY_API_KEY=your_tavily_api_key

API keys:

- Google Gemini: https://aistudio.google.com/apikey
- Tavily: https://app.tavily.com/

5. Run Application

python -m app.main

requirements.txt
langchain
langchain-core
langchain-google-genai
langchain-tavily
langgraph
python-dotenv
pydantic

.gitignore

.venv/
_pycache_/
*.pyc
.env
.pytest_cache/
.vscode/
.idea/
