#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# アプリ設定・定数管理

import os
from dotenv import load_dotenv

# 親ディレクトリの.envを読み込む
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Notion設定
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
NOTION_CLIENT_DB_ID = os.getenv("NOTION_CLIENT_DB_ID", "4d430e2fc8ad41a29362cdf1994d507a")
NOTION_COMM_DB_ID = os.getenv("NOTION_COMM_DB_ID", "63beeef39d0745be8d0a89b2bed280a2")
NOTION_VERSION = "2022-06-28"

# Gemini設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"

# Anthropic設定（フォールバック用）
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Flask設定
APP_HOST = "127.0.0.1"
APP_PORT = 5000
