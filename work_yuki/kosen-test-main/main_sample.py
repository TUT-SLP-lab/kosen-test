from test_gpt import test

#質問を書く
text = f"""
同一方向に進行しながら進路変更する場合の合図の時期は、その行為をする３０メートル手前に達したときである。
〇か×で答え、理由も答えよ
""" 

answer = test(text)
print("------------")
print(answer)