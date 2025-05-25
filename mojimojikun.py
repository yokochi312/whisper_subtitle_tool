import whisper
import os
import subprocess

# ===== ASS字幕用の時間フォーマット関数 =====
def format_ass_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)  # centiseconds
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"

# ===== 字幕スタイル定義（ASSヘッダー） =====
ASS_STYLE = """[Script Info]
Title: Whisper Subtitles
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,30,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,2,0,2,10,10,30,1
# 🔧 フォント名: 「ヒラギノ角ゴ Pro W3」 → 例: Noto Sans JP, Arial など
# 🔧 フォントサイズ: 「50」 → 例: 30（小さめ）、60（大きめ）
# 🔧 文字色: 「&H00FFFFFF」 → 白文字。&H00FFFF00（青）、&H0000FF00（緑）など
# 🔧 アウトライン（縁取り）: 「2」 → 太さ（0〜3あたりが見やすい）
# 🔧 シャドウ（影）: 「0」 → 1以上で影がつく
# 🔧 表示位置: 「2」→下中央（1:左下, 2:中央下, 3:右下, 8:中央上 など）

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# ===== Whisperモデル読み込み =====
model = whisper.load_model("small")

# ===== 入力ファイル設定 =====
input_path = "videos/sakura.MOV"
assert os.path.exists(input_path), f"ファイルが存在しません: {input_path}"

# ===== 出力パス設定 =====
output_dir = "subtitles"
os.makedirs(output_dir, exist_ok=True)
ass_path = os.path.join(output_dir, "sakura.ass")
output_video_path = "videos/sakura_with_subtitles.mp4"

# ===== Whisperで文字起こし =====
result = model.transcribe(input_path, language="ja", fp16=False)

# ===== ASS字幕ファイルの生成 =====
with open(ass_path, "w", encoding="utf-8") as f:
    f.write(ASS_STYLE)
    for segment in result["segments"]:
        start = format_ass_timestamp(segment["start"])
        end = format_ass_timestamp(segment["end"])
        text = segment["text"].strip().replace("\n", "\\N")
        f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")

print(f"✅ ASS字幕ファイル生成完了: {ass_path}")

# ===== ffmpegで字幕焼き付け（ハードサブ） =====
cmd = [
    "ffmpeg",
    "-i", input_path,
    "-vf", f"ass={ass_path}",
    "-c:a", "copy",
    output_video_path
]

print("🎬 字幕付き動画を生成中...")
subprocess.run(cmd, check=True)
print(f"✅ 字幕付き動画を保存しました: {output_video_path}")