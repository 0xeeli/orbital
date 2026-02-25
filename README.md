# 🪐 Orbital CLI

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🚀 **Orbital: Your AI co-pilot in the terminal.** Powered by Google's Gemini, this Python CLI tool brings real-time Markdown streaming, persistent chat history, and coding assistance right to your Linux Debian workflow. Say goodbye to browser tabs and hello to terminal productivity! 🐧✨

## ✨ Features
* **Real-time Streaming:** Watch the AI type out responses with full Markdown formatting and syntax highlighting.
* **Persistent Memory:** Orbital remembers your context between sessions (saved locally in `~/.orbital/history.json`).
* **File Ingestion:** Read and analyze local files directly from the chat prompt.
* **Debian Native:** Built to run smoothly on Linux using Python 3.

## ⚙️ Installation

1. Clone the repository:
```bash
git clone git@github.com:0xeeli/orbital.git
cd orbital
```

2. Install the package locally:
```bash
pip3 install -e .
```

3. Configure your API Key:
Create a `.env` file in the root directory and add your Gemini API key:
```text
GEMINI_API_KEY=your_api_key_here
```

## 🚀 Usage

Just type the command from anywhere in your terminal:

```bash
orbital
```

### Commands inside the chat:
* `quit`, `exit`, `q` : Close the session.
* `/clear` : Wipe the AI's memory and start a fresh context.
* `/read <file_path>` : Load a local file into Orbital's memory for analysis (e.g., `/read cli/main.py`).

---
*Built with [Typer](https://typer.tiangolo.com/), [Rich](https://rich.readthedocs.io/), and [Google GenAI](https://ai.google.dev/).*
