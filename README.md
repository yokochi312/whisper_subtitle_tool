# 🎧 Whisper Subtitle Tool

Whisperを使って、**動画・音声から自動で文字起こしし、SRT字幕ファイルを生成**するツールです。

## 📌 特徴

- OpenAI Whisperを使用した高精度な音声認識
- 日本語対応
- SRT形式の字幕ファイルを自動生成
- ffmpegと組み合わせて字幕焼き込みも可能！

---

## 🛠 使用技術

- Python 3.10
- [Whisper](https://github.com/openai/whisper)
- ffmpeg
- MacOS（動作確認済）

---

## 🔧 セットアップ

```bash
# 仮想環境推奨
pip install git+https://github.com/openai/whisper.git
brew install ffmpeg