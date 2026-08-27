"""A small, self-contained proposal website.

Run with:  python3 main.py
Then visit: http://localhost:8000
"""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import webbrowser


ROOT = Path(__file__).resolve().parent


PAGE = r'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#25172b">
  <title>Наша маленькая история</title>
  <style>
    :root { --ink:#fff8f4; --rose:#ff7597; --peach:#ffbd93; --violet:#5b365f; --night:#201625; }
    * { box-sizing:border-box; }
    html { scroll-behavior:smooth; }
    body { margin:0; color:var(--ink); background:var(--night); font-family: Georgia, 'Times New Roman', serif; overflow:hidden; }
    body::before { content:''; position:fixed; inset:0; z-index:-2; background:radial-gradient(circle at 14% 8%, #703d62 0, transparent 25rem), radial-gradient(circle at 88% 28%, #b55d63 0, transparent 25rem), linear-gradient(145deg,#221427,#372035 48%,#1f1724); }
    .stars { position:fixed; inset:0; z-index:0; pointer-events:none; opacity:.5; background-image:radial-gradient(#fff 1px,transparent 1.4px); background-size:44px 44px; mask-image:linear-gradient(#000,transparent); }
    .scene-bg { position:fixed; inset:0; z-index:-1; overflow:hidden; background:#211525; }
    .scene-bg::after { content:''; position:absolute; inset:0; background:linear-gradient(115deg,#140a20d9 0%,#2b163a88 45%,#160c22d6 100%),radial-gradient(circle at 18% 18%,#ff9ab844,transparent 36%),radial-gradient(circle at 80% 78%,#8bd5ff33,transparent 40%); mix-blend-mode:multiply; }
    .scene-bg img { width:100%; height:100%; object-fit:cover; filter:blur(17px) saturate(1.15) brightness(.86); opacity:.37; transform:scale(1.12); transition:opacity .8s ease,transform 8s ease,filter .8s ease; }
    .scene-bg img.shift { opacity:.5; transform:scale(1.2); }
    .progress { position:fixed; inset:0 auto auto 0; height:4px; width:0; z-index:30; background:linear-gradient(90deg,var(--rose),var(--peach)); box-shadow:0 0 12px var(--rose); transition:width .45s ease; }
    .welcome { position:fixed; inset:0; z-index:1000; display:grid; place-items:center; padding:22px; background:radial-gradient(circle at 50% 35%,#754267,#1d1423 65%); opacity:1; visibility:visible; transition:opacity .8s ease,visibility .8s; }
    .welcome.open { opacity:0; visibility:hidden; pointer-events:none; }
    .letter { width:min(510px,100%); padding:52px 30px; text-align:center; background:#fff4ec; color:#4b2638; box-shadow:0 25px 70px #09040bb0; border-radius:5px; transform:rotate(-1deg); }
    .letter .seal { display:block; font-size:44px; margin-bottom:15px; }
    .letter h2 { font-size:clamp(35px,7vw,56px); margin:0 0 16px; }
    .letter p { font-size:18px; line-height:1.55; margin:0 0 25px; }
    .letter button { color:#fff7f2; background:#873c59; box-shadow:none; }
    header { min-height:100vh; display:grid; place-items:center; padding:32px 20px; text-align:center; }
    .hero { max-width:780px; animation:appear 1.3s ease both; }
    .eyebrow { color:var(--peach); text-transform:uppercase; letter-spacing:.24em; font:600 11px/1.4 Arial,sans-serif; }
    h1 { font-size:clamp(48px,10vw,108px); line-height:.9; margin:17px 0 24px; font-weight:400; text-shadow:0 8px 28px #130b18; }
    h1 em { color:#ff9eb6; font-style:italic; }
    .lead { font-size:clamp(18px,2.5vw,24px); line-height:1.55; max-width:570px; margin:0 auto 35px; color:#ffece4; }
    .scroll { display:inline-flex; gap:10px; align-items:center; color:#ffd1bd; text-decoration:none; font:600 12px Arial,sans-serif; letter-spacing:.1em; text-transform:uppercase; }
    .scroll span { font-size:24px; animation:bounce 1.6s infinite; }
    main { width:min(1060px,calc(100% - 36px)); margin:auto; }
    section { margin:0; }
    .page { display:none; min-height:100vh; align-content:center; padding:80px 0 105px; animation:appear .65s ease both; }
    .page.active { display:grid; }
    .chapter { grid-template-columns:1fr 1fr; gap:clamp(24px,6vw,76px); align-items:center; }
    .chapter:nth-child(even) .words { order:2; }
    .photo { position:relative; margin:0; }
    .photo img { display:block; width:100%; max-height:650px; object-fit:cover; border-radius:5px; box-shadow:0 20px 55px #0c0710aa; }
    .photo img, .gallery img { cursor:zoom-in; }
    .photo::after { content:''; position:absolute; inset:12px -12px -12px 12px; border:1px solid #ffb3a180; border-radius:5px; z-index:-1; }
    .tag { color:var(--peach); font:700 11px Arial,sans-serif; letter-spacing:.18em; text-transform:uppercase; }
    h2 { font-weight:400; font-size:clamp(36px,5vw,59px); line-height:1.03; margin:14px 0 20px; }
    .words { padding:clamp(22px,4vw,46px); border:1px solid #ffc5b92e; border-radius:8px; background:#1e1127a8; backdrop-filter:blur(10px); box-shadow:0 18px 50px #09040b55; }
    .words p { color:#f8ded9; font-size:19px; line-height:1.65; margin:0 0 15px; }
    .quote { border-left:2px solid var(--rose); padding:12px 0 12px 20px; color:#ffc4c9 !important; font-style:italic; }
    .memory { padding:17px 0 0; }
    .memory button { padding:11px 17px; font-size:12px; background:#fff1eb; }
    .memory-text { display:none; margin-top:15px !important; padding:15px; border-radius:4px; background:#ffffff12; color:#ffd3c4 !important; }
    .memory-text.show { display:block; animation:appear .45s ease both; }
    .name-game { position:relative; overflow:hidden; margin-top:22px; padding:50px 20px 20px; border:1px solid #ffc5b966; border-radius:10px; background:linear-gradient(145deg,#ffffff18,#ff91b90b),#1b1025aa; box-shadow:inset 0 1px #fff4ec2e,0 16px 35px #09040b55; }
    .name-game::before { content:'ПРОВЕРКА ПАМЯТИ  •  01'; position:absolute; top:0; left:0; right:0; padding:11px 16px; border-bottom:1px solid #ffc5b944; color:#ffc5b9; background:#ffffff0b; font:700 10px Arial,sans-serif; letter-spacing:.14em; }
    .name-game::after { content:'?'; position:absolute; top:28px; right:16px; color:#ff9eb655; font:italic 50px Georgia,serif; pointer-events:none; }
    .name-game-question { margin:0 0 12px !important; color:#ffece4 !important; font-size:20px !important; }
    .name-game-question + .name-game-question { color:#ffc990 !important; font-size:14px !important; font-family:Arial,sans-serif; letter-spacing:.06em; text-transform:uppercase; }
    .name-options { display:flex; flex-wrap:wrap; gap:10px; }
    .name-options button { flex:1; min-width:120px; margin:0; padding:13px 16px; border-radius:8px; background:#ffffff16; color:#ffece4; border:1px solid #ffc5b944; box-shadow:none; }
    .name-options button:hover { background:#ffc990; color:#38182a; transform:translateY(-3px) rotate(-1deg); }
    .name-options button.correct { background:#91d8ad; color:#183928; border-color:#b9f1ca; }
    .name-options button.wrong { background:#d87d89; color:#401b28; border-color:#ffb0b7; }
    .name-game-status { min-height:25px; margin:14px 0 0 !important; color:#ffd4c5 !important; font-size:16px !important; }
    .portrait-wrap { width:min(560px,100%); margin:auto; text-align:center; }
    .portrait-frame { position:relative; width:min(390px,100%); margin:0 auto 28px; padding:10px; background:#fff4ec; box-shadow:0 24px 60px #08030caa; transform:rotate(-2deg); }
    .portrait-frame img { display:block; width:100%; aspect-ratio:4/5; object-fit:cover; filter:blur(22px) brightness(.72); transition:filter 1.1s ease,transform 1.1s ease; cursor:pointer; }
    .portrait-frame.revealed img { filter:blur(0) brightness(1); transform:scale(1.02); }
    .portrait-frame::after { content:'♡'; position:absolute; inset:0; display:grid; place-items:center; color:#fff; font-size:58px; text-shadow:0 4px 18px #000; pointer-events:none; opacity:1; transition:opacity .5s; }
    .portrait-frame.revealed::after { opacity:0; }
    .portrait-wrap h2 { margin-bottom:12px; }
    .portrait-wrap p { color:#f8ded9; font-size:19px; line-height:1.55; }
    .countdown-card { width:min(720px,100%); margin:auto; padding:clamp(28px,5vw,58px); text-align:center; border:1px solid #ffc5b94d; border-radius:10px; background:#1e1127b8; backdrop-filter:blur(12px); box-shadow:0 25px 60px #09040b66; }
    .countdown-card h2 { margin:12px 0 10px; }
    .countdown-card p { color:#f8ded9; font-size:19px; }
    .countdown-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin:30px auto 0; }
    .countdown-unit { padding:14px 8px; border:1px solid #ffc5b940; border-radius:6px; background:#ffffff12; }
    .countdown-unit strong { display:block; color:#fff5ed; font-size:clamp(25px,5vw,43px); font-weight:400; }
    .countdown-unit span { color:#ffc5b9; font:10px Arial,sans-serif; letter-spacing:.1em; text-transform:uppercase; }
    .quiz-wrap { width:min(760px,100%); margin:auto; }
    .quiz-card { padding:clamp(24px,5vw,52px); border:1px solid #ffc5b94d; border-radius:10px; background:#fff1ed0d; box-shadow:0 20px 50px #0c071055; }
    .quiz-card h2 { margin-top:10px; }
    .quiz-number { color:var(--peach); font:700 12px Arial,sans-serif; letter-spacing:.17em; text-transform:uppercase; }
    .answers { display:grid; gap:12px; margin-top:28px; }
    .answer-option { width:100%; margin:0; text-align:left; color:#ffece4; background:#ffffff12; border:1px solid #ffc5b935; box-shadow:none; }
    .answer-option:hover { color:#38182a; background:#ffc990; }
    .answer-option.correct { background:#91d8ad; border-color:#b9f1ca; color:#183928; }
    .answer-option.wrong { background:#d87d89; border-color:#ffb0b7; color:#401b28; }
    .answer-option:disabled { cursor:default; opacity:.78; transform:none; }
    .quiz-status { min-height:28px; margin:18px 0 0; color:#ffd4c5; font-size:18px; }
    .quiz-next { display:none; margin:18px 0 0; }
    .quiz-next.show { display:inline-block; }
    .quiz-complete { display:none; text-align:center; animation:appear .6s ease both; }
    .quiz-complete.show { display:block; }
    .quiz-complete h2 { margin-bottom:16px; }
    .quiz-complete p { color:#f8ded9; font-size:20px; }
    .break { padding:60px 20px; text-align:center; background:#fff1ed0f; border:1px solid #ffc5b935; border-radius:10px; }
    .break h2 { margin-bottom:10px; }
    .music-title { font-size:clamp(20px,4vw,31px); letter-spacing:.16em; }
    .music-subtitle { font-size:clamp(27px,4vw,41px); }
    .break p { color:#f8ded9; font-size:18px; }
    video { width:min(720px,100%); display:block; margin:30px auto 0; border-radius:6px; box-shadow:0 22px 50px #0d0710b8; background:#111; }
    .gallery { display:grid; grid-template-columns:1.2fr .8fr; gap:20px; }
    .gallery figure { margin:0; overflow:hidden; border-radius:5px; min-height:250px; }
    .gallery figure:first-child { grid-row:span 2; }
    .gallery img { width:100%; height:100%; min-height:250px; object-fit:cover; display:block; transition:transform .55s ease; }
    .gallery figure:hover img { transform:scale(1.045); }
    .final { min-height:78vh; place-items:center; text-align:center; position:relative; padding:50px 16px; }
    .final-box { max-width:850px; }
    .ring { font-size:70px; display:block; margin-bottom:18px; filter:drop-shadow(0 10px 12px #0c0710); }
    .final-box.celebrate .ring { animation:ringReveal 1.4s cubic-bezier(.17,.89,.32,1.28) both; }
    .question { font-size:clamp(44px,8vw,94px); line-height:.97; margin:12px 0 30px; font-weight:400; }
    button { border:0; border-radius:999px; cursor:pointer; padding:17px 30px; margin:5px; color:#38182a; background:linear-gradient(110deg,#ffb5bd,#ffc990); font:700 15px Arial,sans-serif; box-shadow:0 10px 25px #12091488; transition:transform .2s, box-shadow .2s; }
    button:hover { transform:translateY(-3px); box-shadow:0 14px 30px #120914b8; }
    #yes { background:linear-gradient(110deg,#ff7597,#ffca91); }
    #maybe { position:relative; transition:transform .28s cubic-bezier(.2,.9,.3,1.3),background .2s; }
    #answer { min-height:31px; color:#ffdbb9; font-size:20px; margin:20px 0 0; }
    .lightbox { position:fixed; inset:0; z-index:40; display:none; place-items:center; padding:25px; background:#09050bdc; cursor:zoom-out; }
    .lightbox.show { display:grid; animation:appear .25s ease both; }
    .lightbox img { max-width:100%; max-height:90vh; border-radius:5px; box-shadow:0 20px 70px #000; }
    .lightbox span { position:fixed; top:18px; right:24px; color:#fff; font:26px Arial,sans-serif; }
    .tap-hint { position:fixed; z-index:20; bottom:22px; left:50%; transform:translateX(-50%); color:#ffe1cf99; font:11px Arial,sans-serif; letter-spacing:.12em; text-transform:uppercase; pointer-events:none; transition:opacity .4s; }
    .memory-map { position:fixed; z-index:21; top:20px; right:24px; display:flex; gap:4px; padding:6px; border:1px solid #ffffff35; border-radius:999px; background:#251526c7; backdrop-filter:blur(12px); }
    .memory-map button { width:10px; min-width:10px; height:10px; padding:0; margin:0; border:1px solid #ffe6d788; border-radius:50%; color:transparent; background:#ffe6d744; box-shadow:none; font-size:0; transition:transform .25s,background .25s,border-color .25s; }
    .memory-map button:hover { background:#fff1e8; border-color:#fff1e8; transform:scale(1.3); }
    .memory-map button.active { background:var(--peach); border-color:var(--peach); transform:scale(1.55); }
    .heart { position:fixed; pointer-events:none; z-index:10; font-size:24px; animation:float 2.2s ease-out forwards; }
    .fireworks { position:fixed; inset:0; z-index:12; width:100%; height:100%; pointer-events:none; }
    @keyframes appear { from { opacity:0; transform:translateY(22px); } to { opacity:1; transform:none; } }
    @keyframes bounce { 50% { transform:translateY(6px); } }
    @keyframes float { to { opacity:0; transform:translate(var(--x),-110vh) rotate(300deg); } }
    @keyframes ringReveal { 0% { transform:scale(.2) rotate(-30deg); opacity:0; } 55% { transform:scale(1.25) rotate(12deg); opacity:1; } 100% { transform:scale(1) rotate(0); filter:drop-shadow(0 0 28px #ffadbd); } }
    @media (max-width:720px) { .page { padding:52px 0 100px; overflow-y:auto; align-content:start; } .chapter { grid-template-columns:1fr; gap:28px; } .chapter:nth-child(even) .words { order:initial; } .photo { margin:0 10px 0 0; } .gallery { grid-template-columns:1fr 1fr; gap:10px; } .gallery figure:first-child { grid-column:span 2; grid-row:auto; height:330px; } .break { padding:35px 14px; } .tap-hint { bottom:15px; } .memory-map { top:13px; right:13px; gap:3px; } .memory-map button { min-width:24px; width:24px; height:24px; padding:0; font-size:9px; } .countdown-grid { gap:6px; } .countdown-unit { padding:10px 4px; } .portrait-frame { width:min(290px,100%); } }
  </style>
</head>
<body>
  <div class="stars"></div><div class="scene-bg"><img id="scene-image" src="first.jpg" alt=""></div><div class="progress" id="progress"></div>
  <div class="welcome" id="welcome"><div class="letter"><span class="seal">💌</span><div class="tag">Личное письмо для тебя</div><h2>У меня есть для тебя одна история</h2><p>Улыбнись и открой, когда будешь готова.</p><button id="open-story" type="button">Открыть письмо ♡</button></div></div>
  <main id="story">
    <section class="page active" data-page data-bg="first.jpg">
      <header>
        <div class="hero"><div class="eyebrow">для самой прекрасной девушки</div><h1>Наша история,<br><em>которая началась онлайн</em></h1><p class="lead">Я собрал несколько наших моментов. Потому что некоторые истории слишком красивые, чтобы оставлять их только в чате.</p><button class="next-page" type="button">Начать историю ↓</button></div>
      </header>
    </section>
    <section class="page" data-page data-bg="herpicture.jpg" id="portrait-page">
      <div class="portrait-wrap"><div class="portrait-frame" id="portrait-frame"><img src="herpicture.jpg" alt="Твоя любимая улыбка"></div><h2>Есть кое-что, что я хочу тебе показать</h2><p>Нажми на кнопку — и увидишь мою любимую улыбку.</p><button id="reveal-portrait" type="button">Нажми, чтобы увидеть мою любимую улыбку ♡</button></div>
    </section>
    <section class="page" data-page data-bg="first.jpg">
      <div class="countdown-card"><div class="tag">Наша дата — 14 мая</div><h2>До следующего 14 мая</h2><p>Мы разговариваем с тобой с 14 мая — смеёмся, спорим и каждый день становимся ближе.</p><p id="countdown-intro">Каждый день приближает нас к ещё одной годовщине нашей встречи.</p><div class="countdown-grid"><div class="countdown-unit"><strong id="days">—</strong><span>дней</span></div><div class="countdown-unit"><strong id="hours">—</strong><span>часов</span></div><div class="countdown-unit"><strong id="minutes">—</strong><span>минут</span></div><div class="countdown-unit"><strong id="seconds">—</strong><span>секунд</span></div></div></div>
    </section>
    <section class="page chapter" data-page data-bg="first.jpg">
      <figure class="photo"><img src="first.jpg" alt="Наше первое знакомство"></figure>
      <div class="words"><h2>HelloTalk</h2><p>Всё началось с простого «create a vr». Кто бы мог подумать, что приложение для языков подарит мне мой любимый разговор на свете?</p><p class="quote">Ты — мой самый удачный перевод с «случайности» на «судьбу».</p><div class="name-game"><p class="name-game-question">Секунду… а почему ты столько времени была Марией? 🤨</p><p class="name-game-question">Кто должен объясниться?</p><div class="name-options"><button type="button" data-answer="Я">Я</button><button type="button" data-answer="HelloTalk">HelloTalk</button></div><p class="name-game-status" id="name-game-status" aria-live="polite"></p></div></div>
    </section>
    <section class="page chapter" data-page data-bg="insta.jpg">
      <figure class="photo"><img src="insta.jpg" alt="Наши переписки"></figure>
      <div class="words"><h2>Наша первая переписка в Instagram</h2><p>Потом были бесконечные переписки, улыбки у экрана и те самые маленькие моменты, из которых неожиданно собирается что-то большое.</p><p>И да, я всё ещё считаю, что твои сообщения работают лучше кофе.</p><div class="memory"><button type="button" data-memory="Официально: ты виновата в том, что я проверяю телефон на работе с очень счастливым лицом.">Нажми для улыбки</button><p class="memory-text"></p></div></div>
    </section>
    <section class="page chapter" data-page data-bg="roblox.jpg">
      <figure class="photo"><img src="roblox.jpg" alt="Наши приключения в Roblox"></figure>
      <div class="words"><h2>Мы и Roblox</h2><p>Наша первая игра в Roblox. Кто бы мог подумать, что даже в виртуальном мире я буду счастлив проводить время именно с тобой.</p><p class="quote">Даже когда я проигрывал, я всё равно чувствовал себя победителем, потому что играл вместе с тобой.</p></div>
    </section>
    <section class="page break" data-page data-bg="morning.jpg">
      <div class="tag music-title">Музыкальная пауза</div><h2 class="music-subtitle">Нажми ▶</h2><p>Твой пианино-саундтрек — моя любимая часть этой истории.</p>
      <video controls preload="metadata" playsinline><source src="IMG_1935.MP4" type="video/mp4">Твой браузер не поддерживает видео.</video>
    </section>
    <section class="page chapter" data-page data-bg="movie.jpg">
      <figure class="photo"><img src="movie.jpg" alt="Наш несостоявшийся киносеанс"></figure>
      <div class="words"><h2>Фильм, который мы так и не посмотрели</h2><p>Мы столько раз хотели посмотреть фильм вместе — и ни разу не смогли. Кажется, кино просто ревнует: у нас с тобой и без него слишком интересный сюжет.</p><p>Но когда встретимся, я обещаю: выберем фильм.</p></div>
    </section>
    <section class="page chapter" data-page data-bg="morning.jpg">
      <figure class="photo"><img src="morning.jpg" alt="Наше доброе утро"></figure>
      <div class="words"><h2>Доброе утро, Александра</h2><p>Однажды я позвонил тебе утром, когда ты спала. Ты сказала: «Не буди меня». A Теперь я каждое утро тебя бужу.</p><p class="quote">Прости за то утро. Но не прости меня за желание говорить тебе «доброе утро» всю жизнь.</p></div>
    </section>
    <section class="page" data-page id="quiz-page" data-bg="joke.jpg">
      <div class="quiz-wrap"><div class="quiz-card" id="quiz-card"><div class="quiz-number" id="quiz-number">Вопрос 1 из 3</div><h2 id="quiz-question">Какую игру мы впервые вместе играли в Roblox?</h2><div class="answers" id="answers"></div><div class="quiz-status" id="quiz-status" aria-live="polite"></div><button class="quiz-next" id="quiz-next" type="button">Следующий вопрос →</button></div><div class="quiz-complete" id="quiz-complete"><div class="tag">Ты всё вспомнила</div><h2>Тогда у меня остался только один вопрос…</h2><p>Он ждёт тебя на следующей странице.</p><button class="go-final" type="button">Открыть последний вопрос ♡</button></div></div>
    </section>
    <section class="page final" data-page data-bg="pic.jpg">
      <div class="final-box" id="final-box">
        <span class="ring">💍</span><div class="tag">Самый важный момент</div>
        <h2 class="question">Ты выйдешь за меня, когда мы встретимся?</h2>
        <button id="yes" type="button">Да, конечно! ♡</button><button id="maybe" type="button">Мне нужно обнять тебя и подумать</button>
        <div id="answer" aria-live="polite"></div>
      </div>
    </section>
  </main>
  <div class="tap-hint" id="tap-hint">Нажми, чтобы продолжить</div>
  <nav class="memory-map" id="memory-map" aria-label="Карта истории"></nav>
  <canvas class="fireworks" id="fireworks" aria-hidden="true"></canvas>
  <div class="lightbox" id="lightbox" role="dialog" aria-label="Увеличенная фотография"><span>×</span><img id="lightbox-image" alt=""></div>
  <script>
    const answer = document.getElementById('answer');
    const pages=[...document.querySelectorAll('[data-page]')]; let current=0;
    const sceneImage=document.getElementById('scene-image'), map=document.getElementById('memory-map');
    const pageNames=['Начало','Улыбка','14 мая','HelloTalk','Переписка','Roblox','Музыка','Кино','Утро','Викторина','Финал'];
    pages.forEach((page,index)=>{ const link=document.createElement('button'); link.type='button'; link.title=pageNames[index]||`Экран ${index+1}`; link.setAttribute('aria-label',link.title); link.onclick=()=>showPage(index); map.appendChild(link); });
    function showPage(index){ current=Math.max(0,Math.min(index,pages.length-1)); pages.forEach((page,i)=>page.classList.toggle('active',i===current)); document.getElementById('tap-hint').style.opacity=current===pages.length-1?'0':'1'; document.getElementById('progress').style.width=((current+1)/pages.length*100)+'%'; const bg=pages[current].dataset.bg; if(bg){ sceneImage.src=bg; sceneImage.style.filter=`blur(17px) saturate(1.15) brightness(.86) hue-rotate(${[0,18,-24,12,42,-18,70,120,-45,28,165][current]}deg)`; sceneImage.classList.remove('shift'); requestAnimationFrame(()=>sceneImage.classList.add('shift')); } [...map.children].forEach((link,i)=>link.classList.toggle('active',i===current)); }
    document.getElementById('open-story').onclick = () => { document.getElementById('welcome').classList.add('open'); showPage(0); };
    document.querySelectorAll('.next-page').forEach(button=>button.onclick=()=>showPage(current+1));
    document.getElementById('reveal-portrait').onclick = () => { const frame=document.getElementById('portrait-frame'); frame.classList.toggle('revealed'); document.getElementById('reveal-portrait').textContent=frame.classList.contains('revealed')?'Спрятать улыбку':'Нажми, чтобы увидеть мою любимую улыбку ♡'; };
    document.querySelectorAll('[data-answer]').forEach(button=>button.onclick=()=>{ const correct=button.dataset.answer==='Я'; const status=document.getElementById('name-game-status'); document.querySelectorAll('[data-answer]').forEach(option=>option.classList.remove('correct','wrong')); button.classList.add(correct?'correct':'wrong'); status.textContent=correct?'Так и думал. Ладно, Александра — теперь без секретов.':'Попробуй ещё раз.'; });
    function updateCountdown(){ const now=new Date(); let target=new Date(now.getFullYear(),4,14,0,0,0); if(target<=now) target=new Date(now.getFullYear()+1,4,14,0,0,0); const total=Math.max(0,target-now); document.getElementById('days').textContent=Math.floor(total/86400000); document.getElementById('hours').textContent=String(Math.floor(total/3600000)%24).padStart(2,'0'); document.getElementById('minutes').textContent=String(Math.floor(total/60000)%60).padStart(2,'0'); document.getElementById('seconds').textContent=String(Math.floor(total/1000)%60).padStart(2,'0'); document.getElementById('countdown-intro').textContent=`Следующая наша дата — ${target.toLocaleDateString('ru-RU',{day:'numeric',month:'long',year:'numeric'})}.` ; }
    updateCountdown(); setInterval(updateCountdown,1000);
    document.getElementById('yes').onclick = () => { answer.textContent = 'Я буду ждать этого дня. Я люблю тебя. ♡'; document.getElementById('yes').textContent='Ура! Это наше «да» ♡'; document.getElementById('final-box').classList.add('celebrate'); launchFireworks(); for(let i=0;i<80;i++) setTimeout(heart, i*35); };
    const maybeButton=document.getElementById('maybe'); let escapeCount=0;
    function runAway(event){ if(event.cancelable) event.preventDefault(); if(event.stopPropagation) event.stopPropagation(); escapeCount++; const rangeX=Math.min(135,innerWidth*.22), rangeY=Math.min(95,innerHeight*.12); const x=(Math.random()*2-1)*rangeX, y=(Math.random()*2-1)*rangeY; maybeButton.style.transform=`translate(${x}px,${y}px)`; maybeButton.textContent=escapeCount>3?'Поймай меня сначала ♡':'Мне нужно обнять тебя и подумать'; }
    maybeButton.addEventListener('pointerenter',event=>{ if(event.pointerType==='mouse') runAway(event); });
    maybeButton.addEventListener('pointerdown',runAway);
    maybeButton.onclick = event => { event.preventDefault(); answer.textContent = 'Но обнимать тебя я планирую очень долго. ♡'; for(let i=0;i<20;i++) setTimeout(heart, i*70); };
    function heart(){ const h=document.createElement('span'); h.className='heart'; h.textContent=['♥','♡','✦'][Math.floor(Math.random()*3)]; h.style.left=(15+Math.random()*70)+'vw'; h.style.bottom='-30px'; h.style.setProperty('--x', (Math.random()*180-90)+'px'); h.style.color=['#ff7296','#ffd19b','#fff2e8'][Math.floor(Math.random()*3)]; document.body.appendChild(h); setTimeout(()=>h.remove(),2300); }
    document.querySelectorAll('[data-memory]').forEach(button => button.onclick = () => { const text=button.nextElementSibling; text.textContent=button.dataset.memory; text.classList.toggle('show'); button.textContent=text.classList.contains('show') ? 'Спрятать секрет' : 'Открыть ещё раз'; });
    const lightbox=document.getElementById('lightbox'), lightboxImage=document.getElementById('lightbox-image');
    document.querySelectorAll('.photo img,.gallery img').forEach(image => image.onclick = () => { lightboxImage.src=image.src; lightboxImage.alt=image.alt; lightbox.classList.add('show'); });
    lightbox.onclick=()=>lightbox.classList.remove('show');
    addEventListener('keydown', event => { if(event.key==='Escape') lightbox.classList.remove('show'); if(event.key==='ArrowRight') showPage(current+1); if(event.key==='ArrowLeft') showPage(current-1); });
    const quiz=[
      { question:'Какую игру мы впервые вместе играли в Roblox?', options:['Murderers vs Sheriffs Duels','Guess My Number','Blind Timer'], correct:0, right:'Точно! Ты помнишь наше первое приключение в Roblox ♡', wrong:'Почти! Вспомни нашу самую первую игру…' },
      { question:'Кто первым начинает спорить?', options:['Я','Ты'], correct:0, right:'Вот именно. Но я всё равно первым иду мириться ♡', wrong:'Хм… кажется, ты знаешь этот ответ лучше меня 😄' },
      { question:'Когда мы посмотрим фильм вместе?', options:['Никогда','Как только ты выберешь фильм'], correct:1, right:'Договорились! Выбирай фильм — я уже приготовил место рядом с собой ♡', wrong:'Неверно. Всё зависит от одного очень важного выбора…' }
    ];
    let quizIndex=0, quizLocked=false;
    function renderQuiz(){ const item=quiz[quizIndex]; document.getElementById('quiz-number').textContent=`Вопрос ${quizIndex+1} из ${quiz.length}`; document.getElementById('quiz-question').textContent=item.question; document.getElementById('quiz-status').textContent=''; const list=document.getElementById('answers'); list.innerHTML=''; document.getElementById('quiz-next').classList.remove('show'); quizLocked=false; item.options.forEach((option,index)=>{ const button=document.createElement('button'); button.className='answer-option'; button.type='button'; button.textContent=`${index+1}. ${option}`; button.onclick=()=>chooseAnswer(button,index); list.appendChild(button); }); }
    function chooseAnswer(button,index){ if(quizLocked)return; quizLocked=true; const item=quiz[quizIndex]; document.querySelectorAll('.answer-option').forEach((option,i)=>{option.disabled=true; if(i===item.correct) option.classList.add('correct');}); const status=document.getElementById('quiz-status'); if(index===item.correct){ button.classList.add('correct'); status.textContent=item.right; if(quizIndex<quiz.length-1) document.getElementById('quiz-next').classList.add('show'); else setTimeout(()=>{document.getElementById('quiz-card').style.display='none'; document.getElementById('quiz-complete').classList.add('show');},650); } else { button.classList.add('wrong'); status.textContent=item.wrong; document.querySelectorAll('.answer-option').forEach(option=>option.disabled=false); quizLocked=false; } }
    document.getElementById('quiz-next').onclick=()=>{ quizIndex++; renderQuiz(); };
    document.querySelector('.go-final').onclick=()=>showPage(current+1);
    renderQuiz();
    pages.forEach(page=>page.onclick=event=>{ if(page.id==='quiz-page' || event.target.closest('button,video,img')) return; showPage(current+1); });
    addEventListener('pointermove',event=>{ if(event.pointerType==='touch') return; const x=(event.clientX/innerWidth-.5)*10, y=(event.clientY/innerHeight-.5)*6; sceneImage.style.transform=`translate(${x}px,${y}px) scale(1.16)`; },{passive:true});
    addEventListener('pointerleave',()=>{ sceneImage.style.transform='scale(1.1)'; });
    const fireworks=document.getElementById('fireworks'), fireCtx=fireworks.getContext('2d'); let sparks=[];
    function resizeFireworks(){ const dpr=Math.min(devicePixelRatio||1,2); fireworks.width=innerWidth*dpr; fireworks.height=innerHeight*dpr; fireCtx.setTransform(dpr,0,0,dpr,0,0); }
    addEventListener('resize',resizeFireworks); resizeFireworks();
    function launchFireworks(){ sparks=[]; const colors=['#ff7597','#ffc990','#fff2e8','#b7e4ff']; for(let burst=0;burst<5;burst++){ const cx=innerWidth*(.18+Math.random()*.64), cy=innerHeight*(.18+Math.random()*.48); for(let i=0;i<42;i++){ const angle=Math.PI*2*i/42, speed=2+Math.random()*4; sparks.push({x:cx,y:cy,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,life:1,color:colors[Math.floor(Math.random()*colors.length)],size:1+Math.random()*2}); } } const started=performance.now(); function draw(now){ fireCtx.clearRect(0,0,innerWidth,innerHeight); sparks.forEach(s=>{s.x+=s.vx;s.y+=s.vy;s.vy+=.045;s.vx*=.99;s.life-=.012; fireCtx.globalAlpha=Math.max(0,s.life); fireCtx.fillStyle=s.color; fireCtx.beginPath(); fireCtx.arc(s.x,s.y,s.size,0,Math.PI*2); fireCtx.fill();}); fireCtx.globalAlpha=1; if(now-started<4200) requestAnimationFrame(draw); else fireCtx.clearRect(0,0,innerWidth,innerHeight); } requestAnimationFrame(draw); }
    showPage(0);
  </script>
</body>
</html>'''


class ProposalHandler(SimpleHTTPRequestHandler):
    """Serve the proposal page at / and the media files beside this script."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            content = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        super().do_GET()


if __name__ == "__main__":
    # Hosting platforms provide PORT; locally we keep the friendly port 8000.
    port = int(os.environ.get("PORT", "8000"))
    host = "0.0.0.0" if "PORT" in os.environ else "127.0.0.1"
    local_url = f"http://localhost:{port}"
    print(f"\nYour proposal website is ready at {local_url}\n")
    if "PORT" not in os.environ:
        webbrowser.open(local_url)
    try:
        ThreadingHTTPServer((host, port), ProposalHandler).serve_forever()
    except KeyboardInterrupt:
        print("\nWebsite stopped. ❤️")
