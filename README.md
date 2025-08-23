# 📸 Python Playwright Pageshot

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-latest-orange.svg)](https://playwright.dev/)
[![Container Ready](https://img.shields.io/badge/container-ready-purple.svg)](https://podman.io/)

**A powerful and feature-rich Python utility for capturing high-quality web page screenshots using Microsoft Playwright** 🎯

*Fast • Reliable • Cross-browser • Container-ready*

</div>

---

## ✨ Features

🎨 **Advanced Screenshot Options**
- 📱 Full-page or viewport screenshots
- 🖼️ Multiple formats: PNG & JPEG with quality control
- 📏 CSS or device pixel scaling
- 🎭 Background omission support
- 🔍 Network idle wait for complete page loading

🌐 **Multi-Browser Support**
- 🦊 **Firefox** (default)
- 🌊 **Chromium/Chrome**
- 🧭 **WebKit/Safari**

🛡️ **Enterprise Features**
- 🔒 Proxy support with authentication
- 📁 Configurable output directories
- 📊 File size validation (10MB limit)
- 🚨 Error handling and validation
- 🐳 Container-ready deployment

## 🚀 Quick Start

### 📦 Prerequisites

**Option 1: Python Environment**
```bash
# Install Python dependencies
python3 -m venv .
source bin/activate
pip install pytest-playwright
playwright install
```

**Option 2: Container Environment**
```bash
# Install container runtime
apt update && apt install -y podman
# or use Docker: apt install -y docker.io
```

### ⚡ Basic Usage

**Simple screenshot:**
```bash
python pageshot.py "https://example.com"
```

**With custom options:**
```bash
python pageshot.py "https://example.com" \
    --browser chromium \
    --img-type jpeg \
    --quality 95 \
    --data-dir ./screenshots
```

**Using containers:**
```bash
bash podman-run-playwright.bash
```

## 🛠️ Advanced Usage

### 📋 Command Line Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `uri` | Target URL to capture | `https://www.python.org/` | `"https://github.com"` |
| `--browser` | Browser engine | `firefox` | `chromium`, `webkit` |
| `--img-type` | Image format | `png` | `jpeg` |
| `--quality` | JPEG quality (0-100) | `90` | `85` |
| `--scale` | Screenshot scale | `css` | `device` |
| `--data-dir` | Output directory | `./data` | `./screenshots` |
| `--omit-background` | Remove page background | `false` | `--omit-background` |
| `--no-full-page` | Viewport only | `false` | `--no-full-page` |
| `--proxy-server` | Proxy URL | - | `http://proxy:8080` |
| `--proxy-username` | Proxy username | - | `user` |
| `--proxy-password` | Proxy password | - | `pass` |

### 🎯 Usage Examples

**High-quality JPEG with custom browser:**
```bash
python pageshot.py "https://docs.python.org" \
    --browser webkit \
    --img-type jpeg \
    --quality 100 \
    --scale device
```

**Corporate environment with proxy:**
```bash
python pageshot.py "https://internal.company.com" \
    --proxy-server "http://proxy.corp.com:8080" \
    --proxy-username "employee" \
    --proxy-password "secret123"
```

**Viewport screenshot without background:**
```bash
python pageshot.py "https://example.com" \
    --no-full-page \
    --omit-background \
    --data-dir "./captures"
```

## 🐳 Container Usage

The project includes a ready-to-use container setup:

```bash
# Build and run in one command
bash podman-run-playwright.bash

# Or manually:
podman build -t playwright:pageshot .
podman run -v ./data:/playwright/data playwright:pageshot \
    pageshot.py "https://your-target-site.com"
```

**Container features:**
- 🔒 Secure non-root execution
- 📂 Volume mounting for output
- 🚀 Pre-installed Playwright browsers
- 🐧 Debian-based with minimal dependencies

## 📁 Output

Screenshots are saved with automatically generated filenames based on the URL:
- **Format**: `domain_path.{png|jpeg}`
- **Location**: `./data/` (or specified directory)
- **Example**: `github_com.png`, `docs_python_org.jpeg`

## 🔧 Installation Methods

### 🐍 Python Virtual Environment (Recommended)

```bash
# Create and activate virtual environment
python -m venv playwright-env
source playwright-env/bin/activate  # On Windows: playwright-env\Scripts\activate

# Install dependencies
pip install pytest-playwright
playwright install

# Run the tool
python pageshot.py "https://example.com"
```

### 🐳 Container Deployment

```bash
# Clone repository
git clone https://github.com/PhilippGoecke/PythonPlaywrightPageshot.git
cd PythonPlaywrightPageshot

# Build and run
bash podman-run-playwright.bash
```

### 📦 System-wide Installation

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install -y python3-pip python3-venv

# Install Playwright
pip3 install playwright
playwright install
```

## 🚨 Troubleshooting

**Common Issues:**

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: playwright` | Run `pip install playwright` |
| `Browser not found` | Execute `playwright install` |
| Permission denied | Check file/directory permissions |
| Large file warning | Image exceeds 10MB limit |
| Network timeout | Check internet connection/proxy settings |

**Debug mode:**
```bash
# Enable verbose output
python -v pageshot.py "https://example.com"
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/PythonPlaywrightPageshot.git`
3. **Create** a feature branch: `git checkout -b feature/amazing-feature`
4. **Make** your changes
5. **Test** thoroughly
6. **Commit** your changes: `git commit -m 'Add amazing feature'`
7. **Push** to your branch: `git push origin feature/amazing-feature`
8. **Open** a Pull Request

### 🧪 Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/PhilippGoecke/PythonPlaywrightPageshot.git
cd PythonPlaywrightPageshot
python -m venv venv
source venv/bin/activate
pip install pytest-playwright
playwright install
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Resources

- 📖 **[Playwright Documentation](https://playwright.dev/python/docs/intro)** - Official Playwright Python docs
- 📦 **[Playwright PyPI](https://pypi.org/project/playwright/)** - Python package on PyPI
- 🐳 **[Podman Documentation](https://docs.podman.io/)** - Container runtime documentation
- 🌐 **[Docker Hub](https://hub.docker.com/)** - Alternative container registry

## 🙏 Acknowledgments

- **Microsoft Playwright Team** for the amazing browser automation framework
- **Open Source Community** for continuous inspiration and support
- **Contributors** who help make this project better

---

<div align="center">

**⭐ Star this repository if you find it useful!**

Made with ❤️ and Python 🐍

</div>
