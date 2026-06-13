<?php
/**
 * Template Name: 新トップページ
 *
 * karakoko.com 用 新トップページテンプレート
 * 確認後に「フロントページ」と差し替えてください
 */

// このページ専用CSS・フォントをheadに直接追加
add_action( 'wp_head', function() {
    echo '<link rel="preconnect" href="https://fonts.googleapis.com">';
    echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>';
    echo '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;600&display=swap">';
    echo '<link rel="stylesheet" href="' . get_stylesheet_directory_uri() . '/assets/css/new-top.css?v=3">';
} );

get_header();
?>

<main class="kk-top">

  <!-- =====================================================
       ファーストビュー
  ===================================================== -->
  <section class="kk-fv">
    <div class="kk-fv__inner">

      <div class="kk-fv__text">
        <h1 class="kk-fv__title">
          思春期の子育てが<br>
          <em>苦しい</em>お母さんへ
        </h1>
        <p class="kk-fv__subtitle">
          「どうしてうちの子だけ…」<br>
          その悩み、ひとりで抱えないでください。<br>
          私は、あなたの味方です。
        </p>
        <p class="kk-fv__note">＼1分で登録完了／</p>
        <a href="【メルマガ登録URL】" class="kk-btn kk-btn--primary kk-btn--large">
          ✉ 今すぐ無料動画を受け取る &rsaquo;
        </a>
      </div>

      <div class="kk-fv__image">
        <!-- ▼ WordPress メディアライブラリから差し替えてください -->
        <img
          src="【プロフィール写真URL】"
          alt="思春期の子育て専門家 桃木亜子"
          class="kk-fv__photo"
        >
      </div>

    </div>
  </section>


  <!-- =====================================================
       信頼セクション
  ===================================================== -->
  <section class="kk-trust">
    <div class="kk-trust__inner">

      <div class="kk-trust__body">
        <h2 class="kk-trust__title">
          24年間、子育てに追い詰められた<br>
          お母さんを支えてきた。<br>
          <em>だから確信がある。</em>
        </h2>
        <p class="kk-trust__text">
          お母さんが変われば、子どもは必ず変わります。<br>
          そのことを、私は何よりも確信しています。<br>
          あなたの子育てが、笑顔に変わる未来を一緒に作りましょう。
        </p>
      </div>

    </div>
  </section>


  <!-- =====================================================
       お客様の声
  ===================================================== -->
  <section class="kk-testimonials">
    <div class="kk-testimonials__inner">

      <h2 class="kk-section-title">お客様の声</h2>

      <div class="kk-testimonials__grid">

        <div class="kk-card">
          <h3 class="kk-card__headline">子どもとの関係が驚くほど楽になりました</h3>
          <p class="kk-card__body">
            思春期の子どもとの毎日が辛くて、涙が止まらない日もありました。先生の言葉をきっかけに、子どもとの関係が驚くほど変わりました。
          </p>
          <p class="kk-card__name">中学2年生のママ（42歳）</p>
        </div>

        <div class="kk-card">
          <h3 class="kk-card__headline">自分を責める気持ちがなくなりました</h3>
          <p class="kk-card__body">
            「私の育て方が悪いんだ…」と自分を責めてばかりでした。今では、子どもを信じて見守れるようになりました。
          </p>
          <p class="kk-card__name">高校1年生のママ（45歳）</p>
        </div>

        <div class="kk-card">
          <h3 class="kk-card__headline">家庭の雰囲気が明るくなりました</h3>
          <p class="kk-card__body">
            ピリピリした空気がなくなり、笑顔で会話できる時間が増えました。本当に感謝しています。
          </p>
          <p class="kk-card__name">中学3年生のママ（48歳）</p>
        </div>

      </div>

      <p class="kk-disclaimer">
        ※個人の感想であり、効果を保証するものではありません。
      </p>

    </div>
  </section>


  <!-- =====================================================
       代表紹介
  ===================================================== -->
  <section class="kk-profile">
    <div class="kk-profile__inner">

      <div class="kk-profile__image">
        <!-- ▼ 代表写真 WordPress メディアから差し替え可 -->
        <img
          src="【代表写真URL】"
          alt="思春期の子育て専門家 桃木亜子"
          class="kk-profile__photo"
        >
      </div>

      <div class="kk-profile__text">
        <p class="kk-profile__greeting">はじめまして、</p>
        <h2 class="kk-profile__title">
          思春期の子育て専門家<br>
          <strong>桃木亜子</strong>です
        </h2>
        <p class="kk-profile__body">
          私自身、子育てに悩み、苦しみ、どうしていいかわからない時期がありました。その経験から、同じように苦しむお母さんの力になりたいと思い、24年間にわたり、思春期の子育て支援を続けています。どんな辛い状況でも、必ず変われます。あなたの未来を、心を込めてサポートします。
        </p>
        <a href="/profile/" class="kk-btn kk-btn--outline">
          想いを読む &rarr;
        </a>
      </div>

    </div>
  </section>


  <!-- =====================================================
       メルマガCTA
  ===================================================== -->
  <section class="kk-cta">
    <div class="kk-cta__inner">

      <div class="kk-cta__text">
        <p class="kk-cta__label">── 期間限定 ──</p>
        <h2 class="kk-cta__title">
          子どもへの対応に悩むお母さんへ<br>
          <em>無料動画プレゼント</em>
        </h2>
        <ul class="kk-cta__list">
          <li>子どもとの関わり方のコツ</li>
          <li>イライラが減る考え方</li>
          <li>親子関係が変わる魔法の言葉</li>
        </ul>
        <a href="【メルマガ登録URL】" class="kk-btn kk-btn--primary kk-btn--large">
          ✉ 今すぐ無料動画を受け取る &rsaquo;
        </a>
        <p class="kk-cta__note">登録は1分で完了します</p>
      </div>

      <div class="kk-cta__image">
        <!-- ▼ イメージ写真 WordPress メディアから差し替え可 -->
        <img src="【CTAイメージ写真URL】" alt="" class="kk-cta__photo">
      </div>

    </div>
  </section>

</main>

<?php get_footer(); ?>
