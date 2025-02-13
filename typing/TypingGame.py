import pyxel
import json
import os
from typehandler import Process  # ✅ 外部の `Process` クラスを使う

shifted = {
    'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 
    'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 
    'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z'
}

# ✅ **ワードリストを追加**
words = {
    'IMT':'いちのせちゃんまじてんし',
     'ドイツ生まれ永遠の十三歳':'どいつうまれえいえんのじゅうさんさい',
     'む一みんロル教室':'むいちみんろるきょうしつ',
     'むーみんカスタムまだかな':'むーみんかすたむまだかな',
     'おきつね工房':'おきつねこうぼう',
     'きっぽちゃんとマダミスしたい':'きっぽちゃんとまだみすしたい',
     '菓子工房異国屋':'かしこうぼういこくや',
     '推し夫婦ぽっぽあぬるlove':'おしふうふぽっぽあぬるlove',
     'てぃる教':'てぃるきょう',
     '推しに推される世界線':'おしにおされるせかいせん',
     'やきにく博士だね':'やきにくはかせだね',
     'やきにくチャンネル':'やきにくちゃんねる',
     'ぽにー痩せろ':'ぽにーやせろ',
     'カービンの達人ぽにー':'かーびんのたつじんぽにー',
     'べるめも最高':'べるめもさいこう',
     'べるちゃんと行く飛鳥クルーズ':'べるちゃんといくあすかくるーず',
     'おちゅきみコロナ':'おちゅきみころな',
     'お刺身野菜cvつきみ':'おさしみやさいcvつきみ',
     'お邪魔さんは練習にもならない':'おじゃまさんはれんしゅうにもならない',
     'お邪魔さんのお茶増します':'おじゃまさんのおちゃまします',
     'ぬるのおまちゅり':'ぬるのおまちゅり',
     '迷探偵ぬるまゅ':'めいたんていぬるまゅ',
     'もは恋最強':'もはこいさいきょう',
     'あずくんスノボ上手い':'あずくんすのぼうまい',
     'ティアスリービジネスパートナー':'てぃあすりーびじねすぱーとなー',
     'とおるん':'へんじん',
     'ごみくず野郎':'ごみくずやろう',
     'ごみくず実況秀逸':'ごみくずじっきょうしゅういつ',
     'ことさん結婚おめでとう':'ことさんけっこんおめでとう',
     '最後のキンタリズムこと':'さいごのきんたりずむこと',
     'じぃじさんhappybirthday':'じぃじさんhappybirthday',
     '宇宙忍者しろくま':'うちゅうにんじゃしろくま',
     'sena配信せえすなせえ':'senaはいしんせえすなせえ',
     'senaさんはお尻からウルトを出す':'senaさんはおしりからうるとをだす',
     'ゆりやんの二の腕もちもち':'ゆりやんのにのうでもちもち',
     'ユリやんカスタムまだかな':'ゆりやんのかすたむまだかな',
     'まめたのお尻もちもち':'まめたのおしりもちもち',
     'ダイエッターまめた':'だいえったーまめた',
     '宗教団体キンタリズム':'しゅうきょうだんたいきんたりずむ',
     'リアルスタイル':'りあるすたいる',
     'コーチングされ中しゅぷりーむ':'こーちんぐされちゅうしゅぷりーむ',
     'メイド服のしいな':'めいどふくのしいな',
     '記念日耐久パズル男しいな':'きねんびたいきゅうぱずるおとこしいな',
     'ゆうゆうさんはイケメン':'ゆうゆうさんはいけめん',
     '優しさの権化ゆうゆう':'やさしさのごんげゆうゆう',
     'イケボのるーまる':'いけぼのるーまる',
     '飲酒のるーまる':'いんしゅのるーまる',
     'ビートマニアじじい':'びーとまにあじじい',
     'キンバリーマスターじじい':'きんばりーますたーじじい',
     'もりさんちの子供になりたい':'もりさんちのこどもになりたい',
     '星のやに行ったらもりさんに報告':'ほしのやにいったらもりさんにほうこく',
     'みんなのもちもちなのね':'みんなのもちもちなのね',
     'もちもちなのねは持ち帰り':'もちもちなのねはもちかえり',
     'うひニキと絶対遊ぶぞ':'うひにきとぜったいあそぶぞ',
     '縦読みのuhihi':'たてよみのuhihi',
     '土の家を壊すなはとぷ':'つちのいえをこわすなはとぷ',
     'はとぷのお料理教室':'はとぷのおりょうりきょうしつ',
     'ぽよの霊圧が':'ぽよのれいあつが',
     'ぽよにラーメンを食べさせる':'ぽよにらーめんをたべさせる',
     'ぶろさん国家試験合格めでたい':'ぶろさんこっかしけんごうかくめでたい',
     'コーチングし中ぶろっこりーじゃむ':'こーちんぐしちゅうぶろっこりーじゃむ',
     'ミモさん広島へゆく':'みもさんひろしまへゆく',
     '仕事前コメントのmimo':'しごとまえこめんとのmimo',
     '双子のパパぱんだっち':'ふたごのぱぱぱんだっち',
     '意外とイケボぱんだっち':'いがいといけぼぱんだっち',
     'いとうちゃんの眼鏡になりたい':'いとうちゃんのめがねになりたい',
     'いとうちゃんのATMになりたい':'いとうちゃんのatmになりたい',
     'ネイルのプロえりー':'ねいるのぷろえりー',
     '英会話えりーちゃんと頑張ってます':'えいかいわえりーちゃんとがんばってます',
     '山口県のかずやさん':'やまぐちけんのかずやさん',
     'かずやさんちの猫可愛い':'かずやさんちのねこかわいい',
     'ひかべるカスタム':'ひかべるかすたむ',
     'サイゼリアのひかさん':'さいぜりあのひかさん',
     'ロシア出張中のエスク':'ろしあしゅっちょうちゅうのえすく',
     'みんなのパパエスク':'みんなのぱぱえすく',
     'ゼロキルのハリボー':'ぜろきるのはりぼー',
     'ストロクで初心者狩りハリボー':'すとろくでしょしんしゃがりはりぼー',
     '鳴かず飛ばずれんちん':'なかずとばずれんちん',
     'れんちん痩せろ':'れんちんやせろ',
     'リバウンド上等魔装青年':'りばうんどじょうとうまそうせいねん',
     '魔装さんとなんかゲームしよ':'まそうさんとなんかげーむしよ',
     'おしゃべりすぎ子ぶた':'おしゃべりすぎこぶた',
     'たくさんスキンくれる子ぶた':'たくさんすきんくれるこぶた',
     'かががじぇ':'かががじぇ',
     'ホワイトだいすきあきちゃん':'ほわいとだいすきあきちゃん',
     'たぬの歌を聴けっ':'たぬのうたをきけっ',
     '連続視聴回数記録更新中おゆき':'れんぞくしちょうかいすうきろくこうしんちゅうおゆき',
     '魔法少女名探偵ぴまちゃん':'まほうしょうじょめいたんていぴまちゃん',
     'ありけり系女子ぴーまん':'ありけりけいじょしぴーまん',
     'メンヘラ三銃士さや':'めんへらさんじゅうしさや',
     '四十回スノボに行く女さや':'よんじゅっかいすのぼにいくおんなさや',
     '葉っぱの男しゃりあ':'はっぱのおとこしゃりあ',
     'れおん会に呼ばれないしゃりあ':'れおんかいによばれないしゃりあ',
     'プロゲーマーりゅうきまん代表':'ぷろげーまーりゅうきまんだいひょう',
     '二十万投げた男りゅうき':'にじゅうまんなげたおとこりゅうき',
     'いつのまにか関東にようこそばな':'いつのまにかかんとうにようこそばな',
     'めちゃくちゃ理数系ぽいバナ':'めちゃくちゃりすうけいぽいばな'
}

SCORE_FILE = "scores.json"

font = pyxel.Font("k8x12.bdf")
process = Process(words)  # ✅ **ワードリストを Process に渡す**


class TypingGame:
    def __init__(self):
        pyxel.init(160, 120, fps=50)
        self.state = "input_name"
        self.player_name = ""
        self.start_time = 0
        self.score = 0
        self.rankings = self.load_scores()
        self.create_sounds()
        pyxel.run(self.update, self.draw)  # ✅ `draw()` を正しく設定

    def create_sounds(self):
        """✅ サウンド設定（非推奨コード修正）"""
        pyxel.sounds[0] = pyxel.Sound()
        pyxel.sounds[0].set("c2", "t", "6", "vffn", 5)  # 成功音

        pyxel.sounds[1] = pyxel.Sound()
        pyxel.sounds[1].set("g1", "t", "6", "vffn", 5)  # ミス音

    def load_scores(self):
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_scores(self):
        previous_score = self.rankings.get(self.player_name, 0)  # ✅ 前回のスコアを取得
        if self.score > previous_score:
            self.rankings[self.player_name] = self.score  # ✅ 新しいスコアが前回より高ければ更新

        with open(SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.rankings, f, ensure_ascii=False, indent=4)


    def update(self):
        if self.state == "input_name":
            self.update_name_input()
        elif self.state == "game":
            self.update_game()
        elif self.state == "game_over":
            self.update_game_over()

    def update_name_input(self):
        for key in pyxel.input_keys:
            if pyxel.btnp(key):
                if key == pyxel.KEY_RETURN and self.player_name:
                    self.state = "game"
                    self.start_time = pyxel.frame_count
                elif key == pyxel.KEY_BACKSPACE and self.player_name:
                    self.player_name = self.player_name[:-1]
                elif len(self.player_name) < 10 and 32 <= key <= 126:
                    self.player_name += chr(key)

    def update_game(self):
        elapsed_time = (pyxel.frame_count - self.start_time) / 50
        if elapsed_time >= 60:
            self.state = "game_over"
            self.save_scores()
            return
        
        process.update_show_roman()

        for key in pyxel.input_keys:
            if key not in range(pyxel.KEY_UNKNOWN, pyxel.KEY_Z + 1):
                continue
            
            char = chr(key)
            if pyxel.btnp(pyxel.KEY_UNKNOWN):
                char = '\\'
            if pyxel.btn(pyxel.KEY_SHIFT):
                char = shifted.get(char, char)

            if process.main(char):
                self.score += 1
                pyxel.play(0, [0])  # ✅ 成功音の再生
            else:
                pyxel.play(1, [1])  # ✅ ミス音の再生

    def update_game_over(self):
        """✅ リザルト画面でEnterを押すと最初の画面に戻る"""
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.reset_game()

    def reset_game(self):
        """✅ ゲームをリセットして最初の画面に戻る"""
        self.state = "input_name"
        self.start_time = 0
        self.score = 0
        self.player_name = ""

        # ✅ `Process` のリセット処理（next_word() の代わりに `Process` を再初期化）
        global process
        process = Process(words)  # ✅ `Process` を完全に再初期化

    def draw(self):
        """✅ 画面を描画"""
        pyxel.cls(0)
        if self.state == "input_name":
            self.draw_name_input()
        elif self.state == "game":
            self.draw_game()
        elif self.state == "game_over":
            self.draw_game_over()

    def draw_name_input(self):
        """✅ 名前入力画面"""
        pyxel.text(40, 40, "名前を入力してください:", 7, font)
        pyxel.text(40, 60, self.player_name + "_", 10, font)
        pyxel.text(40, 80, "Enterでスタート", 6, font)

    def draw_game(self):
        pyxel.text(20, 40, process.show_roman, 13, font)
        pyxel.text(20, 50, process.input, 14, font)
        pyxel.text(20, 60, process.sentence if process.sentence else "", 7, font)
        pyxel.text(20, 80, f"Time Left: {60 - (pyxel.frame_count - self.start_time) // 50}", 10, font)
        pyxel.text(20, 90, f"Score: {self.score}", 10, font)

    def draw_game_over(self):
        pyxel.text(40, 30, "Game Over!", 8)  # ✅ ピンク
        pyxel.text(40, 45, f"Score: {self.score}", 7)  # ✅ 白
        pyxel.text(40, 60, "Ranking:", 7)  # ✅ 白

    # ✅ ランキング表示 (間隔を 8px に変更)
        sorted_rankings = sorted(self.rankings.items(), key=lambda x: x[1], reverse=True)
        for i, (player, score) in enumerate(sorted_rankings[:5]):
            pyxel.text(40, 70 + i * 8, f"{i+1}. {player}: {score}", 12)  # ✅ 青

    # ✅ 「Enterでリスタート」→「Press ENTER to Restart」に変更
        pyxel.text(40, 120, "Press ENTER to Restart", 10)  # ✅ 黄色


TypingGame()

