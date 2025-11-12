<!--
<p align="center">
  <img src="https://huggingface.co/datasets/xlangai/assets/resolve/main/github_banner_v2.png" alt="Banner">
</p>

<p align="center">
  <a href="https://os-world.github.io/">Website</a> •
  <a href="https://arxiv.org/abs/2404.07972">Paper</a> •
  <a href="https://timothyxxx.github.io/OSWorld/">Doc</a> •
  <a href="https://github.com/xlang-ai/OSWorld/tree/main/evaluation_examples">Data</a> •
  <a href="https://os-world.github.io/explorer.html">Data Viewer</a> •
  <a href="https://discord.gg/4Gnw7eTEZR">Discord</a>
</p>

<p align="center">
    <a href="https://img.shields.io/badge/PRs-Welcome-red">
        <img src="https://img.shields.io/badge/PRs-Welcome-red">
    </a>
    <a href="https://img.shields.io/github/last-commit/xlang-ai/OSWorld?color=green">
        <img src="https://img.shields.io/github/last-commit/xlang-ai/OSWorld?color=green">
    </a>
    <a href="https://opensource.org/licenses/Apache-2.0">
        <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg">
    </a>
    <a href="https://badge.fury.io/py/desktop-env">
        <img src="https://badge.fury.io/py/desktop-env.svg">
    </a>
    <a href="https://pepy.tech/project/desktop-env">
        <img src="https://static.pepy.tech/badge/desktop-env">
    </a>
    <br/>
</p>
-->
# OSWorld-JP

言語を考慮した評価のための、日本語版コンピュータユースベンチマーク

## 📢 アップデート

- 2025-05-28: 本ベンチマークに関して、2025年度 人工知能学会全国大会 (JSAI2025) にて発表予定です。日時等は[こちら](https://confit.atlas.jp/guide/event/jsai2025/subject/3Win5-56/tables) をご参照ください。

- 2025-05-28: 本 GitHub にて、本ベンチマークを v0.1 として公開しました。以下の内容を反映済みです。
    - [x] システム環境のローカライズ
    - [x] システムプロンプトの日本語化
    - [x] 全てのタスクのプロンプトの日本語化
    - [x] 344/437 (=79%) のタスクに関して、タスク内容にまで踏み込んだ日本語化（タスク関連ファイルの修正・タスクの読み替え等）

- 2025-11-04: **本リポジトリにて現在公開中の v0.1 に多くの不具合が含まれていることが判明しました。今後、不具合の修正作業を実施予定です。v0.1 の使用は推奨せず、今後公開予定の v0.2 以降の使用を強く推奨します。**

## ✨ OSWorld-JP とは？

近年、大規模言語モデル(LLM)を搭載したエージェントは、GUI や CLI インターフェースを介したコンピュータ操作の自動化に広く応用されています。しかし、[OSWorld](https://os-world.github.io/) など既存のエージェント評価ベンチマークは英語環境向けに最適化されており、日本語環境でのエージェント評価には適していません。そこで本研究では、プロンプトの翻訳、システム環境のローカライズ、タスク関連ファイルの修正を行い、OSWorld の日本語版である OSWorld-JP を開発しました。

> **注意：** 本ベンチマークは今後も改善活動によりバージョンアップがなされていく予定です。また、インターネット上のウェブサイトの挙動に依存するタスクが一部含まれており、永続性が保証されません。そのため、評価結果を公表する際には、ベンチマークのバージョンおよび評価を実施した日付を明記することを推奨します。

## 💾 インストール方法

### VMware/VirtualBox（デスクトップ、ノートパソコン、ベアメタルマシン）

仮想化されていないシステム（例：デスクトップ、ノートパソコン、ベアメタルマシン）を使用している場合は、以下の手順に従ってください。もし仮想化されたプラットフォーム（例：AWS、Azure、k8s）を使用している場合は、下記 Docker のセクションをご覧ください。

1. まず、このリポジトリをクローンして `cd` で移動し、`requirements.txt` に記載された依存関係をインストールします。環境管理には Conda の最新版を使うことが推奨されていますが、手動でのインストールも可能です。Python のバージョンは **3.9 以上** を使用してください。

```bash
# OSWorld-JP リポジトリをクローン
git clone https://github.com/karakuri-ai/OSWorld-JP

# クローンしたディレクトリに移動
cd OSWorld-JP

# オプション：OSWorld-JP 用の Conda 環境を作成
# conda create -n osworldjp python=3.9
# conda activate osworldjp

# 必要な依存パッケージをインストール
pip install -r requirements.txt
```

代替手段として、ベンチマークタスクを含まない環境のみをインストールすることもできます：

```bash
pip install desktop-env
```

2. [VMware Workstation Pro](https://www.vmware.com/products/workstation-pro/workstation-pro-evaluation.html) をインストールします（Apple チップ搭載マシンでは [VMware Fusion](https://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware+Fusion) を使用してください）。その後、`vmrun` コマンドを設定します。インストール手順については、[VMware Workstation Pro のインストール手順](desktop_env/providers/vmware/INSTALL_VMWARE.md)を参照してください。以下のコマンドで正常にインストールされていることを確認できます：

```bash
vmrun -T ws list
```

環境変数の設定が正常に完了していれば、現在起動中の仮想マシン一覧が表示されます。

> **注意：** [VirtualBox](https://www.virtualbox.org/) も利用可能ですが、VMware Pro に比べて並列実行や Apple チップ上での macOS のサポートが制限されます。

準備完了！セットアップスクリプトが必要な仮想マシンを自動でダウンロードして環境を構成します。

### Docker（サーバー環境向け：KVM サポートがあるとより良い）

ベアメタルサーバー以外での実行や、VMware/VirtualBox を使いたくない場合には、Docker を使った実行を推奨します。

#### 前提条件：KVM サポートの確認

KVM サポートを確認するには、Linux 上で以下のコマンドを実行してください：

``` bash
egrep -c '(vmx|svm)' /proc/cpuinfo
```

結果が 0 より大きければ、プロセッサは KVM をサポートしています。

> **注記**：macOS は通常 KVM をサポートしていません。macOS で OSWorld-JP を実行したい場合は VMware を推奨します。

#### Docker のインストール

GUI が利用できる環境では、以下の手順を参照してください：

- [Linux で Docker Desktop をインストール](https://docs.docker.com/desktop/install/linux/)
- [Windows で Docker Desktop をインストール](https://docs.docker.com/desktop/install/windows-install/)

GUI がない場合は、[Docker Engine のインストール](https://docs.docker.com/engine/install/) を参照してください。

#### 実験の実行

`DesktopEnv` を初期化する際に以下の引数を指定してください：

- `provider_name`: `docker`
- `os_type`: `Ubuntu` または `Windows`（VM の OS による）

> **注記**：実験が途中で中断された場合、Docker コンテナが残り続けることがあります。コマンド `docker stop $(docker ps -q) && docker rm $(docker ps -a -q)` でクリーンアップしてください。

<!--
### その他

さらなる環境のサポートを進行中です👷。続報をお待ちください！
-->

## 🇯🇵 日本語環境の設定

実験を実施する前に仮想環境を日本語に変更する必要があります。変更が必要な点を以下に示します。仮想環境を起動後、手動で変更が必要な点について設定言語の日本語化を行なってください。

- OS
- アプリ
        - chromium
        - gimp
        - libreoffice calc
        - libreoffice impress
        - libreoffice writer
        - vlc
        - vscode

日本語化が終了したらスナップショットを作成し、desktop_env.pyのsnapshotnameを変更したsnapshotに置き換えてください。
[snapshot nameを変更する箇所](https://github.com/karakuri-ai/OSWorld-JP/blob/a7b4eeea7e49403e6752e49d20f819b62f82ab53/desktop_env/desktop_env.py#L32)

### 変更手法

変更手法は大きく分けてCLIでの操作とGUIでの操作があります。CLIでの操作がうまくいかない場合はGUIからの操作を推奨します。

#### OS

##### GUIでの変更方法

1. 画面右上のシステム設定アイコン（歯車マーク）をクリックします
2. 設定メニューから「Region & Language」（地域と言語）を選択します
3. 「Language」（言語）の欄で「Manage Installed Languages」（インストール済み言語の管理）をクリックします
4. 「Install / Remove Languages...」（言語のインストール/削除）をクリックし、リストから「Japanese」（日本語）にチェックを入れて「Apply」（適用）をクリックします
5. インストールが完了したら、言語一覧から「日本語」を選択し、「Apply System-Wide」（システム全体に適用）をクリックします
6. 再起動を促すメッセージが表示されるので「Restart Now」（今すぐ再起動）をクリックします

##### CLIでの変更

```bash
#日本語ロケールのインストール
sudo apt update
sudo apt install -y language-pack-ja language-pack-ja-base
#ロケールの生成
sudo locale-gen ja_JP.UTF-8
#デフォルトロケールの設定
sudo update-locale LANG=ja_JP.UTF-8 LANGUAGE="ja_JP:ja"
#再起動による設定の反映
sudo reboot
```

#### アプリケーション

##### Chromium

###### Chromium - GUIでの設定

1. Chromiumを起動し、右上のメニューアイコン（縦に並んだ3点）をクリックします
2. 「Settings」（設定）を選択します
3. 左側のメニューから「Advanced」（詳細設定）を展開し、「Languages」（言語）をクリックします
4. 「Add languages」（言語を追加）をクリックし、リストから「日本語」を選択して「Add」（追加）をクリックします
5. 追加された「日本語」の行の右側にある3点メニューをクリックし、「Display Chromium in this language」（Chromiumをこの言語で表示する）を選択します
6. Chromiumを再起動して変更を適用します

###### Chromium - CLIでの設定

```bash
# Chromiumの設定ファイルが保存されているディレクトリに移動
cd ~/.config/chromium/Default/

# 設定ファイルを編集（存在しない場合は作成されます）
cat > Preferences << EOF
{
  "intl": {
    "accept_languages": "ja,ja_JP,en-US,en",
    "selected_languages": "ja,ja_JP,en-US,en"
  },
  "browser": {
    "enabled_labs_experiments": ["enable-force-ui-direction@1"],
    "app_locale": "ja"
  }
}
EOF

# Chromiumを再起動して変更を適用
```

##### GIMP

###### GIMP - GUIでの設定

1. GIMPを起動し、メニューバーから「Edit」（編集）→「Preferences」（設定）を選択します
2. 左側のメニューから「Interface」（インターフェース）を選択します
3. 「Language」（言語）のドロップダウンメニューから「Japanese (ja_JP.UTF-8)」を選択します
4. 「OK」をクリックし、GIMPを再起動して変更を適用します

###### GIMP - CLIでの設定

```bash
# GIMPの設定ファイルを編集
mkdir -p ~/.config/GIMP/2.10
cat > ~/.config/GIMP/2.10/gimprc << EOF
(language "ja_JP.UTF-8")
EOF

# GIMPを再起動して変更を適用
```

##### LibreOffice（Calc, Impress, Writer共通）

###### LibreOffice - GUIでの設定

1. LibreOfficeのいずれかのアプリケーションを起動します
2. メニューバーから「Tools」（ツール）→「Options」（オプション）を選択します
3. 左側のメニューから「Language Settings」（言語設定）→「Languages」（言語）を選択します
4. 「User Interface」（ユーザーインターフェース）、「Locale Setting」（ロケール設定）、「Default Languages for Documents」（文書のデフォルト言語）の各項目で「日本語」を選択します
5. 「OK」をクリックし、LibreOfficeを再起動して変更を適用します

###### LibreOffice - CLIでの設定

```bash
# LibreOfficeの設定ディレクトリを作成
mkdir -p ~/.config/libreoffice/4/user/

# 言語設定ファイルを作成
cat > ~/.config/libreoffice/4/user/registrymodifications.xcu << EOF
<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry">
 <item oor:path="/org.openoffice.Office.Linguistic/General"><prop oor:name="UILocale" oor:op="fuse"><value>ja-JP</value></prop></item>
 <item oor:path="/org.openoffice.Setup/L10N"><prop oor:name="ooLocale" oor:op="fuse"><value>ja-JP</value></prop></item>
 <item oor:path="/org.openoffice.Setup/L10N"><prop oor:name="ooSetupSystemLocale" oor:op="fuse"><value>ja-JP</value></prop></item>
</oor:items>
EOF

# LibreOfficeを再起動して変更を適用
```

##### VLC

###### VLC - GUIでの設定

1. VLCを起動し、メニューバーから「Tools」（ツール）→「Preferences」（設定）を選択します
2. 左下の「Show settings」（設定の表示）を「All」（すべて）に変更します
3. 左側のメニューから「Interface」（インターフェース）→「Main interfaces」（主要インターフェース）→「Qt」を選択します
4. 右側の「Language」（言語）ドロップダウンメニューから「Japanese」（日本語）を選択します
5. 「Save」（保存）をクリックし、VLCを再起動して変更を適用します

###### VLC - CLIでの設定

```bash
# VLCの設定ファイルを編集
mkdir -p ~/.config/vlc
cat > ~/.config/vlc/vlcrc << EOF
language=ja
EOF

# VLCを再起動して変更を適用
```

##### Visual Studio Code

###### VSCode - GUIでの設定

1. VSCodeを起動します
2. 左下の歯車アイコンをクリックし、「Settings」（設定）を選択します
3. 検索バーに「locale」と入力します
4. 「Configure Display Language」（表示言語の設定）をクリックします
5. 日本語言語パックがインストールされていない場合は、「Install additional languages...」（追加の言語をインストール）をクリックします
6. 表示されるマーケットプレイスで「Japanese Language Pack」を検索し、「Install」（インストール）をクリックします
7. インストール完了後、言語の選択リストから「ja」を選択します
8. 変更を適用するためにVSCodeを再起動するよう促されるので、「Restart Now」（今すぐ再起動）をクリックします

###### VSCode - CLIでの設定

```bash
# 日本語言語パックをインストール
code --install-extension MS-CEINTL.vscode-language-pack-ja

# 設定ファイルを編集
cat > ~/.config/Code/User/settings.json << EOF
{
    "locale": "ja"
}
EOF

# VSCodeを再起動して変更を適用
```

以上の設定変更が完了したら、仮想環境のスナップショットを作成してください。VMware Workstation/Fusionの場合は、仮想マシンを選択し、「VM」メニューから「Snapshot」→「Take Snapshot」を選択します。スナップショットに「日本語環境」などのわかりやすい名前を付けてください。

スナップショットを作成したら、`desktop_env.py`ファイルの`snapshotname`の値を変更したスナップショット名に更新してください。

##### GUIでの変更

1. 画面右上のシステム設定アイコン（歯車マーク）をクリックします
2. 設定メニューから「Region & Language」（地域と言語）を選択します
3. 「Language」（言語）の欄で「Manage Installed Languages」（インストール済み言語の管理）をクリックします
4. 「Install / Remove Languages...」（言語のインストール/削除）をクリックし、リストから「Japanese」（日本語）にチェックを入れて「Apply」（適用）をクリックします
5. インストールが完了したら、言語一覧から「日本語」を選択し、「Apply System-Wide」（システム全体に適用）をクリックします
6. 再起動を促すメッセージが表示されるので「Restart Now」（今すぐ再起動）をクリックします

## 🚀 クイックスタート

以下の最小限の例で環境と対話できます：

```python
from desktop_env.desktop_env import DesktopEnv

example = {
    "id": "94d95f96-9699-4208-98ba-3c3119edf9c2",
    "instruction": "Spotify をこのシステムにインストールしたいです。手伝ってくれますか？",
    "config": [
        {
            "type": "execute",
            "parameters": {
                "command": [
                    "python",
                    "-c",
                    "import pyautogui; import time; pyautogui.click(960, 540); time.sleep(0.5);"
                ]
            }
        }
    ],
    "evaluator": {
        "func": "check_include_exclude",
        "result": {
            "type": "vm_command_line",
            "command": "which spotify"
        },
        "expected": {
            "type": "rule",
            "rules": {
                "include": ["spotify"],
                "exclude": ["not found"]
            }
        }
    }
}

env = DesktopEnv(action_space="pyautogui")

obs = env.reset(task_config=example)
obs, reward, done, info = env.step("pyautogui.rightClick()")
```

システムのログが正常に表示され、環境作成、セットアップ、アクションの実行が成功するのを確認できます。最終的に右クリックに成功している様子が表示されていれば、準備完了です。

## 🧪 実験

### エージェントのベースライン

論文（訳註: オリジナルの OSWorld の論文です）で使用されたベースラインエージェントを実行したい場合、以下のコマンドで GPT-4V のスクリーンショット設定に基づいて実行可能です：

API キーを環境変数に設定：

```bash
export OPENAI_API_KEY='changeme'
```

```bash
python run.py --path_to_vm Ubuntu/Ubuntu.vmx --headless --observation_type screenshot --model gpt-4-vision-preview --result_dir ./results
```

結果（スクリーンショット、アクション、ビデオ記録）は `./results` ディレクトリに保存されます。その後、以下のコマンドで結果を確認できます：

```bash
python show_result.py
```

### 評価

まず、[エージェントインターフェース](https://github.com/karakuri-ai/OSWorld-JP/blob/main/mm_agents/README.md)と[環境インターフェース](https://github.com/karakuri-ai/OSWorld-JP/blob/main/desktop_env/README.md)を読んでください。インターフェースを実装し、`run.py` にカスタムエージェントを読み込んだ後、先ほどのようなコマンドでベンチマークを実行できます。

## ❓ よくある質問（FAQ）

### 仮想マシンのユーザー名とパスワードは何ですか？

- **Ubuntu:** `user` / `password`

### Google や Google Drive のアカウント認証はどう設定すればいいですか？

[アカウントガイド](ACCOUNT_GUIDELINE.md)を参照してください。

<!--
### GFW（グレートファイアウォール）下でのプロキシ設定は？

[プロキシ設定ガイド](PROXY_GUIDELINE.md)を参照してください。

### 各種設定における実行時間とコストは？

| 設定                       | 想定時間 | コスト（全テスト / 小テスト） |
| ------------------------ | ---- | ---------------- |
| GPT-4V（スクリーンショット）        | 10時間 | \$100（\$10）      |
| Gemini-ProV（スクリーンショット）   | 15時間 | \$0（\$0）         |
| Claude-3 Opus（スクリーンショット） | 15時間 | \$150（\$15）      |
| GPT-4V（アクセシビリティツリーなど）    | 30時間 | \$500（\$50）      |

\*並列実行なし、2024年4月時点の計算。

-->

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

This repository is a fork of [OSWorld](https://github.com/xlang-ai/OSWorld) by XLANG NLP Lab.
The original project is licensed under the Apache License 2.0, which is preserved in this repository.
