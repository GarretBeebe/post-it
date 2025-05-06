# post-it 🗞️

A lightweight CLI tool to post photos and text to Facebook, X (Twitter), BlueSky, and Substack.

## Features

- ✅ Posts to multiple social platforms
- 🔐 Uses `.env` for secure credentials
- 🖼️ Supports text and image posts
- ⚙️ Subcommands for platform control

## Installation

```bash
git clone https://github.com/yourusername/post-it.git
cd post-it
pip install .
```

## Setup

1. Copy `.env.example` to `.env`
2. Add your API credentials

```bash
cp .env.example .env
```

## Usage

```bash
post-it "Your caption here" -i path/to/image.jpg --all
```

Or selectively:

```bash
post-it "Just BlueSky" -i img.jpg --bluesky
```

## Platforms Supported

- Facebook Pages (via Graph API)
- X (Twitter v1.1 API)
- BlueSky (via AT Protocol)
- Substack (simulated, no API)

## License

MIT
