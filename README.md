# kosen-test
テストデータ(input.txt)は後日公開

## 使い方
1. test.pyを置き換える
1. main.pyを実行

## フォルダ構成
- out
- test
    - input.txt
- main.py
- README.md
- test.py

## test.py
- test関数
    - input
        - input_text:str 問題文
    - output
        - str 回答
    - 例
        ```python
        def test(input_text:str) -> str:
            return "Hello, " + input_text 
        ```
    
## 問題
- encoding: utf-8
- 英数字記号: 半角
- ひらがなカタカナ漢字： 全角
- ファイル: test/input.txt
- 1行に1つの問題
- strip(前後の空白等の削除)のみ行い、test関数へ渡される