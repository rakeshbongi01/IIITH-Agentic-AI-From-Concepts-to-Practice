# **Tutorial 3: Models**

[Agentic AI Systems - From Concepts to Practice](https://dfl-apps.iiit.ac.in/learning/course/course-v1:IIITH_2026_06+AAI+2026_06/home)



> **Learning outcome:** By the end of this tutorial, you should be able to describe a neural network at a very basic level, explain the difference between model size and model location, run a Gemini chatbot from Python, run a local Ollama chatbot, and identify when cloud, local, or hybrid use is appropriate.

---
| Part | Topic | 
|---|---:|
| 0 | A very basic neural-network idea (MLP) | 
| 1 | Large vs small; cloud vs local | 
| 2 | Why teams use cloud models | 
| 3 | Build a Gemini chatbot in VS Code |
| 4 | What local models are | 
| 5 | Ollama, llama.cpp, LM Studio, and vLLM | 
| 6–7 | Run a local model and compare | 


## Ready-to-run files

The complete code is included beside this tutorial:

- [`gemini_chatbot.py`](gemini_chatbot.py) — multi-turn Gemini cloud chatbot
- [`ollama_chatbot.py`](ollama_chatbot.py) — multi-turn local Ollama chatbot
- [`requirements.txt`](requirements.txt) — Python packages used by both examples
- [`.env.example`](.env.example) — API-key variable name without a real secret
- [`README.md`](README.md) — short setup and run instructions

The code blocks below are teaching versions of these files. Use the complete files for the live demonstration.

---

# **Part 0: A very basic neural-network idea**

Over the last two tutorials, we learned Python basics and ML topics of linear regression and logistic regression.

Those models are useful, but they have limits: real-world problems—especially language, images, and complex decisions—contain patterns that are not always simple or straight-line relationships.  

Today, we will take the next step: neural networks. We will start with a very simple MLP, just to understand the core idea of many small pattern-finders working together.  

Then we will shift focus to language models. We will learn how to use one in a Python chatbot, and then compare it with a model running locally on our own machine.

## Start with one small decision-maker

Imagine deciding whether to carry an umbrella. You look at a few inputs:

- Is rain predicted?
- Is the sky dark?
- Will I be outside for a long time?

A small decision-maker looks at all those inputs, gives each one an amount of importance, and produces an answer such as **“take an umbrella”** or **“do not take one.”**

In a computer, those amounts of importance are internal numbers. During training, the computer sees many examples and gradually adjusts those numbers so that its answers improve.

> This tiny decision-maker is the basic building block we need for today. It is inspired by the idea of a neuron, but it is simply a small pattern-finder—not a brain.

## Put many decision-makers together

One decision-maker is limited. A **neural network** connects many small decision-makers so that one group can pass useful signals to the next group.

```text
Inputs                 Middle groups                     Answer
rain, sky, time  ──>  small pattern-finders  ──>  take umbrella?
```

An **MLP** is a simple kind of neural network where information moves forward through a stack of groups:

```text
Input group  →  middle group  →  middle group  →  output group
```

For this tutorial, the important idea is only this: early groups notice simple patterns; later groups combine them into a more useful answer. We do not need to learn the calculations inside each group to use a model well.

## From the small classroom MLP to Gemini

Language models are much larger systems trained on enormous amounts of text and compute, but they still follow the broad idea of many connected parts transforming an input into an output.

When we type a chat message, the model turns it into smaller pieces of text, processes those pieces through its network, and predicts the next piece of its reply. It repeats this rapidly until it has produced an answer.

---

# **Part 1: Two different decisions**

People often combine these terms, but they answer different questions.

## Large model vs small model

This describes the model itself—especially its parameter count, memory requirement, capability, and inference cost.

- A **large model** usually offers stronger reasoning and broader capability, but needs more memory and compute.
- A **small language model (SLM)** is easier and cheaper to run, but may be less capable on difficult or unfamiliar tasks.

The parameter count is commonly written as `1B`, `7B`, or `70B`, where `B` is a **billion parameters**. Parameter count is useful, but it is not a complete quality score; architecture, training data, quantization, and the task also matter.

### Cloud: borrow capability

With Gemini, OpenAI, or another hosted model, we send our prompt to a provider and receive an answer.

This is great when we want to start quickly, use very capable models, handle many users, or avoid buying and managing expensive hardware.

But we are sending data outside our own machine. We need to understand the provider's data policy, our organisation's contract, and whether the data is appropriate to send.

### Local: own the capability

With a local model, the model runs on hardware we control: a laptop, workstation, or company server.

This can be useful when data must stay inside the organisation, internet access is unreliable, or we want control over the exact model and version.

But local is not automatically easier or cheaper. We now own the hardware, model downloads, memory limits, updates, speed, monitoring, and security.

### The real trade-off

```text
Cloud:  less infrastructure work, more provider dependence
Local:  more control, more infrastructure responsibility
```

---

# **Part 2: Why use cloud models?**

Cloud APIs let a team consume model capability without first becoming a GPU infrastructure team.

## Advantages

- **Fast start:** authenticate, make an API call, and build.
- **Access to frontier capability:** the provider trains and serves models that may be impractical to run locally.
- **Elastic capacity:** the provider manages much of the serving infrastructure.
- **Managed improvements:** model infrastructure, optimizations, and availability are handled by the provider.
- **Multimodal and managed features:** one API may support text, images, audio, tools, structured output, and safety controls.

## Trade-offs

- Requests depend on provider availability and also providers can restrict access (Fable).
- Usage can create a recurring, request- or token-based cost.
- Data leaves the local process, so the provider's data terms and your organization's policies matter.
- Model versions, limits, and provider behavior can change (frequently model capability changes in codex/claude code).


---

# **Part 3: Build a Gemini chatbot in VS Code**


We will now turn that single model call into a small multi-turn chatbot. We will use a normal Python script instead of a notebook so the demonstration runs directly in VS Code.

## 1. Create the project

Open the VS Code terminal and run:

```bash
mkdir week3-models
cd week3-models
python3 -m venv .venv
```

Activate the environment:

```bash
# macOS or Linux
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Then install the current Google SDK:

```bash
python -m pip install -U google-genai
```

In VS Code, select the Python interpreter inside `.venv` if it is not selected automatically.

## 2. Add the API key safely

Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/apikey). To keep it out of the live demo, copy the included template and add the real key to your local `.env` file:

```bash
# macOS or Linux
cp .env.example .env
# Edit .env and replace paste-your-key-here with the real key.
```

The template uses `export`, so this is all you need before running the chatbot:

```bash
source .env
python gemini_chatbot.py
```

> Never paste an API key directly into a Python file or commit it to Git. `.env` is excluded by this folder's `.gitignore`.

## 3. Create `gemini_chatbot.py`

```python
import os
from google import genai


api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Set the GEMINI_API_KEY environment variable first.")

client = genai.Client(api_key=api_key)
MODEL = "gemini-3.5-flash"

# The SDK keeps the conversation history for this chat session.
chat = client.chats.create(model=MODEL)

print("Gemini chatbot is ready. Type /exit to stop.\n")

while True:
    user_message = input("You: ").strip()

    if user_message.lower() in {"/exit", "exit", "quit"}:
        print("Chat ended.")
        break

    if not user_message:
        continue

    try:
        response = chat.send_message(user_message)
        print(f"Gemini: {response.text}\n")
    except Exception as error:
        print(f"Gemini request failed: {error}\n")
```

Run it (after `source .env`):

```bash
python gemini_chatbot.py
```

Try this sequence to prove that it remembers the conversation:

```text
You: My name is Sam and I am learning about local models.
You: What is my name, and what am I learning?
```

The important Gemini-specific lines are still small:

```python
client = genai.Client(api_key=api_key)
```

This creates the client. It does **not** download Gemini to the laptop.

```python
chat = client.chats.create(model=MODEL)
```

This creates a chat session that keeps track of previous turns.

```python
response = chat.send_message(user_message)
```

## OpenRouter hint

[OpenRouter](https://openrouter.ai/docs/quickstart) is a gateway that exposes models from multiple providers through a common API. It can be useful when you want to compare providers or add routing and fallback without integrating every provider separately.

Conceptually:

```text
Your application ──> OpenRouter ──> selected model provider
```

It is still a **provider call**. It adds a routing layer.

---

# **Part 4: What can run locally?**

Many open-weight model families have variants intended for laptops and workstations. Examples include **Gemma**, **Llama**, **Qwen**, **Mistral**, and **Phi**. Their availability and license terms differ, so check the model card and license before organizational use.

## We download weights, not the original training system

When we run a local model, we normally download trained **weights** and use an **inference runtime** to execute them. We are not retraining the model.

## Why quantization matters

Model weights are numbers. Quantization stores many of those numbers at lower precision, reducing memory and often making local inference faster, usually with some quality trade-off.

A rough lower-bound illustration for weight storage is:

```text
7 billion parameters × 2 bytes at 16-bit ≈ 14 GB
7 billion parameters × 0.5 bytes at 4-bit ≈ 3.5 GB
```

Real memory use is higher because inference also needs runtime overhead and a **KV cache** whose size grows with context length. This is why “the model file fits on disk” does not guarantee that it will run comfortably in memory.

## Why run locally?

- Offline or low-connectivity operation after the model is downloaded.
- More control over model version and serving configuration.
- Data can remain on infrastructure you control when the entire pipeline is local.
- No per-request provider bill; useful for suitable, steady workloads.
- Experimentation with open weights, quantization, fine-tuning, and custom serving.

## Local does not automatically mean safe or free

- The machine, logs, prompts, model server, and application still need security controls.
- Model downloads are large and licenses impose conditions.
- Hardware, electricity, engineering, monitoring, and maintenance have costs.
- Smaller local models may hallucinate more or fail tasks that a stronger cloud model handles.
- A server bound to `0.0.0.0` is no longer accessible only from the same machine; do not expose an unauthenticated local model server accidentally.

---

# **Part 5: Four ways to access local models**

Gemma, Llama, Qwen, and Mistral are examples of **models**: they are the trained systems that generate text.

Ollama, llama.cpp, LM Studio, and vLLM are **runtimes/tools**: they download, load, run, and sometimes serve those models to an application.

```text
Model   = the trained pattern-finder
Runtime = the software that loads and runs it
```

The same model family can often run through more than one tool. We choose the tool based on the experience and infrastructure we need.

| Tool | What it feels like | Why someone would choose it |
|---|---|---|
| **Ollama** | “Download a model and start chatting.” | Simple CLI and local API; ideal for laptops, learning, prototypes, and developer tools. |
| **LM Studio** | “Try models through a desktop app.” | Visual discovery, downloading, loading, and testing without starting in the terminal. |
| **llama.cpp** | “A lower-level engine with more knobs.” | Lightweight execution, GGUF models, broad hardware support, and greater control over CPU/GPU use. |
| **vLLM** | “Serve models to many users.” | GPU infrastructure, concurrent requests, and production-style throughput. |

## Ollama

Ollama gives us a simple way to download a model, run it locally, and call it from Python. It is the tool we will demonstrate because it keeps the focus on the chatbot rather than on model files, GPU settings, and server configuration.

```bash
ollama run gemma4:12b
```

That command downloads the model if needed, loads it, and opens a chat. Ollama also runs a local service, so our Python chatbot can call a model on the same machine.


> Ollama is a good choice for this learning demo, not automatically the right choice for every production system.

See the [Ollama quickstart](https://docs.ollama.com/quickstart).

## llama.cpp

`llama.cpp` is a lower-level inference engine written mainly in C/C++. It loads quantized models and performs the calculations needed to generate text on a CPU, GPU, or a mix of both.

Ollama uses llama.cpp as one of its supported backends. Ollama gives us the easier experience; llama.cpp exposes more controls. We would use llama.cpp directly when we need to choose the exact model file, quantization, CPU/GPU split, or server settings.

The model generates one token at a time. The **KV cache** keeps useful information from earlier tokens, so the model does not start the entire conversation from zero each time. A longer conversation needs more cache memory.

### Why CPU/GPU offload matters

- If the model fits in fast GPU memory, it is usually faster.
- If it does not fit, llama.cpp can use both system memory and the CPU, but generation may slow down.
- Quantization makes the model smaller; this can help it fit, with a possible quality trade-off.

### One practical note: speed and memory

- Models generate **tokens**—small pieces of text—one at a time. More tokens per second means the answer appears faster.
- The model weights need RAM or GPU memory. The conversation also needs extra memory while the model is answering.
- If a model is too slow or will not fit, try a smaller model or a more heavily quantized version.

For this tutorial, simply notice the difference when you run Ollama: your own machine is now doing the work that Gemini's cloud infrastructure did earlier.

---

# **Part 6: Run our first local model**

## 1. Install and start Ollama

Install Ollama using the instructions for your operating system at [ollama.com/download](https://ollama.com/download).

Then download and open a chat with a small model:

```bash
ollama run gemma4:12b
```

The first run downloads the model. Later runs use the local copy. At the interactive prompt, try:

```text
Explain the difference between a process and a thread to a junior developer.
Use one analogy and no more than 100 words.
```

Type `/bye` to exit the interactive chat. Ollama continues to provide its local service in the background.

> The tutorial uses `gemma4:12b` because it is already available on the demonstration machine. Choose a model that fits the available memory, and download it before class; model files can be large and venue Wi-Fi is unpredictable.

## 2. Build the same chatbot with Ollama

Install Ollama's official Python client in the same virtual environment:

```bash
python -m pip install -U ollama
```

Create `ollama_chatbot.py`:

```python
from ollama import chat


MODEL = "gemma4:12b"
messages = []

print("Ollama chatbot is ready. Type /exit to stop.\n")

while True:
    user_message = input("You: ").strip()

    if user_message.lower() in {"/exit", "exit", "quit"}:
        print("Chat ended.")
        break

    if not user_message:
        continue

    # Ollama expects the conversation as user/assistant message objects.
    messages.append({"role": "user", "content": user_message})

    try:
        response = chat(model=MODEL, messages=messages)
    except Exception as error:
        print(
            "Could not reach Ollama. Confirm that Ollama is running "
            f"and {MODEL} is installed. Details: {error}\n"
        )
        messages.pop()  # Remove the unanswered user turn.
        continue

    assistant_message = response.message.content
    if assistant_message is None:
        messages.pop()  # Remove the unanswered user turn.
        print("Ollama returned an empty response. Please try again.\n")
        continue

    messages.append({"role": "assistant", "content": assistant_message})
    print(f"Ollama: {assistant_message}\n")
```

Run it:

```bash
python ollama_chatbot.py
```

### Where is the conversation memory?

The model itself does not permanently remember earlier terminal input.

- In `gemini_chatbot.py`, the Gemini SDK's chat helper maintains the history for the active chat session.
- In `ollama_chatbot.py`, our Python code stores the `messages` list and sends that history with every request.
- Closing either program loses this in-memory conversation unless we deliberately save it somewhere.

This distinction will matter later when building chat applications with databases and user sessions.

---

# **Troubleshooting before the live session**

| Problem | Check |
|---|---|
| `python` or `python3` is not found | Install Python and restart the VS Code terminal |
| VS Code cannot import `google.genai` | Select `.venv` as the interpreter and run the install command again |
| Gemini reports an authentication error | Confirm `GEMINI_API_KEY` exists in the same terminal used to run Python |
| `ollama` is not found | Install Ollama, then restart the terminal |
| Cannot connect to port `11434` | Start/open Ollama and confirm its service is running |
| Ollama says the model is missing | Run `ollama run gemma4:12b` once to download it |
| Local generation is very slow | Use a smaller model, shorten the prompt/context, and close memory-heavy applications |

## Pre-flight checklist

- Install Python, VS Code, the VS Code Python extension, and Ollama.
- Create and test the Gemini API key without showing it on screen.
- Pre-download the Ollama model on the presentation machine.
- Run both scripts once from a clean VS Code terminal.
- Keep sample outputs available in case the network or API is unavailable.
- Avoid live-installing llama.cpp, LM Studio, and vLLM; show their roles and docs, then keep the hands-on path focused on Ollama.


---

# **Final takeaway**

A model is not only a name. It is part of a system with a runtime, hardware, an interface, operational ownership, and constraints.

---

## **Official references**
 

- [Gemini API quickstart](https://ai.google.dev/gemini-api/docs/quickstart)
- [Gemini text generation](https://ai.google.dev/gemini-api/docs/text-generation)
- [OpenRouter quickstart](https://openrouter.ai/docs/quickstart)
- [Ollama quickstart](https://docs.ollama.com/quickstart)
- [Ollama API](https://docs.ollama.com/api/introduction)
- [Ollama Python client](https://github.com/ollama/ollama-python)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [llama.cpp benchmarking tool](https://github.com/ggml-org/llama.cpp/tree/master/tools/llama-bench)
- [llama.cpp server and metrics](https://github.com/ggml-org/llama.cpp/tree/master/tools/server)
- [LM Studio local server](https://lmstudio.ai/docs/developer/core/server)
- [vLLM quickstart](https://docs.vllm.ai/en/latest/getting_started/quickstart/)
