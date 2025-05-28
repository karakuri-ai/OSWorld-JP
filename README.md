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


## ✨ OSWorld-JP とは？

近年、大規模言語モデル(LLM)を搭載したエージェントは、GUI や CLI インターフェースを介したコンピュータ操作の自動化に広く応用されています。しかし、[OSWorld](https://os-world.github.io/) など既存のエージェント評価ベンチマークは英語環境向けに最適化されており、日本語環境でのエージェント評価には適していません。そこで本研究では、プロンプトの翻訳、システム環境のローカライズ、タスク関連ファイルの修正を行い、OSWorld の日本語版である OSWorld-JP を開発しました。


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

> **注記：** [VirtualBox](https://www.virtualbox.org/) も利用可能ですが、VMware Pro に比べて並列実行や Apple チップ上での macOS のサポートが制限されます。

準備完了！セットアップスクリプトが必要な仮想マシンを自動でダウンロードして環境を構成します。

### Docker（サーバー環境向け：KVM サポートがあるとより良い）

ベアメタルサーバー以外での実行や、VMware/VirtualBox を使いたくない場合には、Docker を使った実行を推奨します。

#### 前提条件：KVM サポートの確認

KVM サポートを確認するには、Linux 上で以下のコマンドを実行してください：

```
egrep -c '(vmx|svm)' /proc/cpuinfo
```

結果が 0 より大きければ、プロセッサは KVM をサポートしています。

> **注記**：macOS は通常 KVM をサポートしていません。macOS で OSWorld-JP を実行したい場合は VMware を推奨します。

#### Docker のインストール

GUI が利用できる環境では、以下の手順を参照してください：

* [Linux で Docker Desktop をインストール](https://docs.docker.com/desktop/install/linux/)
* [Windows で Docker Desktop をインストール](https://docs.docker.com/desktop/install/windows-install/)

GUI がない場合は、[Docker Engine のインストール](https://docs.docker.com/engine/install/) を参照してください。

#### 実験の実行

`DesktopEnv` を初期化する際に以下の引数を指定してください：

* `provider_name`: `docker`
* `os_type`: `Ubuntu` または `Windows`（VM の OS による）

> **注記**：実験が途中で中断された場合、Docker コンテナが残り続けることがあります。コマンド `docker stop $(docker ps -q) && docker rm $(docker ps -a -q)` でクリーンアップしてください。

<!--
### その他

さらなる環境のサポートを進行中です👷。続報をお待ちください！
-->

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

### 仮想マシンのユーザー名とパスワードは？

* **Ubuntu:** `user` / `password`

### Google や Google Drive のアカウント認証はどう設定すればいい？

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
@misc{OSWorld-JP,
      title={OSWorld-JP: }, 
      author={Tianbao Xie and Danyang Zhang and Jixuan Chen and Xiaochuan Li and Siheng Zhao and Ruisheng Cao and Toh Jing Hua and Zhoujun Cheng and Dongchan Shin and Fangyu Lei and Yitao Liu and Yiheng Xu and Shuyan Zhou and Silvio Savarese and Caiming Xiong and Victor Zhong and Tao Yu},
      year={2024},
      eprint={2404.07972},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```
