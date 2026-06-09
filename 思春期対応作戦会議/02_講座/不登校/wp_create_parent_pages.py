"""
WordPress 親ページ一括作成スクリプト

作成するページ：
  【外向け・集客用】
  - 無料コンテンツ
  - 相談・サロン

  【受講者専用】
  - セルフケア講座
  - 子どもサポート講座

使い方:
  python wp_create_parent_pages.py
"""

import requests
from requests.auth import HTTPBasicAuth
import sys
sys.path.append('../self_care')
from wp_config import WP_URL, WP_USER, WP_APP_PASSWORD


def create_page(title, slug, status='draft'):
    """固定ページを新規作成"""
    url = f'{WP_URL}/wp-json/wp/v2/pages'
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    response = requests.post(url, json={
        'title': title,
        'content': '',
        'status': status,
        'slug': slug,
    }, auth=auth)
    if response.status_code in (200, 201):
        r = response.json()
        print(f'作成完了: 【{r["id"]}】{r["title"]["rendered"]}')
        print(f'  編集URL: {WP_URL}/wp-admin/post.php?post={r["id"]}&action=edit')
        return r['id']
    else:
        print(f'エラー（{title}）: {response.status_code}')
        print(response.text)
        return None


if __name__ == '__main__':
    print('親ページを作成しています...\n')

    print('── 外向け・集客用 ──')
    create_page('無料コンテンツ', 'free-content')
    create_page('相談・サロン', 'consultation-salon')

    print('\n── 受講者専用 ──')
    create_page('セルフケア講座', 'self-care-course')
    create_page('子どもサポート講座', 'child-support-course')

    print('\n完了しました。')
    print('次のステップ：')
    print('  各ページの編集画面で「親ページ」を設定してください。')
    print('  例）不登校支援LP → 親ページ：無料コンテンツ')
