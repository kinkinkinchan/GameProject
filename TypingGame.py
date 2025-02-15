import pyxel
import json
import os
import random

# ✅ ローマ字入力の許容パターン
romaji_variants = {
    "chi": ["chi", "ti"],
    "cchi": ["cchi", "tti", "ltchi"],
    "shi": ["shi", "si"],
    "ji": ["ji", "zi"],
    "je": ["zile", "je"],
    "tsu": ["tsu", "tu"],
    "fu": ["fu", "hu"],
    "cha": ["tya", "cha"],
    "tya": ["tya", "cha"],
    "chu": ["tyu", "chu"],
    "tyu": ["tyu", "chu"],
    "cho": ["tyo", "cho", "ccho", "ttyo"],  # ✅ 追加
    "tyo": ["tyo", "cho", "ccho", "ttyo"],  # ✅ 追加
    "ccho": ["ccho", "ttyo", "cho", "tyo"],  # ✅ 追加
    "ttyo": ["ttyo", "ccho", "cho", "tyo"],  # ✅ 追加
    "sha": ["sha", "sya"],
    "shu": ["shu", "syu"],
    "sho": ["sho", "syo"],
    "ja": ["jya", "ja", "zya", "zilya"],
    "jya": ["jya", "ja", "zya", "zilya"],
    "ju": ["jyu", "ju", "zyu", "zilyu"],
    "jyu": ["jyu", "zyu"],  # ✅ 追加
    "zyu": ["zyu", "jyu"],  # ✅ 追加
    "jyo": ["jyo", "jo", "zyo", "zilyo"],
    "zyo": ["zyo", "jo", "jyo"],  # ✅ 追加
    "jo": ["jo", "zyo", "jyo"],  # ✅ 追加
    "jyo": ["jyo", "jo", "zyo"],  # ✅ 追加
    "chan": ["chan", "tyan"]  # ✅ tyan と chan を許容
}

shifted = {chr(i): chr(i).upper() for i in range(ord('a'), ord('z') + 1)}

words = {
    'IMT':'ichinosechanmajitenshi',
    'ドイツ生まれ永遠の十三歳':'doitsuumareeiennojyuusansai',
    'む一みんロル塾':'muichiminrorujuku',
    'むーみんカスタムまだかな':'mu-minkasutamumadakana',
    'おきつね工房':'okitsunekoubou',
    'きっぽちゃんとマダミスしたい':'kippochantomadamisshitai',
    '菓子工房異国屋':'kashikoubouikokuya',
    '推し夫婦ぽっぽあぬるlove':'oshifuufupoppoanurulove',
    'てぃる教':'telirukyou',
    '推しに推される世界線':'oshiniosareresekaisen',
    'やきにく博士だね':'yakinikuhakasedane',
    'やきにくチャンネル':'yakinikuchanneru',
    'ぽにー痩せろ':'poni-yasero',
    'カービンの達人ぽにー':'ka-binnnotatsujinponi-',
    'べるめも最高':'berumemosaikou',
    'べるちゃんと行く飛鳥クルーズ':'beruchantoikuasukakuru-zu',
    'おちゅきみコロナ':'ochukimikorona',
    'お刺身野菜cvつきみ':'osashimiyasaicvtsukimi',
    'お邪魔さんは練習にもならない':'ojamasanharensyuunimonaranai',
    'お邪魔さんのお茶増します':'ojamasannoochamashimasu',
    'ぬるのおまちゅり':'nurunoomatsuri',
    '迷探偵ぬるまゅ':'meitanteinurumayu',
    'もは恋最強':'mohakoisaikyou',
    'あずくんスノボ上手い':'azukunsunoboumai',
    'ティアスリービジネスパートナー':'tiasuri-bijinesupa-tona-',
    'とおるん':'toorun',
    'ごみくず野郎':'gomikuzuyarou',
    'ごみくず実況秀逸':'gomikuzujikkyoushuuitsu',
    'ことさん結婚おめでとう':'kotosankekkonomedetou',
    '最後のキンタリズムこと':'saigonokintarizumukoto',
    'じぃじさんhappybirthday':'jilijisanhappybirthday',
    '宇宙忍者しろくま':'uchuuninjashirokuma',
    'sena配信せえすなせえ':'senahaishinseesunasee',
    'senaはお尻からウルトを出す':'senahaoshirikaraurutoodasu',
    'ゆりやんの二の腕もちもち':'yuriyannnoninoudemochimochi',
    'ユリやんカスタムまだかな':'yuriyannkasutamumadakana',
    'まめたのお尻もちもち':'mametanooshirimochimochi',
    'ダイエッターまめた':'daietta-mameta',
    '宗教団体キンタリズム':'shuukyoudantaikintarizumu',
    'リアルスタイル':'riarusutairu',
    'コーチングされ中しゅぷりーむ':'ko-chingusarechuushupuri-mu',
    'メイド服のしいな':'meidofukunoshiina',
    '記念日耐久パズル男しいな':'kinenbitaikyuupazuruotokoshiina',
    'ゆうゆうさんはイケメン':'yuuyuusanhaikemen',
    '優しさの権化ゆうゆう':'yasashisanogongeyuuyuu',
    'イケボのるーまる':'ikebonoru-maru',
    '飲酒のるーまる':'inshunoru-maru',
    'ビートマニアじじい':'bi-tomaniajijii',
    'キンバリーマスターじじい':'kinbari-masuta-jijii',
    'もりさんちの子供になりたい':'morisanchinokodomoninaritai',
    '星のや行く時もりさんに報告':'hoshinoyaikutokimorisannihoukoku',
    'みんなのもちもちなのね':'minnanomochimochinanone',
    'もちもちなのねは持ち帰り':'mochimochinanonehamochikaeri',
    'うひニキと絶対遊ぶぞ':'uhinikitozettaiasubuzo',
    '縦読みのuhihi':'tateyominouhihi',
    '土の家を壊すなはとぷ':'tsuchinoiewokowasunahatopu',
    'はとぷのお料理教室':'hatopunooriyourikyoushitsu',
    'ぽよの霊圧が':'poyonoreiatsuga',
    'ぽよにラーメンを食べさせる':'poyonira-menwotabesaseru',
    'ぶろさん国家試験合格めでたい':'burosankokkashikengoukakumedetai',
    'コーチングし中ぶろっこりー':'ko-chingushichuuburokkori-',
    'ミモさん広島へゆく':'mimosannhirosimaheyuku',
    '仕事前コメントのmimo':'shigotomaekomentonomimo',
    '双子のパパぱんだっち':'futagonopapapandacchi',
    '意外とイケボぱんだっち':'igaitoikebopandacchi',
    'いとうちゃんの眼鏡になりたい':'itouchannomeganeninaritai',
    'いとうちゃんのATMになりたい':'itouchannoATMninaritai',
    'ネイルのプロえりー':'neirunopuroeri-',
    '英会話えりーと頑張ってます':'eikaiwaeri-toganbattemasu',
    '山口県のかずやさん':'yamaguchikennokazuyasan',
    'かずやさんちの猫可愛い':'kazuyasanchinonekokawaii',
    'ひかべるカスタム':'hikaberukasutamu',
    'サイゼリアのひかさん':'saizerianohikasan',
    'ロシア出張中のエスク':'roshiashucchouchuunoesuku',
    'みんなのパパエスク':'minnanopapaesuku',
    'ゼロキルのハリボー':'zerokirunoharibo-',
    'ストロクで初心者狩りハリボー':'sutorokudeshoshinshagariharibo-',
    '鳴かず飛ばずれんちん':'nakazutobazurenchin',
    'れんちん痩せろ':'renchinyasero',
    'リバウンド上等魔装青年':'ribaundojoutoumasouseinen',
    '魔装さんとなんかゲームしよ':'masousantonankage-mushiyo',
    'おしゃべりすぎ子ぶた':'oshaberisugikobuta',
    'たくさんスキンくれる子ぶた':'takusansukinkurerukobuta',
    'かががじぇ':'kagagaje',
    'ホワイトだいすきあきちゃん':'howaitodaisukiakichan',
    'たぬの歌を聴け':'tanunoutawokike',
    '連続視聴回数記録更新中おゆき':'renzokushichoukaisuukirokukoushinchuuoyuki',
    '魔法少女名探偵ぴまちゃん':'mahoushoujomeitanteipimachan',
    'ありけり系女子ぴーまん':'arikerikeijoshipi-man',
    'メンヘラ三銃士さや':'menherasanjuushisaya',
    'スノボのプロすぎるさや':'sunobonopurosugirusaya',
    '葉っぱの男しゃりあ':'happanootokosharia',
    'れおん会に呼ばれないしゃりあ':'reonkainiyobarenaisharia',
    'プロゲーマーりゅうきまん代表':'puroge-ma-ryuukimandaihyou',
    '二十万投げた男りゅうき':'nijyuumannagetaotokoryuuki',
    '関東にようこそばな':'kantouniyoukosobana',
    '理数系ぽいバナ':'risuukeipoibana'
}

SCORE_FILE = "scores.json"
TIME_LIMIT = 60  # ✅ 60秒 → 5秒 に変更
font = pyxel.Font("k8x12.bdf")


class TypingGame:
    def __init__(self):
        pyxel.init(160, 120, fps=50)
        self.state = "input_name"
        self.player_name = ""
        self.start_time = 0
        self.score = 0
        self.input_text = ""  # ユーザーの入力
        self.words_used = []  # 使用済みワードを記録
        self.current_word = ""
        self.show_roman = ""
        self.rankings = self.load_scores()
        self.create_sounds()
        self.next_word()  # 最初の単語を設定
        pyxel.run(self.update, self.draw)

    def create_sounds(self):
        """✅ サウンド設定"""
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
        previous_score = self.rankings.get(self.player_name, 0)
        if self.score > previous_score:
            self.rankings[self.player_name] = self.score  # ✅ 新しいスコアが前回より高ければ更新
        with open(SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.rankings, f, ensure_ascii=False, indent=4)

    def next_word(self):
        """✅ 一度出た単語はそのゲーム中に出ないようにする"""
        available_words = list(words.keys())
        if len(self.words_used) == len(available_words):
            self.words_used = []  # ✅ すべての単語が出たらリセット

        while True:
            word = random.choice(available_words)
            if word not in self.words_used:
                self.words_used.append(word)
                self.current_word = word
                self.show_roman = words[word]  # ✅ ローマ字見本をセット
                self.input_text = ""  # 入力をリセット
                break

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
                    self.start_time = pyxel.frame_count  # ✅ ゲーム開始時間を記録
                elif key == pyxel.KEY_BACKSPACE and self.player_name:
                    self.player_name = self.player_name[:-1]
                elif len(self.player_name) < 10 and 32 <= key <= 126:
                    self.player_name += chr(key)

    def update_game(self):
        elapsed_time = (pyxel.frame_count - self.start_time) // 50  # ✅ 経過時間を秒単位に変換
        if elapsed_time >= TIME_LIMIT:  # ✅ 5秒経過したらゲーム終了
            self.state = "game_over"
            self.save_scores()
            return

        for key in pyxel.input_keys:
            if key not in range(pyxel.KEY_UNKNOWN, pyxel.KEY_Z + 1):
                continue

            char = chr(key)
            if pyxel.btnp(pyxel.KEY_UNKNOWN):
                char = '\\'
            if pyxel.btn(pyxel.KEY_SHIFT):
                char = shifted.get(char, char)

            if pyxel.btnp(key):
                expected_chars = self.get_valid_next_inputs()
                if char in expected_chars:
                    self.input_text += char
                    self.score += 1
                    pyxel.play(0, [0])  # 成功音

                # ✅ 入力が完全一致したら次の単語へ
                if self.is_valid_input(self.input_text, self.show_roman):
                    self.next_word()


    def get_valid_next_inputs(self):
        """✅ 次に入力すべき文字を取得"""
        valid_inputs = self.expand_variants(self.show_roman)
        valid_chars = set()
        for variant in valid_inputs:
            if variant.startswith(self.input_text):
                next_index = len(self.input_text)
                if next_index < len(variant):
                    valid_chars.add(variant[next_index])
        return valid_chars


    def is_valid_input(self, input_text, target_text):
        """✅ ユーザーの入力が完全一致しているかチェック"""
        valid_inputs = self.expand_variants(target_text)
        return input_text in valid_inputs

    def expand_variants(self,text):
        """ ローマ字の代替表記を考慮してすべてのパターンを生成 """
        variations = {text}
        for key, variants in romaji_variants.items():
            new_variations = set()
            for variation in variations:
                if key in variation:
                    for variant in variants:
                        new_variations.add(variation.replace(key, variant))
            variations.update(new_variations)
        return variations  # ✅ 重複を排除



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
        self.words_used = []
        self.next_word()

    def draw(self):
        pyxel.cls(0)
        if self.state == "input_name":
            self.draw_name_input()
        elif self.state == "game":
            self.draw_game()
        elif self.state == "game_over":
            self.draw_game_over()

    def draw_name_input(self):
        pyxel.text(40, 40, "名前を入力してください:", 7, font)
        pyxel.text(40, 60, self.player_name + "_", 10, font)
        pyxel.text(40, 80, "Enterでスタート", 6, font)

    def draw_game(self):
        remaining_time = max(0, TIME_LIMIT - (pyxel.frame_count - self.start_time) // 50)  # ✅ 残り時間を表示
        pyxel.text(20, 50, f"Word: {self.current_word}", 13, font)
        pyxel.text(20, 60, f"Roman: {self.show_roman}", 10, font)
        pyxel.text(20, 70, f"Input: {self.input_text}", 14, font)
        pyxel.text(20, 90, f"Time Left: {remaining_time}", 10, font)
        pyxel.text(20, 100, f"Score: {self.score}", 10, font)

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