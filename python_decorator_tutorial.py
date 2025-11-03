"""
【完全解説】Pythonデコレーター入門 - 自作から組み込みまで

新人エンジニア向けに、デコレーターを1行ずつ丁寧に解説します。
"""

# =============================================================================
# 【第1章】デコレーターとは？
# =============================================================================

"""
デコレーター（Decorator）とは：
- 関数やクラスに「機能を追加する」ための仕組み
- @ マークを使って、既存の関数を「装飾（デコレート）」する
- 元の関数を変更せずに、新しい機能を追加できる

イメージ：
プレゼント（元の関数）にリボン（デコレーター）を付ける感じ
"""

# =============================================================================
# 【第2章】デコレーターなしの世界（before）
# =============================================================================

def say_hello():  # 普通の関数を定義
    """挨拶する関数"""  # docstring（関数の説明）
    print("こんにちは！")  # メッセージを表示


def say_goodbye():  # 別の関数を定義
    """お別れの挨拶をする関数"""
    print("さようなら！")  # メッセージを表示


# 実行してみる
print("=== デコレーターなし ===")  # 見出しを表示
say_hello()  # 関数を呼び出す → 「こんにちは！」と表示される
say_goodbye()  # 関数を呼び出す → 「さようなら！」と表示される

# 問題点：
# 各関数に「実行時間を測りたい」「ログを出力したい」などの
# 共通機能を追加するには、全ての関数を書き換える必要がある


# =============================================================================
# 【第3章】デコレーターの基本 - 簡単な例
# =============================================================================

def simple_decorator(func):  # デコレーター関数を定義（関数を引数として受け取る）
    """シンプルなデコレーター"""
    
    def wrapper():  # 内部関数（ラッパー）を定義
        # wrapperは「包む」という意味
        print("--- 関数の実行前 ---")  # 元の関数の前に実行される
        func()  # 元の関数を実行（funcには装飾された関数が入っている）
        print("--- 関数の実行後 ---")  # 元の関数の後に実行される
    
    return wrapper  # 内部関数を返す（これが重要！）
    # wrapper関数そのものを返すので、()は付けない


# デコレーターを使わない場合
def greet_without_decorator():  # 普通の関数
    print("Hello!")  # メッセージ表示


# デコレーターを手動で適用
greet_decorated = simple_decorator(greet_without_decorator)
# simple_decorator()の戻り値（wrapper関数）がgreet_decoratedに代入される

print("\n=== デコレーターを手動適用 ===")
greet_decorated()  # wrapper関数が実行される
# 実行順序：
# 1. "--- 関数の実行前 ---" が表示
# 2. 元のgreet_without_decorator()が実行 → "Hello!" が表示
# 3. "--- 関数の実行後 ---" が表示


# デコレーターを@記号で使う（推奨される書き方）
@simple_decorator  # この行が「デコレーターを適用」という意味
# これは greet = simple_decorator(greet) と同じ意味
def greet():  # 普通に関数を定義
    print("Hello with @decorator!")  # メッセージ表示


print("\n=== @記号でデコレーター適用 ===")
greet()  # 実行すると、simple_decoratorで包まれた状態で実行される


# =============================================================================
# 【第4章】引数を受け取るデコレーター
# =============================================================================

def decorator_with_args(func):  # 引数を持つ関数用のデコレーター
    """引数を受け取る関数に対応したデコレーター"""
    
    def wrapper(*args, **kwargs):  # *args と **kwargs で任意の引数を受け取る
        # *args: 位置引数（タプルとして受け取る）
        # **kwargs: キーワード引数（辞書として受け取る）
        
        print(f"引数: {args}, {kwargs}")  # 受け取った引数を表示
        result = func(*args, **kwargs)  # 元の関数に引数を渡して実行
        # 結果を変数に保存
        print(f"戻り値: {result}")  # 戻り値を表示
        return result  # 戻り値を返す（これを忘れると結果が返らない）
    
    return wrapper  # wrapper関数を返す


@decorator_with_args  # デコレーターを適用
def add(a, b):  # 2つの引数を受け取る関数
    """2つの数を足す"""
    return a + b  # 足し算の結果を返す


@decorator_with_args  # 同じデコレーターを別の関数にも適用できる
def multiply(x, y, z=1):  # 3つの引数（zはデフォルト値あり）
    """3つの数を掛ける"""
    return x * y * z  # 掛け算の結果を返す


print("\n=== 引数付き関数のデコレーター ===")
result1 = add(3, 5)  # 3 + 5 を計算
print(f"最終結果: {result1}")  # 8が表示される

result2 = multiply(2, 3, z=4)  # 2 * 3 * 4 を計算
print(f"最終結果: {result2}")  # 24が表示される


# =============================================================================
# 【第5章】実用的なデコレーター① - 実行時間測定
# =============================================================================

import time  # 時間測定用のモジュールをインポート


def measure_time(func):  # 実行時間を測定するデコレーター
    """関数の実行時間を測定するデコレーター"""
    
    def wrapper(*args, **kwargs):  # 任意の引数を受け取る
        start_time = time.time()  # 開始時刻を記録
        # time.time()は現在時刻を秒単位で返す
        
        result = func(*args, **kwargs)  # 元の関数を実行
        
        end_time = time.time()  # 終了時刻を記録
        elapsed_time = end_time - start_time  # 経過時間を計算（秒単位）
        
        # 結果を表示（小数点以下4桁まで）
        print(f"実行時間: {elapsed_time:.4f}秒")
        
        return result  # 元の関数の戻り値を返す
    
    return wrapper  # wrapper関数を返す


@measure_time  # 実行時間測定デコレーターを適用
def slow_function():  # 重い処理をシミュレート
    """時間がかかる処理"""
    print("処理中...")  # メッセージ表示
    time.sleep(2)  # 2秒間停止（重い処理を模擬）
    print("処理完了！")  # 完了メッセージ
    return "Done"  # 結果を返す


@measure_time  # 同じデコレーターを別の関数にも適用
def calculate_sum(n):  # 1からnまでの合計を計算
    """1からnまでの合計を計算"""
    total = sum(range(1, n + 1))  # 合計を計算
    # range(1, n+1)は1からnまでの数列を生成
    # sum()でその合計を計算
    return total  # 結果を返す


print("\n=== 実行時間測定デコレーター ===")
result = slow_function()  # 実行すると自動で時間が測定される
print(f"戻り値: {result}")  # "Done"が表示される

result = calculate_sum(1000000)  # 100万までの合計を計算
print(f"合計: {result}")  # 結果と実行時間が表示される


# =============================================================================
# 【第6章】実用的なデコレーター② - ログ出力
# =============================================================================

import functools  # デコレーター作成に便利な機能を提供するモジュール


def logger(func):  # ログ出力デコレーター
    """関数の呼び出しをログに記録するデコレーター"""
    
    @functools.wraps(func)  # 元の関数のメタ情報を保持する
    # これがないと、デコレートされた関数の名前やdocstringが失われる
    def wrapper(*args, **kwargs):  # 任意の引数を受け取る
        # 関数名と引数を表示
        print(f"[LOG] 関数 '{func.__name__}' を実行")
        # func.__name__は関数の名前を取得
        print(f"[LOG] 引数: args={args}, kwargs={kwargs}")
        
        try:  # エラーが起きるかもしれない処理
            result = func(*args, **kwargs)  # 元の関数を実行
            print(f"[LOG] 正常終了: 戻り値={result}")  # 成功メッセージ
            return result  # 結果を返す
        
        except Exception as e:  # エラーが発生した場合
            # Exception as eで、発生したエラーをeという変数に格納
            print(f"[LOG] エラー発生: {e}")  # エラー内容を表示
            raise  # エラーを再発生させる（呼び出し元にエラーを伝える）
    
    return wrapper  # wrapper関数を返す


@logger  # ログデコレーターを適用
def divide(a, b):  # 割り算をする関数
    """aをbで割る"""
    return a / b  # 割り算の結果を返す


print("\n=== ログ出力デコレーター ===")
result = divide(10, 2)  # 正常なケース
print(f"結果: {result}")  # 5.0が表示される

print("\n--- エラーケース ---")
try:  # エラーを捕捉するためのtry-except
    result = divide(10, 0)  # 0で割ろうとする（エラーが発生する）
except ZeroDivisionError:  # 0除算エラーを捕捉
    print("0で割ることはできません")  # エラーメッセージ


# =============================================================================
# 【第7章】パラメータ付きデコレーター
# =============================================================================

def repeat(times):  # パラメータを受け取るデコレーターの外側
    """関数を指定回数繰り返し実行するデコレーター
    
    Args:
        times (int): 繰り返し回数
    """
    
    def decorator(func):  # 実際のデコレーター部分
        # 3重の入れ子構造になる
        
        @functools.wraps(func)  # メタ情報を保持
        def wrapper(*args, **kwargs):  # ラッパー関数
            results = []  # 結果を保存するリスト
            
            for i in range(times):  # 指定回数だけ繰り返す
                print(f"--- {i + 1}回目 ---")  # 回数を表示
                result = func(*args, **kwargs)  # 関数を実行
                results.append(result)  # 結果をリストに追加
            
            return results  # 全ての結果をリストで返す
        
        return wrapper  # wrapper関数を返す
    
    return decorator  # decorator関数を返す
    # この構造により、@repeat(3)のように使える


@repeat(times=3)  # 3回繰り返すデコレーター
# これは repeat(3)(say_hello)() と同じ意味
def say_hello_repeat():  # 繰り返す関数
    """挨拶を繰り返す"""
    print("こんにちは！")  # メッセージ表示
    return "Hello"  # 戻り値


print("\n=== パラメータ付きデコレーター ===")
results = say_hello_repeat()  # 3回実行される
print(f"全ての戻り値: {results}")  # ['Hello', 'Hello', 'Hello']


# =============================================================================
# 【第8章】複数のデコレーターを組み合わせる
# =============================================================================

@measure_time  # 2番目に適用（外側）
@logger        # 1番目に適用（内側）
# デコレーターは下から順に適用される
# つまり、logger → measure_time の順番で処理される
def complex_calculation(x, y):  # 複雑な計算をする関数
    """複雑な計算をシミュレート"""
    time.sleep(1)  # 1秒待つ（重い処理を模擬）
    return x * y + x - y  # 計算結果を返す


print("\n=== 複数デコレーターの組み合わせ ===")
result = complex_calculation(10, 5)  # 実行
print(f"最終結果: {result}")  # 55が表示される

# 実行順序：
# 1. measure_timeのwrapper開始（時間測定開始）
# 2. loggerのwrapper開始（ログ出力開始）
# 3. 元の関数実行
# 4. loggerのwrapper終了（ログ出力終了）
# 5. measure_timeのwrapper終了（時間測定終了）


# =============================================================================
# 【第9章】組み込みデコレーター① - @property
# =============================================================================

class Person:  # Personクラスを定義
    """人物を表すクラス"""
    
    def __init__(self, name, age):  # 初期化メソッド
        """初期化
        
        Args:
            name (str): 名前
            age (int): 年齢
        """
        self._name = name  # アンダースコア付き（慣習的にprivate扱い）
        self._age = age    # 直接アクセスは推奨されない


    @property  # ゲッター（読み取り専用プロパティ）
    # このデコレーターにより、メソッドを属性のように扱える
    def name(self):  # メソッド名がプロパティ名になる
        """名前を取得"""
        print("[LOG] nameが参照されました")  # アクセスログ
        return self._name  # 内部の変数を返す
    
    
    @property  # 年齢のゲッター
    def age(self):  # 年齢を取得するメソッド
        """年齢を取得"""
        return self._age  # 内部の変数を返す
    
    
    @age.setter  # セッター（書き込み可能プロパティ）
    # @property でゲッターを定義した後に使える
    def age(self, value):  # 新しい値を受け取る
        """年齢を設定（バリデーション付き）"""
        if not isinstance(value, int):  # 整数でない場合
            raise TypeError("年齢は整数で指定してください")
        if value < 0:  # 負の値の場合
            raise ValueError("年齢は0以上である必要があります")
        
        print(f"[LOG] 年齢を {self._age} から {value} に変更")
        self._age = value  # 値を設定
    
    
    def introduce(self):  # 自己紹介メソッド
        """自己紹介する"""
        # self.nameやself.ageは@propertyで定義されたプロパティ
        print(f"私は{self.name}、{self.age}歳です")


print("\n=== @property デコレーター ===")
person = Person("太郎", 25)  # インスタンスを作成

# プロパティとして読み取り（()なしで呼び出せる）
print(person.name)  # "太郎"が表示される（メソッドだが括弧不要）
print(person.age)   # 25が表示される

# セッターで値を変更（代入のように書ける）
person.age = 26  # メソッドだが代入のように書ける
print(f"新しい年齢: {person.age}")  # 26が表示される

person.introduce()  # 自己紹介

# エラーケース
try:
    person.age = -5  # 負の値を設定しようとする
except ValueError as e:  # エラーを捕捉
    print(f"エラー: {e}")  # エラーメッセージ表示


# =============================================================================
# 【第10章】組み込みデコレーター② - @staticmethod と @classmethod
# =============================================================================

class Calculator:  # 計算機クラス
    """計算機能を提供するクラス"""
    
    # クラス変数（全インスタンスで共有）
    PI = 3.14159  # 円周率（定数）
    
    
    def __init__(self, name):  # 初期化メソッド
        """初期化
        
        Args:
            name (str): 計算機の名前
        """
        self.name = name  # インスタンス変数
    
    
    # 通常のインスタンスメソッド
    def instance_method(self, x):  # 第1引数はself（インスタンス自身）
        """インスタンスメソッドの例"""
        # selfを通じてインスタンス変数にアクセスできる
        return f"{self.name}: {x * 2}"
    
    
    @staticmethod  # 静的メソッド
    # インスタンスもクラスも必要としない、独立した関数のようなもの
    def add(a, b):  # selfもclsも不要
        """2つの数を足す（静的メソッド）
        
        インスタンスやクラス変数にアクセスしない、
        純粋な計算処理に使う。
        """
        return a + b  # 計算結果を返す
    
    
    @staticmethod  # 別の静的メソッド
    def multiply(a, b):  # 引数だけで完結する処理
        """2つの数を掛ける"""
        return a * b
    
    
    @classmethod  # クラスメソッド
    # 第1引数にクラス自身(cls)が渡される
    def circle_area(cls, radius):  # clsはクラス自身を指す
        """円の面積を計算（クラスメソッド）
        
        クラス変数（PI）にアクセスする必要がある場合に使う。
        """
        # cls.PIでクラス変数にアクセス
        return cls.PI * radius * radius
    
    
    @classmethod  # ファクトリーメソッド（インスタンス生成用）
    def create_scientific(cls):  # クラスメソッドでインスタンス生成
        """科学計算用の計算機を作成"""
        # cls()で自身のインスタンスを作成できる
        return cls("科学計算機")  # nameに"科学計算機"を渡してインスタンス作成


print("\n=== @staticmethod と @classmethod ===")

# 静的メソッドの呼び出し
# インスタンスを作らずに直接呼び出せる
result = Calculator.add(3, 5)  # クラス名.メソッド名
print(f"3 + 5 = {result}")  # 8が表示される

result = Calculator.multiply(4, 6)  # 同様に呼び出し
print(f"4 × 6 = {result}")  # 24が表示される

# クラスメソッドの呼び出し
area = Calculator.circle_area(10)  # 半径10の円の面積
print(f"円の面積: {area}")  # 314.159が表示される

# ファクトリーメソッドでインスタンス作成
calc = Calculator.create_scientific()  # クラスメソッドでインスタンス生成
print(f"作成した計算機: {calc.name}")  # "科学計算機"が表示される

# インスタンスメソッドの呼び出し
# インスタンスが必要
calc2 = Calculator("通常計算機")  # インスタンス作成
result = calc2.instance_method(5)  # インスタンス経由で呼び出し
print(result)  # "通常計算機: 10"が表示される


# =============================================================================
# 【第11章】実践例 - デコレーターの組み合わせ
# =============================================================================

def cache_result(func):  # キャッシュデコレーター
    """計算結果をキャッシュするデコレーター
    
    同じ引数での呼び出しは、前回の結果を返す。
    重い計算を高速化できる。
    """
    cache = {}  # キャッシュ用の辞書（クロージャとして保持される）
    
    @functools.wraps(func)  # メタ情報を保持
    def wrapper(*args):  # 引数を受け取る
        # 辞書のキーとして使うため、引数をタプルに変換
        if args in cache:  # キャッシュに存在する場合
            print(f"[CACHE] キャッシュから取得: {args}")
            return cache[args]  # キャッシュの値を返す
        
        # キャッシュに存在しない場合は計算
        print(f"[CALC] 新規計算: {args}")
        result = func(*args)  # 元の関数を実行
        cache[args] = result  # 結果をキャッシュに保存
        return result  # 結果を返す
    
    return wrapper


@cache_result  # キャッシュデコレーターを適用
@measure_time  # 実行時間測定デコレーターも適用
def fibonacci(n):  # フィボナッチ数列を計算
    """フィボナッチ数列のn番目を計算（再帰版）"""
    if n <= 1:  # 基底条件
        return n  # 0または1を返す
    # 再帰的に計算
    return fibonacci(n - 1) + fibonacci(n - 2)


print("\n=== デコレーター実践例：キャッシュ ===")
print("1回目の呼び出し:")
result = fibonacci(10)  # 10番目のフィボナッチ数
print(f"fibonacci(10) = {result}")

print("\n2回目の呼び出し（同じ引数）:")
result = fibonacci(10)  # 同じ引数で再度呼び出し
print(f"fibonacci(10) = {result}")  # キャッシュから即座に取得


# =============================================================================
# 【第12章】まとめ - デコレーターの使い分け
# =============================================================================

"""
■ 自作デコレーターを使う場面：
1. 実行時間測定 (@measure_time)
   - パフォーマンス測定が必要な時

2. ログ出力 (@logger)
   - デバッグやトレーサビリティが必要な時

3. キャッシュ (@cache_result)
   - 重い計算を高速化したい時

4. リトライ処理
   - ネットワーク処理など、失敗時に再試行したい時

5. 権限チェック
   - Webアプリケーションで、認証・認可が必要な時

■ 組み込みデコレーターを使う場面：
1. @property
   - クラスの属性にアクセス制御を追加したい時
   - ゲッター/セッターを実装したい時

2. @staticmethod
   - クラスに関連するが、インスタンス変数を使わない処理

3. @classmethod
   - クラス変数を使う処理
   - ファクトリーメソッド（インスタンス生成）

■ デコレーターの設計原則：
1. 単一責任の原則
   - 1つのデコレーターは1つの機能だけを持つ

2. 透過性
   - デコレーターは元の関数の動作を変えない
   - 追加機能を提供するだけ

3. 再利用性
   - 様々な関数に適用できるように汎用的に作る

4. functools.wrapsを使う
   - 元の関数のメタ情報（名前、docstring等）を保持する
"""


# =============================================================================
# 実行：すべてのサンプルを試す
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🎉 すべてのデコレーターサンプルが完了しました！")
    print("=" * 60)
    
    print("\n【学んだこと】")
    print("✓ デコレーターの基本構造")
    print("✓ @記号の使い方")
    print("✓ 引数を持つデコレーター")
    print("✓ 実用的なデコレーター（時間測定、ログ、キャッシュ）")
    print("✓ パラメータ付きデコレーター")
    print("✓ 複数デコレーターの組み合わせ")
    print("✓ @property, @staticmethod, @classmethod")
    print("✓ 実践的な応用例")
    
    print("\n【次のステップ】")
    print("1. 自分でデコレーターを作ってみる")
    print("2. 既存のコードにデコレーターを適用してみる")
    print("3. Flaskなどのフレームワークでデコレーターを使う")
    print("4. より高度なデコレーター（クラスデコレーター）に挑戦")
