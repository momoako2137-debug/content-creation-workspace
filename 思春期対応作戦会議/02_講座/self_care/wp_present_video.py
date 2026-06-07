"""
プレゼント動画ページ WordPress 作成スクリプト

使い方:
  python wp_present_video.py          # 新規作成（下書き・固定ページ）
  python wp_present_video.py update   # 既存ページを上書き更新

※ 公開設定は下書き。URLが確定したらモモさんが確認後に公開してください。
"""

import sys
import requests
from requests.auth import HTTPBasicAuth
from wp_config import WP_URL, WP_USER, WP_APP_PASSWORD

# 既存ページID（更新モード用。ページ作成後に発行されたIDをここに記入する）
EXISTING_PAGE_ID = 1499

# ストアカURL
KOJIN_SODAN_URL = 'https://www.street-academy.com/onetime/services/3620?conversion_name=direct_message&tracking_code=0b90b3eda0dc6d14208ad59b78d98c5d'
OK_SALON_URL = 'https://www.street-academy.com/subscription/services/3067?conversion_name=direct_message&tracking_code=878ced76ab0564e36e3447154ddeac9b&d_code=LP38iLry'


# ── Gutenberg ブロック記法 ─────────────────────────────────────────

def p(html):
    """段落"""
    return f'<!-- wp:paragraph -->\n<p>{html}</p>\n<!-- /wp:paragraph -->'


def sep():
    """区切り線"""
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


def youtube_embed(url):
    """YouTube動画埋め込みブロック"""
    return (
        f'<!-- wp:embed {{"url":"{url}","type":"video","providerNameSlug":"youtube",'
        '"responsive":true,"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} -->\n'
        '<figure class="wp-block-embed is-type-video is-provider-youtube '
        'wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio">'
        '<div class="wp-block-embed__wrapper">\n'
        f'{url}\n'
        '</div></figure>\n'
        '<!-- /wp:embed -->'
    )


def button(label, href):
    """CTAボタン（色：#FABE57）"""
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

        # ── 自己紹介 ──
        p('はじめまして。思春期子育て専門保健師の桃木亜子です。'),
        p('思春期のお父さん・お母さんが、子育ての不安や焦りから抜け出して、子どもとよい関係を築き、思春期の子育てを楽に・楽しく・幸せに——そして親子で未来を描けるようなサポートをしています。'),

        sep(),

        # ── 受講者の声 ──
        p('まず、実際に受講してくださった方の声をご覧ください。'),
        youtube_embed('https://www.youtube.com/watch?v=Mc3DjO8zcBU'),

        sep(),

        # ── メインメッセージ ──
        p('思春期の子育ては、学ばなくてもできます。<br>でも、学んだら変わります。'),
        p('子どもが「学校に行きたくない」と言い出したとき、どうすればいいかわからない——'),
        p('そんなときに、心の仕組みを使って対応を整えることは、とても効果的です。'),
        p('「何をすればいいかわからない」が、「これをしよう」に変わる。<br>そのきっかけを、この動画でお伝えします。'),
        youtube_embed('https://youtu.be/UJP_B0sxpxc'),

        sep(),

        # ── 個別相談・段階説明 ──
        p('個別相談・OKサロンはストアカを通じてご利用いただけます。ストアカは登録が必要ですが、無料で登録でき、安心して使えるプラットフォームです。'),

        group_pink([
            p('学校に行っていないお子さんには段階があります。<br>今はどういう状況なのか。その段階に応じて、対応を変えていく必要があります。'),
            p('社会から守る必要がある時期、<br>エネルギーを貯めていく時期、<br>社会とつながるアプローチをする時期。'),
            p('今のお子さんの状態に合った対応をして、子どもが「安心・安全」を感じながら一歩ずつ進んでいく——'),
            p('状況や段階に応じた作戦を、一緒に立てていきましょう。'),
        ]),

        button('保健師と話そう🍀個別相談はこちら', KOJIN_SODAN_URL),

        sep(),

        # ── OKサロン ──
        p('思春期のママがつながる、OKサロン。'),
        p('思春期の悩みや不登校のことを、本当に理解してくれる人が身近にいるお母さんは少ないと感じています。'),
        p('だからこそ、わかり合えて支え合える仲間が必要です。'),

        group_pink([
            p('OKサロンは、思春期の子を持つお母さん同士がつながり、子育ての迷いや苦しさを話し合い、支え合う場所です。毎月、心理学・脳科学の視点から情報提供もしています。'),
            p('初月無料ですので、まずは1か月ぜひ参加してみてください。'),
        ]),

        button('OKサロン（初月無料）はこちら', OK_SALON_URL),

    ]
    return '\n\n'.join(blocks)


# ── API 操作 ──────────────────────────────────────────────────────

def post_page(title, content, status='draft'):
    """新規固定ページ作成（下書き）"""
    url = f'{WP_URL}/wp-json/wp/v2/pages'
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    response = requests.post(url, json={
        'title': title,
        'content': content,
        'status': status,
        'slug': 'present-futokou',
    }, auth=auth)
    _print_result(response, '作成')


def update_page(page_id, title, content, status='draft'):
    """既存ページを上書き更新"""
    url = f'{WP_URL}/wp-json/wp/v2/pages/{page_id}'
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
        print(f'URL: {r["link"]}')
        print(f'編集URL: {WP_URL}/wp-admin/post.php?post={r["id"]}&action=edit')
    else:
        print(f'エラー: {response.status_code}')
        print(response.text)


# ── エントリポイント ──────────────────────────────────────────────

if __name__ == '__main__':
    title = 'プレゼント動画'
    content = build_content()

    if len(sys.argv) > 1 and sys.argv[1] == 'update':
        if EXISTING_PAGE_ID is None:
            print('エラー：EXISTING_PAGE_ID を記入してから update モードを実行してください。')
        else:
            print(f'既存ページ（ID: {EXISTING_PAGE_ID}）を更新中...')
            update_page(EXISTING_PAGE_ID, title, content)
    else:
        print('WordPressに接続中...')
        post_page(title, content)
