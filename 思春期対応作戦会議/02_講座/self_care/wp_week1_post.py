"""
第1回｜セルフモニタリング 〜自分をちゃんと見る〜 WordPress 投稿作成スクリプト（SWELL）

使い方:
  python wp_week1_post.py          # 新規作成（下書き・投稿）
  python wp_week1_post.py update   # 既存投稿を上書き更新

※ 動画URL・テキストDL URL・ワークシートPDF URL・AI（ジェム）URLは
　 撮影・作成・公開後にWordPress管理画面で手動差し替えしてください。
※ CTA ボタン色は #FABE57（黄色系）。セクション3はピンク背景（#fdf6f7）。
"""

import sys
import requests
from requests.auth import HTTPBasicAuth
from wp_config import WP_URL, WP_USER, WP_APP_PASSWORD

# 既存投稿ID（更新モード用。投稿作成後に発行されたIDをここに記入する）
EXISTING_POST_ID = 1496

# 外部URL
YOGA_PAGE_URL = 'https://karakoko.com/yoga/'

# プレースホルダーURL（モモさんがWordPress管理画面で手動差し替え）
TEXT_DL_URL = '★ここにテキストダウンロードのURLを貼る★'
WORKSHEET_PDF_URL = '★ここにワークシートPDFのURLを貼る★'
CBT_AI_URL = '★ここに認知行動療法AI（Geminiジェム）のURLを貼る★'


# ── Gutenberg ブロック記法で生成 ─────────────────────────────────

def h2(text):
    """見出し（H2）"""
    return (
        '<!-- wp:heading {"className":"wp-block-heading"} -->\n'
        f'<h2 class="wp-block-heading">{text}</h2>\n'
        '<!-- /wp:heading -->'
    )


def p(html):
    """段落"""
    return f'<!-- wp:paragraph -->\n<p>{html}</p>\n<!-- /wp:paragraph -->'


def small_p(html):
    """小さめの段落（注釈用）"""
    return (
        '<!-- wp:paragraph {"fontSize":"small"} -->\n'
        f'<p class="has-small-font-size">{html}</p>\n'
        '<!-- /wp:paragraph -->'
    )


def sep():
    """セクション区切り線"""
    return (
        '<!-- wp:separator -->\n'
        '<hr class="wp-block-separator has-alpha-channel-opacity"/>\n'
        '<!-- /wp:separator -->'
    )


def group_pink(inner_blocks):
    """ピンク背景のグループブロック（#fdf6f7）"""
    style = (
        'background-color:#fdf6f7;border-radius:8px;'
        'padding-top:28px;padding-right:32px;padding-bottom:28px;padding-left:32px'
    )
    return (
        '<!-- wp:group {"style":{"color":{"background":"#fdf6f7"},"border":{"radius":"8px"},'
        '"spacing":{"padding":{"top":"28px","right":"32px","bottom":"28px","left":"32px"}}},'
        '"layout":{"type":"constrained"}} -->\n'
        f'<div class="wp-block-group" style="{style}">\n'
        + '\n\n'.join(inner_blocks) + '\n'
        '</div>\n'
        '<!-- /wp:group -->'
    )


def video_placeholder(label):
    """動画URL貼り付け待ちのプレースホルダー（撮影後に差し替え）"""
    return (
        '<!-- wp:paragraph -->\n'
        f'<p><strong>【{label}】</strong><br>'
        '★ここにYouTubeのURLを貼り付けてください★</p>\n'
        '<!-- /wp:paragraph -->'
    )


def button(label, href):
    """CTA ボタン（色：#FABE57）"""
    return (
        '<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->\n'
        '<div class="wp-block-buttons">'
        '<!-- wp:button {"style":{"border":{"radius":"4px"},'
        '"color":{"background":"#FABE57","text":"#ffffff"}}} -->\n'
        '<div class="wp-block-button">'
        f'<a class="wp-block-button__link wp-element-button" '
        f'href="{href}" target="_blank" rel="noreferrer noopener" '
        'style="border-radius:4px;background-color:#FABE57;color:#ffffff">'
        f'{label}</a></div>\n'
        '<!-- /wp:button --></div>\n'
        '<!-- /wp:buttons -->'
    )


# ── コンテンツ本文 ────────────────────────────────────────────────

def build_content():
    blocks = [

        # ── セクション1：はじめに ──
        h2('はじめに'),
        p('セルフケア講座の第1回がスタートしますね。'),
        p('第1回のテーマは<strong>「セルフモニタリング」</strong>。'),
        p('ゴールは<strong>「自分をちゃんと見る私になる」</strong>です。'),
        p('私を大事にするために、まずは自分自身をちゃんと見ること。'),
        p('自分を観察することが、自分を大事にする第一歩です。'),
        p('動画は3本ありますが、全部一気にやらなくて大丈夫。今のあなたのペースで進めてくださいね。'),
        button('テキストはこちらから', TEXT_DL_URL),
        button('ワークシートをダウンロード', WORKSHEET_PDF_URL),

        sep(),

        # ── セクション2：動画① 体と心のセルフモニタリング ──
        h2('動画① 体と心のセルフモニタリング'),
        p('まずは「自分自身をちゃんと見る」というところからスタートします。'),
        p('体から心にアプローチすると、心も緩んできます。'),
        p('心の天気・体の天気を観察する習慣をつけていきましょう。'),
        p('観察すると変化がわかる。ほおっておかない、早めに手を打つ。これが大切です。'),
        video_placeholder('動画①（体と心のセルフモニタリング）のYouTube URLをここに貼る'),

        sep(),

        # ── セクション3：（ピンク背景）体を整えるためにおすすめのヨガ ──
        h2('体を整えるためにおすすめのヨガ'),
        group_pink([
            p('心が疲れていると感じた時、体からアプローチするのもおすすめです。'),
            p('体が緩むと、心も緩んできます。'),
            p('渋沢典子さんが3本のヨガ動画を作ってくださっています。'),
            button('ヨガ動画ページへ', YOGA_PAGE_URL),
        ]),

        sep(),

        # ── セクション4：動画② 認知行動療法とは（こころのメガネ）──
        h2('動画② 認知行動療法とは（こころのメガネ）'),
        p('ここでは、考え方のクセに気づいて、行動を変えることで気分をラクにする<strong>認知行動療法</strong>についてやさしく解説します。'),
        video_placeholder('動画②（認知行動療法とは）のYouTube URLをここに貼る'),
        p('あなたの「モヤモヤ」を「認知・感情・行動・身体反応」の4つに分けて、認知行動療法の質問で一緒に話してくれるAIです。'),
        button('AIに話してみる', CBT_AI_URL),

        sep(),

        # ── セクション5：動画③ 自動思考 ──
        h2('動画③ 自動思考'),
        p('セルフケアには、自分が考えていること（自動思考）に<strong>「気づく」</strong>ことが第一歩。'),
        video_placeholder('動画③（自動思考について）のYouTube URLをここに貼る'),

        sep(),

        # ── セクション6：今週のワーク ──
        h2('今週のワーク'),
        p('ワークシートを使って、心の天気・体の天気を2週間記録してみましょう（ワークシートはページ冒頭からダウンロードできます）。'),
        p('「モヤモヤしたな」と気づいたら、その出来事を書き出してみてください。'),
        p('認知行動療法AIに、その時の気持ちを話してみるのもおすすめです。'),
        p('完璧にやろうとしなくて大丈夫。<strong>「気づくだけ」でOK</strong>です。'),
        p('ワークが進んだら、メールを返信する形でご連絡くださると嬉しいです。'),

        sep(),

        # ── セクション7：末尾（毎回統一テンプレート）──
        p('気がついたことなどありましたら、何でも伝えてくださいね。'),
        p('必ずお返事します。'),
        small_p('※本記事はセルフケア講座オンラインコース受講生様のみに提供するために作成したものです。第三者への開示・シェアなどは固くお断りさせていただきます。'),

    ]
    return '\n\n'.join(blocks)


# ── API 操作 ──────────────────────────────────────────────────────

def post_article(title, content, status='draft'):
    """新規作成（投稿・下書き）"""
    url = f'{WP_URL}/wp-json/wp/v2/posts'
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    response = requests.post(url, json={
        'title': title,
        'content': content,
        'status': status,
        'slug': 'self_care_1',
    }, auth=auth)
    _print_result(response, '作成')


def update_article(post_id, title, content, status='draft'):
    """既存投稿を上書き更新"""
    url = f'{WP_URL}/wp-json/wp/v2/posts/{post_id}'
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    response = requests.post(url, json={
        'title': title,
        'content': content,
        'status': status,
    }, auth=auth)
    _print_result(response, '更新')


def _print_result(response, action):
    if response.status_code in (200, 201):
        r = response.json()
        print(f'{action}完了: {r["title"]["rendered"]}')
        print(f'公開URL: {r["link"]}')
        print(f'編集URL: {WP_URL}/wp-admin/post.php?post={r["id"]}&action=edit')
    else:
        print(f'エラー: {response.status_code}')
        print(response.text)


# ── エントリポイント ──────────────────────────────────────────────

if __name__ == '__main__':
    title = '第1回｜セルフモニタリング 〜自分をちゃんと見る〜'
    content = build_content()

    if len(sys.argv) > 1 and sys.argv[1] == 'update':
        if EXISTING_POST_ID is None:
            print('エラー：EXISTING_POST_ID を記入してから update モードを実行してください。')
        else:
            print(f'既存投稿（ID: {EXISTING_POST_ID}）を更新中...')
            update_article(EXISTING_POST_ID, title, content)
    else:
        print('WordPressに接続中...')
        post_article(title, content)
