"""旧セルフケア講座 PDF からテキストを抽出して .txt に書き出す（作業用一時スクリプト）"""
import os
from pathlib import Path
from pypdf import PdfReader

ここ = Path(__file__).parent
出力先 = ここ / "_抽出テキスト"
出力先.mkdir(exist_ok=True)

対象pdf一覧 = [
    "セルフケアコース１第1回｜「私を大切にする」ということ（テスト） (1).pdf",
    "セルフケア講座Vol.1.pdf",
    "【コース2】セルフケア講座Vol.2.pdf",
    "【コース3】セルフケア講座.pdf",
    "【コース4】セルフケア講座 - Google スライド.pdf",
]

for pdf名 in 対象pdf一覧:
    pdfパス = ここ / pdf名
    if not pdfパス.exists():
        print(f"見つからない: {pdf名}")
        continue
    reader = PdfReader(str(pdfパス))
    ページ数 = len(reader.pages)
    出力ファイル = 出力先 / (pdfパス.stem + ".txt")
    with open(出力ファイル, "w", encoding="utf-8") as f:
        f.write(f"# {pdf名}\n")
        f.write(f"# 全{ページ数}ページ\n\n")
        for i, page in enumerate(reader.pages, start=1):
            f.write(f"\n========== ページ {i} ==========\n")
            try:
                f.write(page.extract_text() or "(テキスト抽出不可)")
            except Exception as e:
                f.write(f"(抽出エラー: {e})")
            f.write("\n")
    print(f"出力完了: {出力ファイル.name} ({ページ数}ページ)")
