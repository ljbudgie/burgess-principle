# Sovereign Mode — Run Iris on Your Own Hardware

The Burgess Principle asks one question: *was a human there?* Sovereign Mode extends that philosophy to the tool itself — **you** control the hardware, the model, and the data. Nothing leaves your device.

Run Iris locally with no cloud, no API keys, no external servers, and no telemetry. Your conversations stay on your machine. If you can run a Python script, you can run Sovereign Mode. It works alongside the existing cloud deployment — you choose which mode fits your needs.

---

## What You Need

You don't need any technical expertise — just a computer and a few minutes.

- A computer with at least **8 GB of RAM** (16 GB recommended).
- **Python 3.11 or later** installed.
- A **GGUF model file** (the install script downloads one for you automatically).
- About **3 GB of free disk space** for the model.

Sovereign Mode works on macOS, Linux, and Windows — including Raspberry Pi 4/5 (with reduced speed).

---

## Quick Start

### 1. Install dependencies

Choose your platform:

**macOS:**
```bash
bash scripts/install-macos.sh
```

**Linux (Debian/Ubuntu):**
```bash
bash scripts/install-linux.sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\install-windows.ps1
```

Each script installs Python dependencies and downloads a small default model (~2.2 GB) if you don't have one already.

### 2. Start Iris

```bash
python3 iris-local.py
```

Iris will load the model, start a local server, and open the chat interface in your browser at `http://localhost:8000`.

That's it. You're running Iris with zero cloud dependency.

---

## Phone Setup

Once `python3 iris-local.py` is running, open `http://localhost:8000` on the phone you want to use as your daily sovereign advocate.

1. Open the site in the mobile browser that lives on the device.
2. Use **Add to Home Screen / Install App** so Iris launches in standalone mode.
3. Tap **+ New Claim** to jump straight into the mobile claim builder.
4. Open **Claim profile & phone settings** and save the local profile fields once.
5. Set a Vault passphrase, then generate or save claims directly from the phone.
6. Use **Export Vault** / **Import Vault** to move the encrypted phone vault between the phone and a laptop with a `.vault` file.

The phone PWA keeps the claim profile, encrypted local vault copies, 14-day reminders, quick actions, and service-worker notifications on the device. Nothing is sent to any external service.

---

## Configuration

Settings live in `iris-config.json` in the project root:

```json
{
    "model_path": "models/model.gguf",
    "context_size": 2048,
    "port": 8000,
    "gpu_acceleration": false
}
```

| Setting | What it does | Default |
|---|---|---|
| `model_path` | Path to your GGUF model file | `models/model.gguf` |
| `context_size` | How many tokens of conversation the model can see at once | `2048` |
| `port` | Which port the local server runs on | `8000` |
| `gpu_acceleration` | Use your GPU for faster inference (requires compatible hardware) | `false` |

You can also override settings from the command line:

```bash
python3 iris-local.py --model models/mistral-7b.gguf --port 9000 --gpu
```

Run `python3 iris-local.py --help` for all options.

---

## Recommended Models

Any GGUF-format model works. Here are good starting points:

| Model | Size | Best for |
|---|---|---|
| **Phi-3 Mini 4K Q4** | ~2.2 GB | Laptops, quick responses, low memory |
| **Mistral 7B Instruct Q4** | ~4.1 GB | Good balance of quality and speed |
| **Llama 3 8B Instruct Q4** | ~4.7 GB | Highest quality on consumer hardware |

The install scripts download Phi-3 Mini by default. To use a different model:

1. Download the GGUF file from [Hugging Face](https://huggingface.co/models?search=gguf).
2. Place it in the `models/` directory (or anywhere on your system).
3. Update `model_path` in `iris-config.json` or pass `--model` on the command line.

---

## GPU Acceleration

If you have a compatible GPU (NVIDIA with CUDA, Apple Silicon with Metal), you can speed up inference significantly:

1. Install the GPU-enabled version of llama-cpp-python. See the [llama-cpp-python installation guide](https://github.com/abetlen/llama-cpp-python#installation) for your platform.
2. Set `"gpu_acceleration": true` in `iris-config.json` or pass `--gpu` on the command line.

On Apple Silicon Macs, Metal acceleration is usually automatic with the standard pip install.

---

## How It Works

Sovereign Mode runs a lightweight local server that stands in for the cloud API. The same interface you see online — landing page, chat, everything — works identically on your machine. The only difference is that every computation happens locally.

```
┌──────────────────────────────────────────────────────────┐
│                     Your Browser                         │
│                                                          │
│  index.html ─── Full site: landing page + Iris chat      │
│       │                                                  │
│       └── Detects localhost → routes to local server      │
│                                                          │
└────────────────────┬─────────────────────────────────────┘
                     │  http://localhost:8000/api/chat
                     ▼
         ┌───────────────────────┐
         │   iris-local.py       │
         │   (FastAPI server)    │
         │                       │
         │  • Loads system prompt│
         │  • Runs inference     │
         │  • Streams response   │
         │  • No network calls   │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   GGUF Model          │
         │   (on your disk)      │
         │   via llama-cpp-python│
         └───────────────────────┘
```

- The same `index.html` serves both modes — landing page, templates, case studies, and chat. It detects localhost and routes API calls to your local server automatically.
- The system prompt (`iris/system-prompt.md`) is loaded from disk — identical to the cloud version.
- The local server is stateless between sessions. No conversation data is saved unless you export it.
- No telemetry, no analytics, no phone-home behaviour of any kind.

The binary test — SOVEREIGN or NULL — works the same way in both modes. Sovereign Mode simply ensures that even the tool asking the question respects your sovereignty.

---

## Privacy

- **No data leaves your device.** All inference happens locally.
- **No API keys needed.** The model runs directly on your hardware.
- **No server-side storage.** The local server processes and forgets.
- **No telemetry.** Zero tracking, zero analytics, zero network calls.

Your model, your data, your hardware — full sovereignty.

---

## Troubleshooting

**"Model file not found"**
Download a GGUF model and place it at the path shown in the error. The install scripts do this automatically.

**Slow responses**
Try a smaller model (Phi-3 Mini), reduce `context_size` to 1024, or enable GPU acceleration.

**Out of memory**
Use a smaller quantised model (Q4 variants use less RAM than Q8) or reduce `context_size`.

**Port already in use**
Change the port: `python3 iris-local.py --port 9001`

**GPU not detected**
You may need to reinstall llama-cpp-python with GPU support. See the [llama-cpp-python docs](https://github.com/abetlen/llama-cpp-python#installation).

---

## Comparison: Local vs Cloud

| | Sovereign (Local) | Cloud (Vercel) |
|---|---|---|
| **Privacy** | No data leaves your device | Messages sent to external API for inference |
| **Cost** | Free after model download | Requires API key (may have usage costs) |
| **Speed** | Depends on your hardware | Fast (cloud GPU) |
| **Quality** | Good (7B–8B models) | Excellent (Grok-3 default, configurable) |
| **Setup** | Run install script + start | Deploy to Vercel + set API key |
| **Offline** | Works without internet | Requires internet |

Both modes serve the same site and use the same system prompt. Choose based on your priorities.
