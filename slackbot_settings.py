import os

# botアカウントのトークンを指定
API_TOKEN = os.environ.get('SLACK_TOKEN_MAKE_ME_SHOWWIN')

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
HOW_TO_USE = """
わたしにメンションを飛ばしながら画像をアップロードするんだ！
"""
DEFAULT_REPLY = HOW_TO_USE

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']
