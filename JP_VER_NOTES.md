# 日本語版についての詳細 (v0.2)

## OSWorld（原語版）のバージョンについて

OSWorld-JP-v0.2は、[2025-10-17 時点の OSWorld（原語版）](https://github.com/xlang-ai/OSWorld/tree/9f97535ef99337da2518b903ec621f7e11e657b3)を起点として開発されています。この時点までに原語版に実装されていた機能は、基本的に利用可能です。

## タスクセットについて

- v0.2 で選定された 100 タスクは、`evaluation_eaxmples/test_J_all.json` に記載されています。これらのタスクは、原語版の 437 タスクから、カテゴリ間の比率が保たれるように無作為に選出されています。
- 日本語化の方針は以下です
    - リソースファイル（タスクで使用する課題ファイル・模範解答ファイル等）
        - テキストファイル・Office文書ファイルは、原則としてそれらの中身をすべて翻訳対象とする
        - 翻訳にあたっては、instruction の内容と整合するように留意する
        - 「ダミー役」の（=順調にタスクを遂行している間には一度も閲覧されることがない）ファイル・スライド・ページ・シートは翻訳対象外とする
        - ソースコードについては、コメントのみ翻訳対象とする。ただしソースの内容を理解する必要が全くないタスクでは、コメントも翻訳不要とする
        - 画像・動画ファイルについては、画像内のテキストの内容がタスクに直接関係し、しかも情報を視覚的に読み取るのに英語スキルが必要である場合にのみ翻訳対象とする。ただし画像・動画のテキストだけを日本語に翻訳しようとすると画像・動画が不細工（不自然）になるようなケースでは、タスクの趣意を損なわないように「日本語の別の画像・動画（自然なもの）」を用意する
        - 音声ファイルは翻訳対象外とする
        - ファイル名はほとんどの場合英語であるが、それ自体の意味を汲み取る必要のあるタスクでない限りは、翻訳不要とする
    - タスクで使用するWebページ（chrome カテゴリおよび multi_apps カテゴリの一部）
        - 「日本語UIのページ」が公式に用意されている場合は、そちらに差し替える。用意されていない場合は、タスクの業界・要求される操作内容・必要となる知識がなるべく類似した、日本のWebサイトに差し替える
    - 上記の修正内容に追従するように、採点基準のロジックも個別に修正する

- v0.2 で選定されたすべてのタスクについて、妥当性検証を実施済です（実施時期: 2025-10-27 〜 2025-12-24）。妥当性検証の方針は以下です
    - 「日本語環境VMイメージ」上で人間がタスクを遂行し、違和感なく遂行完了できることを検証する。以下のチェック項目を少なくとも含める:
        - 自然な方法で正しく操作を実施した場合に「正答」と判定されること
        - JSONファイルを確認して採点ロジックを理解した上で、それに明らかなバグがないこと
        - 採点ロジックと「インストラクション」が整合していること
            - よくあるパターン: インストラクションが和訳されているが、採点ロジック側の和訳（特定文字列の存在チェックでの、チェックされる文字列など）が漏れており、不整合となっている
                - 両者を整合させる必要がある
            - よくあるパターン: インストラクションで特定の方法を強制しているにもかかわらず、採点ロジックではその方法の強制をチェックできていない
                - この場合、採点ロジックを修正する（そのチェックを含めるように）、またはインストラクション側を修正する（その方法を強制しないように）必要がある
        - 何も操作を実施しなかった場合に「誤答」と判定されること（それが採点ロジックから明らかである場合には、実際に実施せずともOK）
    - 作業タスクの選定方法
        - OSWorld（原語版）のVerified版で生存しているタスクの中からランダムに選定する。タスクが偏らないように配慮する

## 仮想環境について

すべての評価は、仮想マシンの内部で実施されます。OSWorld（原語版）では様々な仮想マシンイメージが提供されています。一部のみ、日本語化を完了しています。

| プロバイダー | OS | アーキテクチャ | イメージ | 日本語化済イメージ |
|---|---|---|---|---|
| AWS | Ubuntu | x86 | [`ami-0d23263edb96951d8`](https://console.aws.amazon.com/ec2/home?region=us-east-1#ImageDetails:imageId=ami-0d23263edb96951d8) (us-east-1) | [`ami-0c4fe60b5531d188f`](https://console.aws.amazon.com/ec2/home?region=us-east-1#ImageDetails:imageId=ami-0c4fe60b5531d188f) |
| AWS | Ubuntu | x86 | [`ami-06850864d18fad836`](https://console.aws.amazon.com/ec2/home?region=ap-east-1#ImageDetails:imageId=ami-06850864d18fad836) (ap-east-1) | 未対応 |
| VMware | Ubuntu | ARM | [Ubuntu-arm.zip](https://huggingface.co/datasets/xlangai/ubuntu_osworld/resolve/main/Ubuntu-arm.zip) | 未対応 |
| VMware | Ubuntu | x86 | [Ubuntu-x86.zip](https://huggingface.co/datasets/xlangai/ubuntu_osworld/resolve/main/Ubuntu-x86.zip) | 未対応 |
| VMware | Windows | x86 | [Windows-x86.zip](https://huggingface.co/datasets/xlangai/windows_osworld/resolve/main/Windows-x86.zip) | 未対応 |
| Docker | Ubuntu | x86 | [Ubuntu.qcow2.zip](https://huggingface.co/datasets/xlangai/ubuntu_osworld/resolve/main/Ubuntu.qcow2.zip) | [Ubuntu_JA.qcow.zip](https://huggingface.co/datasets/karakuri-ai/ubuntu_osworld/resolve/main/Ubuntu_JA.qcow2.zip) |
| Docker | Windows | x86 | [Windows-10-x64.qcow2.zip](https://huggingface.co/datasets/xlangai/windows_osworld/resolve/main/Windows-10-x64.qcow2.zip) | 未対応 |
| VirtualBox | Ubuntu | x86 | [Ubuntu.zip](https://huggingface.co/datasets/xlangai/ubuntu_x86_virtualbox/resolve/main/Ubuntu.zip) | 未対応 |
| VirtualBox | Ubuntu | ARM | 未提供 | - |

イメージの日本語化は、以下の手順により行われています。上記で「未対応」となっているイメージを日本語化したい場合、以下の手順に準拠して実施してください。

### 仮想環境イメージ日本語化手順

※ 随所でパスワードを要求された場合は `password` と入力してください。

1. オリジナル版の仮想マシンを起動する。VMware または VirtualBox の場合は、`init_state` スナップショットを復元する
2. デスクトップ画面右上 → `Settings` → `Region & Language` と進み、`Manage Installed Languages` ボタンをクリック
3. `The Language support is not installed completely` というダイアログが表示された場合は、`Install` を選択。インストール完了まで待つ
4. `Install / Remove Languages...` ボタンをクリックし、 Japanese のチェックボックスをオンにして `Apply` ボタンをクリック。インストール完了まで待つ
5. `Language for menus and windows:` のリストボックス内の「日本語」を、ドラッグ&ドロップでリストの一番上に並ぶように移動したのちに、`Apply System-Wide` ボタンをクリック 
6. `Regional Formats` のタブに移動して、 `Display numbers, dates and currncy amounts in the usual format for:` の選択を「日本語」に変更し、`Apply System-Wide` ボタンをクリック
7. デスクトップ画面右上 → `Power Off / Log Out` → `Restart...` → `Restart` と進み、仮想マシンの再起動を実施
8. 再起動後、「標準フォルダーの名前を現在の言語に合わせて更新しますか？」と表示された場合は、「名前を更新する」を選択
9. Chrome (一部環境では代わりに Chromium) ブラウザを起動し、UIが日本語になっていることを確認したのち、閉じる
    - 次に起動するときのウィンドウ位置を変更したくないため、アプリのウィンドウを動かすことなく閉じてください
    - ウェブページを閲覧することも避けてください。「閲覧履歴」が汚れてしまいます
10. Thunderbird を起動し、UIが日本語になっていることを確認したのち、閉じる（アプリのウィンドウを動かさずに閉じること）
11. VSCode を起動し、Japanese Language Pack をインストールしたのちにアプリを再起動し、UIが日本語になっていることを確認したのち、閉じる（アプリのウィンドウを動かさずに閉じること）
12. 同様に、VLC, LibreOffice 3種類, GIMP, ファイルエクスプローラを順に起動し、UIが日本語になっていることを確認したのち、閉じる（アプリのウィンドウを動かさずに閉じること）
    - ファイルを開くことは避けてください。「最近開いたファイル」が汚れてしまいます
13. 「端末」を起動し、 `sudo apt install xclip xsel` を実行
    - `pyperclip.copy(...)` を実行可能とするために実施します
    - 端末のコマンドヒストリーが汚れてしまいますが、オリジナル版でも汚れているので、不問とします
    - `xclip` だけでも `pyperclip.copy()` できるようになりますが、subprocess.run 上で実行された際にタイムアウトする問題([REF](https://github.com/asweigart/pyperclip/issues/116))を解消するために `xsel` もインストールしてください
14. デスクトップで右クリックして「画面解像度の設定」を選択し、画面解像度が 1920 x 1080 となっていることを確認します。それ以外になっている場合は、左記設定に変更してください
    - これが誤った設定のままの場合、多くのエージェントがクリック位置を正しく出力できず、評価結果が本来よりも著しく悪化します
15. デスクトップ画面右上 → `Power Off / Log Out` → `Restart...` → `Restart` と進み、仮想マシンの再起動を実施
    - デスクトップで右クリックしてからの「端末で開く」がなぜか機能しなかったのが再起動後は機能するようになったため、実施しています
