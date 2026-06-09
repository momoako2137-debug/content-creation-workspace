"""
不登校支援LP 固定ページ作成スクリプト

使い方:
  python wp_futouko_lp.py          # 新規作成（下書き）
  python wp_futouko_lp.py publish  # 公開で作成
  python wp_futouko_lp.py update   # 既存ページを上書き更新

※ wp_config.py は 02_講座/self_care/ にあるものを参照します
"""

import sys
import requests
from requests.auth import HTTPBasicAuth
sys.path.append('../self_care')
from wp_config import WP_URL, WP_USER, WP_APP_PASSWORD

# 既存ページID（更新モード用。作成後に発行されたIDをここに記入する）
EXISTING_PAGE_ID = None

# 動画URL
VIDEO_URL = 'https://youtu.be/UJP_B0sxpxc'

# 各リンク
KOJIN_SODAN_URL = 'https://www.street-academy.com/onetime/services/3620?conversion_name=direct_message&tracking_code=0b90b3eda0dc6d14208ad59b78d98c5d'
OK_SALON_URL = 'https://www.street-academy.com/subscription/services/3067?conversion_name=direct_message&tracking_code=878ced76ab0564e36e3447154ddeac9b&d_code=My9mqe1b'
KOJIN_DAIGAKU_URL = 'https://www.street-academy.com/myclass/216641?trigger=search_result'


# ── Gutenberg ブロック記法 ─────────────────────────────────────────

def h1(text):
    """見出し（H1・キャッチコピー用）"""
    return (
        '<!-- wp:heading {"level":1,"textAlign":"center","className":"wp-block-heading"} -->\n'
        f'<h1 class="wp-block-heading has-text-align-center">{text}</h1>\n'
        '<!-- /wp:heading -->'
    )


def h2(text):
    """見出し（H2）"""
    return (
        '<!-- wp:heading {"className":"wp-block-heading"} -->\n'
        f'<h2 class="wp-block-heading">{text}</h2>\n'
        '<!-- /wp:heading -->'
    )


def h3(text):
    """見出し（H3）"""
    return (
        '<!-- wp:heading {"level":3,"className":"wp-block-heading"} -->\n'
        f'<h3 class="wp-block-heading">{text}</h3>\n'
        '<!-- /wp:heading -->'
    )


def p(html, align=''):
    """段落"""
    if align:
        return (
            f'<!-- wp:paragraph {{"textAlign":"{align}"}} -->\n'
            f'<p class="has-text-align-{align}">{html}</p>\n'
            '<!-- /wp:paragraph -->'
        )
    return f'<!-- wp:paragraph -->\n<p>{html}</p>\n<!-- /wp:paragraph -->'


def sep():
    """区切り線"""
    return (
        '<!-- wp:separator -->\n'
        '<hr class="wp-block-separator has-alpha-channel-opacity"/>\n'
        '<!-- /wp:separator -->'
    )


def ul(items):
    """箇条書きリスト"""
    li_html = '\n'.join([f'<li>{item}</li>' for item in items])
    return (
        '<!-- wp:list -->\n'
        f'<ul class="wp-block-list">{li_html}</ul>\n'
        '<!-- /wp:list -->'
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


def group_light(inner_blocks):
    """薄いグレー背景のグループブロック"""
    style = (
        'background-color:#f9f9f9;border-radius:8px;'
        'padding-top:28px;padding-right:32px;padding-bottom:28px;padding-left:32px'
    )
    return (
        '<!-- wp:group {"style":{"color":{"background":"#f9f9f9"},"border":{"radius":"8px"},'
        '"spacing":{"padding":{"top":"28px","right":"32px","bottom":"28px","left":"32px"}}},'
        '"layout":{"type":"constrained"}} -->\n'
        f'<div class="wp-block-group" style="{style}">\n'
        + '\n\n'.join(inner_blocks) + '\n'
        '</div>\n'
        '<!-- /wp:group -->'
    )


def video_embed(url):
    """YouTube動画埋め込み"""
    return (
        f'<!-- wp:embed {{"url":"{url}","type":"video","providerNameSlug":"youtube","responsive":true,"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"}} -->\n'
        f'<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio">'
        f'<div class="wp-block-embed__wrapper">\n{url}\n</div></figure>\n'
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

        # ── キャッチコピー ──
        h1('子どもの回復力を、親が引き出す。'),
        p('「見守るしかない」は、もう終わりにしよう。<br>子どもの回復力を引き出す、親の関わり方があります。', 'center'),

        sep(),

        # ── 共感リスト ──
        h2('こんな状況ではありませんか？'),
        ul([
            '子どもが部屋から出てこない',
            '子どもが荒れる、暴言を吐く',
            '子どもが落ち込んでいて、元気がない',
            '学校に行き渋るようになった',
            '「ほっといて」と言われて、どう関わればいいかわからない',
        ]),
        p('一つでも当てはまるなら、この動画があなたのお役に立てるかもしれません。'),

        sep(),

        # ── 動画 ──
        h2('まずはこちらの動画をご覧ください'),
        p('子どもの回復力を引き出すために、親にできることをお伝えしています。'),
        video_embed(VIDEO_URL),

        sep(),

        # ── 動画後のメッセージ ──
        p('子どもが部屋から出てこない。<br>でも、親にできることはあります。<br>今日から始められる、最初の一歩を。', 'center'),

        sep(),

        # ── 次のステップ ──
        h2('次のステップ'),

        # 個性発見大学
        group_pink([
            h3('まずはここから'),
            p('動画の内容をベースに、マンツーマンで一緒に進めていきます。<br>週1回・1対1で、あなたのお子さんの状況に合わせて進めます。'),
            button('個性発見大学　桃木亜子の講座はこちら', KOJIN_DAIGAKU_URL),
        ]),

        # 個別相談
        group_light([
            h3('保健師に直接相談する'),
            p('今のお子さんの状態を一緒に整理して、段階に応じた作戦を立てます。<br>「様子を見る」で止まらず、今できる具体的な一歩を一緒に考えましょう。'),
            button('保健師と話そう　作戦会議はこちら', KOJIN_SODAN_URL),
        ]),

        # OKサロン
        group_light([
            h3('🍑ママがつながるOKサロン🍑'),
            p('思春期のお母さん同士がつながって、支え合うオンラインサロンです。<br>毎月、心理学・脳科学の視点から情報をお届けしながら、日々の子育てに取り入れていきます。<br><strong>初月無料</strong>でお試しいただけます。'),
            button('OKサロンはこちら', OK_SALON_URL),
        ]),

        sep(),

        # ── プロフィール ──
        h2('桃木亜子（ももきあこ）について'),
        p('<strong>思春期子育て専門保健師</strong>'),
        p('市役所で24年間、保健師として勤務。<br>児童虐待の現場でお母さんの回復を支え続けてきました。'),
        p('「もっと早く出会えていたら」<br>そう悔しい思いをするたびに、問題が大きくなる前に支援できる場を作りたいと思うようになりました。'),
        p('私自身も、思春期の娘2人を育てる母親です。<br>だからこそ、お母さんの葛藤や苦しさが、身に染みてわかります。'),
        p('ストアカでの受講者は377名。<br>専門知識と、母親としての経験の両方からサポートします。'),

    ]
    return '\n\n'.join(blocks)


# ── API操作 ──────────────────────────────────────────────────────

def create_page(title, content, status='draft'):
    """固定ページを新規作成"""
    url = f'{WP_URL}/wp-json/wp/v2/pages'
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    response = requests.post(url, json={
        'title': title,
        'content': content,
        'status': status,
        'slug': 'futouko-support',
    }, auth=auth)
    _print_result(response, '作成')


def update_page(page_id, title, content, status='draft'):
    """既存固定ページを上書き更新"""
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
        print(f'公開URL: {r["link"]}')
        print(f'編集URL: {WP_URL}/wp-admin/post.php?post={r["id"]}&action=edit')
    else:
        print(f'エラー: {response.status_code}')
        print(response.text)


# ── エントリポイント ──────────────────────────────────────────────

if __name__ == '__main__':
    title = '子どもの回復力を、親が引き出す。'
    content = build_content()

    if len(sys.argv) > 1 and sys.argv[1] == 'update':
        if EXISTING_PAGE_ID is None:
            print('エラー：EXISTING_PAGE_ID を記入してから update モードを実行してください。')
        else:
            print(f'既存ページ（ID: {EXISTING_PAGE_ID}）を更新中...')
            update_page(EXISTING_PAGE_ID, title, content)
    elif len(sys.argv) > 1 and sys.argv[1] == 'publish':
        print('WordPressに接続中（公開）...')
        create_page(title, content, status='publish')
    else:
        print('WordPressに接続中（下書き）...')
        create_page(title, content)
