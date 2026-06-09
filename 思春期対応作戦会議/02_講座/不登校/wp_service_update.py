"""
サービスページ更新スクリプト（ID: 1113）

使い方:
  python wp_service_update.py         # 下書きで更新
  python wp_service_update.py publish # 公開で更新
"""

import sys
import requests
from requests.auth import HTTPBasicAuth
sys.path.append('../self_care')
from wp_config import WP_URL, WP_USER, WP_APP_PASSWORD

PAGE_ID = 1113

KOJIN_SODAN_URL = 'https://www.street-academy.com/onetime/services/3620?conversion_name=direct_message&tracking_code=0b90b3eda0dc6d14208ad59b78d98c5d'
OK_SALON_URL = 'https://www.street-academy.com/subscription/services/3067?conversion_name=direct_message&tracking_code=878ced76ab0564e36e3447154ddeac9b&d_code=My9mqe1b'
KOJIN_DAIGAKU_URL = 'https://www.street-academy.com/myclass/216641?trigger=search_result'


# ── Gutenberg ブロック記法 ─────────────────────────────────────────

def h2(text):
    return (
        '<!-- wp:heading {"className":"wp-block-heading"} -->\n'
        f'<h2 class="wp-block-heading">{text}</h2>\n'
        '<!-- /wp:heading -->'
    )


def p(html, align=''):
    if align:
        return (
            f'<!-- wp:paragraph {{"textAlign":"{align}"}} -->\n'
            f'<p class="has-text-align-{align}">{html}</p>\n'
            '<!-- /wp:paragraph -->'
        )
    return f'<!-- wp:paragraph -->\n<p>{html}</p>\n<!-- /wp:paragraph -->'


def sep():
    return (
        '<!-- wp:separator -->\n'
        '<hr class="wp-block-separator has-alpha-channel-opacity"/>\n'
        '<!-- /wp:separator -->'
    )


def ul(items):
    li_html = '\n'.join([f'<li>{item}</li>' for item in items])
    return (
        '<!-- wp:list -->\n'
        f'<ul class="wp-block-list">{li_html}</ul>\n'
        '<!-- /wp:list -->'
    )


def button(label, href):
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

        # ── 冒頭（スクショはモモさんが後で追加） ──
        p('安心のストアカ講座です', 'center'),

        sep(),

        # ── リード文 ──
        p('思春期の子育ては、戸惑いの連続です。'),
        ul([
            '子どもの暴言に傷つく',
            '話しかけても無視される',
            '私の対応が間違っているのかも',
        ]),
        p('一人で抱え込まないでほしい。<br>一緒だったら、前に進めます。'),
        p('知ること、つながること、相談すること。<br>あなたのペースで、始めてみてください。'),

        sep(),

        # ── ① Cafeでの相談会 ──
        h2('① Cafeでの相談会（岡山市北区）'),
        p('思春期の子育てのモヤモヤや不安を、カフェでほっと一息つきながら話せる場です。<br>保健師によるミニセミナーもあります。おひとりでの参加も大歓迎！'),
        button('詳細はこちら', 'https://karakoko.com/good-luck/'),

        sep(),

        # ── ② OKサロン ──
        h2('② 🍑ママがつながるOKサロン🍑'),
        p('思春期のお母さん同士がつながって、支え合うオンラインサロンです。<br>毎月、心理学・脳科学の視点から子育てに役立つ情報をお届けします。'),
        p('初月無料でお試しいただけます。'),
        button('OKサロンはこちら（ストアカ）', OK_SALON_URL),

        sep(),

        # ── ③ 個別相談 ──
        h2('③ 保健師との個別相談'),
        p('子どもとお母さんの回復力を引き出すために、今できることを一緒に考えます。<br>「様子を見るだけ」に止まらず、段階に応じた具体的な一歩を一緒に立てましょう。'),
        button('個別相談はこちら（ストアカ）', KOJIN_SODAN_URL),

        sep(),

        # ── ④ 不登校 ──
        h2('④ 行き渋り・不登校のお子さんをお持ちの方へ'),
        p('〜子どもと、お母さんの回復力を取り戻そう〜'),
        ul([
            '「どう対応すればいいのかわからない」',
            '「見守るしかないの？」',
            '「私自身がつらい」',
        ]),
        p('子どもとお母さん、両方の回復力を引き出すために親ができることを、保健師がお伝えします。'),
        p('まずは無料動画をご覧ください。'),
        button('無料動画はこちら', 'https://karakoko.com/free-content/futouko-support/'),
        button('個性発見大学・桃木亜子の講座はこちら（ストアカ）', KOJIN_DAIGAKU_URL),

        sep(),

        # ── ⑤ ワークショップ ──
        h2('⑤ 人が集まる場を応援するワークショップ'),
        p('サロン・塾・子育てサークルなど、人が集まる場を運営されている方へ。<br>保健師がうかがって、ワークショップをお届けします。'),
        button('詳細はこちら', 'https://karakoko.com/workshop/'),

        sep(),

        # ── ⑥ メルマガ ──
        h2('⑥ メルマガ'),
        p('思春期の子育てに役立つ情報を、メールでお届けします。'),
        button('メルマガ登録はこちら', 'https://momoako.com/p/r/AV6umcv3'),

        sep(),

        # ── ⑦ 準備中 ──
        h2('⑦ 準備中'),
        p('以下の講座は現在準備中です。'),
        ul([
            '思春期対応作戦会議',
            'セルフケア講座（自分が自分を助ける方法）',
            '子どもをサポートする講座',
        ]),

    ]
    return '\n\n'.join(blocks)


# ── API操作 ──────────────────────────────────────────────────────

def update_page(status='draft'):
    url = f'{WP_URL}/wp-json/wp/v2/posts/{PAGE_ID}'
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    content = build_content()
    response = requests.post(url, json={
        'content': content,
        'status': status,
    }, auth=auth)
    if response.status_code in (200, 201):
        r = response.json()
        print(f'更新完了: {r["title"]["rendered"]}')
        print(f'公開URL: {r["link"]}')
        print(f'編集URL: {WP_URL}/wp-admin/post.php?post={r["id"]}&action=edit')
    else:
        print(f'エラー: {response.status_code}')
        print(response.text)


# ── エントリポイント ──────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'publish':
        print('WordPressに接続中（公開）...')
        update_page(status='publish')
    else:
        print('WordPressに接続中（下書き更新）...')
        update_page(status='draft')
