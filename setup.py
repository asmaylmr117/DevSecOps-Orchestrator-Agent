@"
from setuptools import setup, find_packages

setup(
    name="devsecops-orchestrator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langgraph",
        "langchain-anthropic",
        "fastapi",
        "uvicorn",
        "python-dotenv",
    ],
)
"@ | Out-File -FilePath "setup.py" -Encoding UTF8