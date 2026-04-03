# OSWorld-JP

言語を考慮した評価のための、日本語版コンピュータユースベンチマーク

## 📢 アップデート

- 2026-03-27: 本ベンチマークの **v0.2** を公開しました。
    - v0.1 は 437 のタスクからなるベンチマークでしたが、v0.2 ではタスク数を 100 に限定し、代わりに各タスクの妥当性検証（ベリフィケーション）を周到に行ったバージョンとなります
    - 以下の内容を含みます
        - [x] システム環境のローカライズ
        - [x] システムプロンプトの日本語化
        - [x] 原語版の 437 タスクから無作為に選出した 100 のタスクに関して、タスク内容にまで踏み込んだ日本語化（タスク関連ファイルの修正・タスクの読み替え等）
        - [x] 前記 100 タスクについて、**各タスクが実際に正答可能であること**、**採点基準が妥当であること**を人間が検証し、妥当でない点の個別修正
        - [x] OSWorld（原語版）側で開発された並列評価システム（評価時間を短縮可能）、およびその中で使用される AWS AMI イメージの日本語版
    - 補足
        - v0.1 は、オリジナルの OSWorld 437 問を日本語化したものでしたが、問題数が多く、ベンチマークとしての質を担保するのがいささか困難な分量でした。「量」を犠牲にして、有意義なベンチマークであるための最低限の「質」を担保するという趣旨のもと、v0.2 が開発されました。

- 2025-11-04: **本リポジトリにて現在公開中の v0.1 に多くの不具合が含まれていることが判明しました。今後、不具合の修正作業を実施予定です。v0.1 の使用は推奨せず、今後公開予定の v0.2 以降の使用を強く推奨します。**

- 2025-05-28: 本 GitHub にて、本ベンチマークを v0.1 として公開しました。以下の内容を反映済みです。
    - [x] システム環境のローカライズ
    - [x] システムプロンプトの日本語化
    - [x] 全てのタスクのプロンプトの日本語化
    - [x] 344/437 (=79%) のタスクに関して、タスク内容にまで踏み込んだ日本語化（タスク関連ファイルの修正・タスクの読み替え等）

- 2025-05-28: 本ベンチマークに関して、2025年度 人工知能学会全国大会 (JSAI2025) にて発表予定です。日時等は[こちら](https://confit.atlas.jp/guide/event/jsai2025/subject/3Win5-56/tables) をご参照ください。


## ✨ OSWorld-JP とは？

近年、大規模言語モデル(LLM)を搭載したエージェントは、GUI や CLI インターフェースを介したコンピュータ操作の自動化に広く応用されています。しかし、[OSWorld](https://os-world.github.io/) など既存のエージェント評価ベンチマークは英語環境向けに最適化されており、日本語環境でのエージェント評価には適していません。そこで本研究では、プロンプトの翻訳、システム環境のローカライズ、タスク関連ファイルの修正を行い、OSWorld の日本語版である OSWorld-JP を開発しました。

> **注意：** 本ベンチマークは今後も改善活動によりバージョンアップがなされていく予定です。また、インターネット上のウェブサイトの挙動に依存するタスクが一部含まれており、永続性が保証されません。そのため、評価結果を公表する際には、ベンチマークのバージョンおよび評価を実施した日付を明記することを推奨します。

## 💾 インストール
### VMware/VirtualBox（デスクトップ、ラップトップ、ベアメタルマシン）
仮想化されていないシステム（例：デスクトップ、ラップトップ、ベアメタルマシン）で操作していることを想定しています。つまり、AWS、Azure、k8sなどの仮想化環境を使用していない場合です。
この場合は、以下の手順に従ってください。仮想化プラットフォーム上にいる場合は、[Docker](https://github.com/karakuri-ai/OSWorld-JP?tab=readme-ov-file#docker-server-with-kvm-support-for-the-better)セクションを参照してください。

1. まず、このリポジトリをクローンして`cd`で移動します。次に、`requirements.txt`に記載されている依存関係をインストールします。環境管理にはCondaの最新バージョンの使用を推奨しますが、手動で依存関係をインストールすることも可能です。Pythonのバージョンが3.10以上であることを確認してください。
```bash
# OSWorldリポジトリをクローン
git clone https://github.com/karakuri-ai/OSWorld-JP

# クローンしたリポジトリのディレクトリに移動
cd OSWorld-JP

# オプション：OSWorld用のConda環境を作成
# conda create -n osworld python=3.10
# conda activate osworld

# 必要な依存関係をインストール
pip install -r requirements.txt
```

あるいは、ベンチマークタスクなしで環境のみをインストールすることもできます：
```bash
pip install desktop-env
```

2. [VMware Workstation Pro](https://www.vmware.com/products/workstation-pro/workstation-pro-evaluation.html)をインストールし（Apple Chipを搭載したシステムの場合は[VMware Fusion](https://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware+Fusion)をインストールしてください）、`vmrun`コマンドを設定します。インストール手順は[VMware Workstation Proのインストール方法](desktop_env/providers/vmware/INSTALL_VMWARE.md)を参照してください。以下のコマンドを実行して、インストールが成功したことを確認してください：
```bash
vmrun -T ws list
```
インストールと環境変数の設定が成功していれば、現在実行中の仮想マシンを示すメッセージが表示されます。
> **注意:** VMware Proで問題が発生した場合は、[VirtualBox](https://www.virtualbox.org/)の使用もサポートしています。ただし、並列処理やAppleチップ上のmacOSなどの機能は十分にサポートされていない可能性があります。

以上で準備完了です！セットアップスクリプトが必要な仮想マシンを自動的にダウンロードし、環境を設定します。

### Docker（KVMサポートのあるサーバーで高パフォーマンス）
ベアメタルサーバー以外で実行している場合、またはVMwareやVirtualBoxプラットフォームを使用したくない場合は、Dockerサポートの使用を推奨します。

#### 前提条件：マシンがKVMをサポートしているか確認
KVMサポート付きでVMを実行することを推奨します。ホスティングプラットフォームがKVMをサポートしているか確認するには、Linuxで以下を実行します
```
egrep -c '(vmx|svm)' /proc/cpuinfo
```
戻り値がゼロより大きければ、プロセッサはKVMをサポートできるはずです。
> **注意**: macOSホストは一般的にKVMをサポートしていません。macOS上でOSWorldを実行したい場合は、VMwareの使用をお勧めします。

#### Dockerのインストール
ホスティングプラットフォームがグラフィカルユーザーインターフェース（GUI）をサポートしている場合は、OSに応じて[Linux用Docker Desktopのインストール](https://docs.docker.com/desktop/install/linux/)または[Windows用Docker Desktopのインストール](https://docs.docker.com/desktop/install/windows-install/)を参照してください。それ以外の場合は、[Docker Engineのインストール](https://docs.docker.com/engine/install/)を行ってください。

#### 実験の実行
`DesktopEnv`を初期化する際に、以下の引数を追加してください：
- `provider_name`: `docker`
- `os_type`: VMのOSに応じて`Ubuntu`または`Windows`
> **注意**: 実験が異常中断された場合（例：中断シグナルによる）、残留Dockerコンテナがシステムパフォーマンスに影響を与える可能性があります。`docker stop $(docker ps -q) && docker rm $(docker ps -a -q)`を実行してクリーンアップしてください。

### AWS
クラウドサービスを使用した並列評価により、評価効率を大幅に向上させることができます（並列化により評価時間を1時間以内に短縮可能！）。また、トレーニングのインフラストラクチャとしても使用できます。
OSWorldタスクの大規模並列評価を可能にするHost-Clientアーキテクチャによる包括的なAWSサポートを提供しています。
詳細なセットアップ手順については、[パブリック評価ガイドライン](https://github.com/karakuri-ai/OSWorld-JP/blob/main/PUBLIC_EVALUATION_GUIDELINE.md)および[AWS設定ガイド](https://github.com/karakuri-ai/OSWorld-JP/blob/main/desktop_env/providers/aws/AWS_GUIDELINE.md)を参照してください。


## 🚀 クイックスタート
以下の最小限の例を実行して、環境と対話します：

```bash
# デフォルト設定での基本的な使用法
python quickstart.py

# プロバイダーとVMパスのカスタマイズ
python quickstart.py --provider_name vmware --path_to_vm "path/to/your/vm.vmx"
```

システムが正常動作する際のすべてのログが表示されます。これには、環境の正常な作成、セットアップの完了、アクションの正常な実行が含まれます。最後に、画面上での右クリックが成功したことが確認でき、これは準備が整ったことを意味します。

## 🧪 実験
### エージェントベースライン

> **⚠️ 重要な設定要件：**
>
> * **Googleアカウントタスク**: 一部のタスクにはGoogleアカウントへのアクセスとOAuth2.0の設定が必要です。詳細なセットアップ手順については[Googleアカウントガイドライン](ACCOUNT_GUIDELINE.md)を参照してください。
> * **プロキシ設定**: 一部のタスクではプロキシ設定が正しく機能する必要がある場合があります（これはあなたのネットワーク上の場所に対するウェブサイトの防御の強度に依存します）。システムのプロキシ設定ドキュメントを参照してください。
> * **設定が不足している場合の影響**: これらの設定が正しくセットアップされていない場合、対応するタスクは正しく実行されず、評価スコアが低くなります。


論文で使用したベースラインエージェントを実行したい場合は、GPT-4oのスクリーンショットのみの設定で、以下のコマンドを例として実行できます：

**OPENAI_API_KEY**環境変数にAPIキーを設定します
```bash
export OPENAI_API_KEY='changeme'
```

オプションで、カスタムOpenAI互換APIエンドポイントを使用するために**OPENAI_BASE_URL**を設定します
```bash
export OPENAI_BASE_URL='http://your-custom-endpoint.com/v1'  # オプション：デフォルトはhttps://api.openai.com
```

シングルスレッド実行（非推奨、`vmware`プロバイダーを例として使用）
```bash
python run.py \
    --provider_name vmware \
    --path_to_vm Ubuntu/Ubuntu.vmx \ FIXME
    --headless \
    --observation_type screenshot \
    --model gpt-4o \
    --sleep_after_execution 3 \
    --max_steps 15 \
    --result_dir ./results \
    --client_password password \
    --examples_folder_name examples_japanese
```

並列実行（プロバイダーを`docker`に切り替える例）
```bash
python run_multienv.py \
    --provider_name docker \
    --headless \
    --observation_type screenshot \
    --model gpt-4o \
    --sleep_after_execution 3 \
    --max_steps 15 \
    --num_envs 10 \
    --client_password password \
    --examples_folder_name examples_japanese    
```

エージェントのタスク完了のスクリーンショット、アクション、ビデオ録画を含む結果は、この場合`./results`（または指定した他の`result_dir`）ディレクトリに保存されます。
以下のコマンドを実行して結果を取得できます：
```bash
python show_result.py
```

## 評価
### ローカル評価
まず、[エージェントインターフェース](https://github.com/karakuri-ai/OSWorld-JP/blob/main/mm_agents/README.md)と[環境インターフェース](https://github.com/karakuri-ai/OSWorld-JP/blob/main/desktop_env/README.md)を読むことから始めてください。
エージェントインターフェースを正しく実装し、カスタマイズしたバージョンを`run.py`または`run_multienv.py`ファイルにインポートしてください。
その後、前のセクションと同様のコマンドを実行して、エージェントに対してベンチマークを実行できます。

<!--
### パブリック評価
結果を検証し、検証済みリーダーボードに表示したい場合は、私たちとのミーティングを予約する必要があります（現在のメンテナー：tianbaoxiexxx@gmail.com、yuanmengqi732@gmail.com）。あなたのエージェントコードを私たちの側で実行し、結果を報告します。
OSWorldフレームワーク下でのエージェント実装のアップロードと公開を許可していただく必要があります（モデルAPIの一般公開は選択可能です）。また、舞台裏で何が行われているかを一般に理解してもらうためのレポートも必要です。
あるいは、信頼できる機関に所属している場合は、モニタリングデータとトラジェクトリを共有していただくことも可能です。
結果を得るには、[パブリック評価ガイドライン](https://github.com/karakuri-ai/OSWorld-JP/blob/main/PUBLIC_EVALUATION_GUIDELINE.md)に注意深く従ってください。
-->

## ❓ FAQ
### 仮想マシンのユーザー名とパスワードは何ですか？
仮想マシンのユーザー名とパスワードは以下の通りです（プロバイダー`vmware`、`virtualbox`、`docker`の場合）：Ubuntuのアカウント認証情報は`user` / `password`に設定しています。
`aws`などのクラウドサービスプロバイダーの場合、弱いパスワードによる攻撃を防ぐため、デフォルトで`osworld-public-evaluation`を使用しています。
さらに変更を加える場合は、実験実行時にclient_password変数を設定し、DesktopEnvおよびAgent（サポートされている場合）に渡すことを忘れないでください。
プロキシの設定など一部の機能では、環境がsudo権限を取得するためにクライアントVMのパスワードが必要です。また、一部のOSWorldタスクでは、エージェントがタスクを完了するためにsudo権限を取得するためのパスワードが必要です。

### GoogleおよびGoogle Driveのアカウントと認証情報の設定方法は？

[アカウントガイドライン](ACCOUNT_GUIDELINE.md)をご参照ください。

### 仮想環境の日本語化は、どのようにして行われましたか？

[日本語版のオリジナル版との差分](JP_VER_NOTES.md)をご参照ください。

## 📄 引用

```
@inproceedings{OSWorld-JP,
    jtitle = {OSWorld-JP：言語を考慮した評価のための日本語版コンピュータユースベンチマーク},
    title = {OSWorld-JP: A Japanese Computer Use Benchmark for Language-aware Evaluation},
    jauthor = {庄司, 文武 and 吉田, 雄紀},
    author = {Shoji, Bumbu and Yoshida, Yuki},
    jbooktitle = {人工知能学会全国大会},
    booktitle = {The Annual Conference of JSAI},
    year = {2025},
}
```

----

This repository is a fork of [OSWorld](https://github.com/karakuri-ai/OSWorld-JP) by XLANG NLP Lab.
The original project is licensed under the Apache License 2.0, which is preserved in this repository.
