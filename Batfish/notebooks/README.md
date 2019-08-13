<h2>Batfishの環境準備</h2>
https://tekunabe.hatenablog.jp/entry/2018/10/26/batfish_pybatfish

<h2>主な使い方など</h2>
Batfish: https://www.batfish.org/

※snapshotとはshow running-configログの事



<p><h2>BatfishをAnsibleで使えるようにしてみた</h2></p>
※以下、pybatfishがインストールしてある事と、BatfishをDockerで動かしている状態での動作を検証済みです。


<p><モジュール化した目的></p>
Batfishの出力結果は、Jupyter Notebookでも十分見やすいです。しかし、テストからコンフィグ投入まで自動で一気通貫で
できるようにしたかったです。またテストツールをAnsibleで使えるようにしておくだけでも、定期的なテストをかけることが可能になります。

<p><ポイント説明></p>
csvファイルを作り、それを読み込ませるモジュールにしました。

<p>acl_test.csv</p>

```

test_id	src	dest	acl_name	node	application	intend_condition
-------	---------	-------------	---------	------------------	-----------	----------------
1	1.1.1.1		SPLIT-ACL	before_summary_asa	dns	permit
2	10.22.0.0	255.255.255.0	SPLIT-ACL	before_summary_asa	dns	permit
3	10.25.0.0	255.255.255.0	SPLIT-ACL	before_summary_asa	dns	permit
```

・csvの説明

1, 一行ごとにテストしたいパラメータを作成します。テストidはBatfishにテストの合否判定させた場合にどのテストが合格で
   どのテストが不合格なのかがわかるように入れています。

2, intend_conditionはdenyであるべきか、permitであるべきかを二択で設定するようにしています。
   ここに設定した値と、Batfishが出力する結果を照合し、一致していればテストは合格で、一致していなければ不合格とします。

動作した結果：
f:id::20190812225258p:plain

この場合、test_id1のテスト結果は不合格だったのでmoduleの実行結果はfailureとして扱っています。
from 1.1.1.1の通信をノード名'before_summary_asa'のアクセスリスト'SPLIT-ACL'でpermitされることが期待されているのですが
Batfishはdeny(通信拒否)を判断しているからです。


