<?php
/**
 * 子テーマ: 親テーマのスタイルシートを読み込む
 */
function swell_child_enqueue_styles() {
    // 親テーマのスタイルを読み込む
    wp_enqueue_style(
        'swell-parent-style',
        get_template_directory_uri() . '/style.css'
    );
    // 新トップページ用カスタムCSS
    wp_enqueue_style(
        'kk-new-top',
        get_stylesheet_directory_uri() . '/assets/css/new-top.css',
        array( 'swell-parent-style' )
    );
}
add_action( 'wp_enqueue_scripts', 'swell_child_enqueue_styles' );
