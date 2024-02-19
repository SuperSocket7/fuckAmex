# fuckAmex
うざい荒らしを殺害します

## 使い方
#### ユーザー一斉削除/凍結スクリプト(delete.py)
まずはdelete.pyのinstance変数を自分のインスタンスのドメインにして、<br>
token変数に自分のアカウントのトークンを入れる。<br>
`pip3 install requests` で必要なライブラリをインストール<br>
`python3 delete.py <mode>` で実行、deleteなら垢削除、suspendなら凍結って感じになります。<br>
プロンプトが表示されたら荒らしのユーザー名(`@unko`もしくは`@unko@everyone.net`)のフォーマットで入力する<br>
これを繰り返していけばどんどんアカウントが消えていきます。<br>
#### 全自動荒らしぶっ殺しマシン(main.py)
全自動で荒らし殺せないかなーと思って作ったやつ。<br>
websocketsがゴミすぎて途中で途切れるわそもそも検知しないわで諦めた。<br>

### 荒らし死ねよ
ちなみに荒らしの主犯は[こいつ](https://twitter.com/amex2189)<br>
うらむならこいつを恨め