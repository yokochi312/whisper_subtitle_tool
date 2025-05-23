import whisper
import os

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) % 3600 // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

# モデル読み込み
model = whisper.load_model("small")

# 入力ファイル（動画 or 音声）
input_path = "videos/okukku.mp4"
assert os.path.exists(input_path), f"ファイルが存在しません: {input_path}"

# 出力フォルダとファイル名の設定
output_dir = "subtitles"
os.makedirs(output_dir, exist_ok=True)  # フォルダがなければ作る
output_path = os.path.join(output_dir, "okukku.srt")

# 文字起こし
result = model.transcribe(input_path, language="ja")

# SRTファイル出力
with open(output_path, "w", encoding="utf-8") as f:
    for i, segment in enumerate(result["segments"], start=1):
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip()

        f.write(f"{i}\n")
        f.write(f"{start} --> {end}\n")
        f.write(f"{text}\n\n")

print(f"✅ SRTファイルを保存しました: {output_path}")