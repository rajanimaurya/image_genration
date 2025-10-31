# 🎨 AI Image Generation & Video Creation Pipeline

A **powerful Python application** that transforms text prompts into stunning AI-generated images and turns them into seamless, cinematic video presentations — powered by **Hugging Face's Stable Diffusion XL** model.

---

## 🌟 Features

* 🖼️ **AI Image Generation** — Create **4 unique image variations** from a single text prompt
* 🎭 **Style Variations** — Automatically applies different artistic styles (cinematic, cyberpunk, fantasy, etc.)
* 🎬 **Video Creation** — Convert generated images into smooth **MP4 videos**
* ▶️ **Auto-Play Functionality** — Instantly displays generated images and plays the final video
* ⚡ **Asynchronous Processing** — Super-fast parallel image generation using **async/await**
* 📂 **File-based Trigger System** — Monitors a file for new generation requests automatically

---

## 🧠 Technology Stack

| Component               | Purpose                                  |
| ----------------------- | ---------------------------------------- |
| 🐍 **Python 3.7+**      | Core programming language                |
| 🤗 **Hugging Face API** | Stable Diffusion XL for image generation |
| 🧩 **OpenCV**           | Video creation & playback                |
| 🖌️ **Pillow (PIL)**    | Image processing & display               |
| 🔄 **asyncio**          | Asynchronous API calls                   |
| 🌐 **requests**         | HTTP communication                       |

---

## 📋 Prerequisites

* ✅ Python **3.7 or higher**
* 🔑 **Hugging Face API key**
* 🌍 Stable internet connection

---

## 🔧 Installation & Usage

```bash
# 1️⃣ Clone the repository
git clone https://github.com/rajanimaurya/image_genration.git
cd image_genration

# 2️⃣ Install required packages
pip install opencv-python pillow requests

# 3️⃣ Create required folders
mkdir -p Data Files

# 4️⃣ Set your Hugging Face API key
export HuggingFaceAPIKey="hf_your_actual_key_here"

# 5️⃣ Create your first prompt
echo "beautiful landscape with mountains,true" > Files/ImageGeneration.data

# 6️⃣ Start generating
python your_script_name.py
```

---

### 🔁 Every Time You Want New Images

```bash
# Change the prompt
echo "your new idea here,true" > Files/ImageGeneration.data

# Run the script again
python your_script_name.py
```

---

## ⚡ Quick Test Prompts to Try

* `"colorful butterfly in garden,true"`
* `"modern architecture building,true"`
* `"fantasy castle in clouds,true"`
* `"cyberpunk street at night,true"`

---

## 💡 Pro Tip

For best results, experiment with cinematic, fantasy, or futuristic keywords in your prompts.
Example:

> `"sunset over futuristic city skyline, cinematic lighting,true"`

---

## 👩‍💻 Created with Passion by **Rajani Maurya**

✨ *Innovating at the intersection of AI, creativity, and automation.*

🔗 **Let’s Connect on LinkedIn:** [www.linkedin.com/in/rajanimaurya01](https://www.linkedin.com/in/rajanimaurya01/)
