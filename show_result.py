import os
import logging

logger = logging.getLogger(__name__)

def get_result(action_space, use_model, observation_type, result_dir):
    target_dir = "results/main_0219/pyautogui/screenshot/gemini-1.5-pro-latest/"#os.path.join(result_dir, action_space, observation_type, use_model)
    #target_dir = "results/main_0219/pyautogui/screenshot/gpt-4o-2024-11-20/"
    if not os.path.exists(target_dir):
        print("New experiment, no result yet.")
        return None

    all_result = []
    domain_result = {}          # ドメインごとの結果リスト
    all_result_for_analysis = {}  # ドメイン・各例の結果
    error_counts = {}           # ドメインごとのエラー件数

    # 各ドメインのフォルダを走査
    for domain in os.listdir(target_dir):
        domain_path = os.path.join(target_dir, domain)
        if os.path.isdir(domain_path):
            domain_result[domain] = []
            error_counts[domain] = 0  # 初期化
            for example_id in os.listdir(domain_path):
                example_path = os.path.join(domain_path, example_id)
                if os.path.isdir(example_path):
                    result_file = os.path.join(example_path, "result.txt")
                    if os.path.exists(result_file):
                        try:
                            with open(result_file, "r", encoding="utf-8") as f:
                                result_str = f.read().strip()
                            # 数値に変換を試みる
                            try:
                                result_value = float(result_str)
                            except Exception as conv_e:
                                logger.error("Error converting result in %s: %s", example_path, conv_e)
                                result_value = 0.0
                                error_counts[domain] += 1
                        except Exception as e:
                            logger.error("Error reading result.txt in %s: %s", example_path, e)
                            result_value = 0.0
                            error_counts[domain] += 1
                    else:
                        logger.warning("result.txt not found in %s", example_path)
                        result_value = 0.0
                        error_counts[domain] += 1

                    domain_result[domain].append(result_value)
                    all_result_for_analysis.setdefault(domain, {})[example_id] = result_value
                    all_result.append(result_value)

    # 各ドメインごとの集計結果を表示
    for domain, results in domain_result.items():
        num_runs = len(results)
        if num_runs > 0:
            success_rate = sum(results) / num_runs * 100
        else:
            success_rate = 0.0
        print(f"Domain: {domain}, Runned: {num_runs}, Success Rate: {success_rate:.2f}%, Error Count: {error_counts[domain]}")

    # 例としてOffice, Daily, Professionalドメインの集計も出力する
    try:
        office_domains = domain_result["libreoffice_calc"] + domain_result["libreoffice_impress"] + domain_result["libreoffice_writer"]
        office_rate = sum(office_domains) / len(office_domains) * 100
        print(">>>>>>>>>>>>>")
        print("Office", "Success Rate:", f"{office_rate:.2f}%", "Total Errors:",
              error_counts.get("libreoffice_calc", 0) +
              error_counts.get("libreoffice_impress", 0) +
              error_counts.get("libreoffice_writer", 0))
    except KeyError:
        print("Office domain data missing.")

    try:
        daily_domains = domain_result["vlc"] + domain_result["thunderbird"] + domain_result["chrome"]
        daily_rate = sum(daily_domains) / len(daily_domains) * 100
        print("Daily", "Success Rate:", f"{daily_rate:.2f}%", "Total Errors:",
              error_counts.get("vlc", 0) +
              error_counts.get("thunderbird", 0) +
              error_counts.get("chrome", 0))
    except KeyError:
        print("Daily domain data missing.")

    try:
        prof_domains = domain_result["gimp"] + domain_result["vs_code"]
        prof_rate = sum(prof_domains) / len(prof_domains) * 100
        print("Professional", "Success Rate:", f"{prof_rate:.2f}%", "Total Errors:",
              error_counts.get("gimp", 0) +
              error_counts.get("vs_code", 0))
    except KeyError:
        print("Professional domain data missing.")

    # 分析用の全結果をjsonとして保存
    with open(os.path.join(target_dir, "all_result.json"), "w", encoding="utf-8") as f:
        f.write(str(all_result_for_analysis))

    if not all_result:
        print("New experiment, no result yet.")
        return None
    else:
        print("Runned:", len(all_result), "Current Success Rate:", sum(all_result) / len(all_result) * 100, "%")
        return all_result

if __name__ == '__main__':
    get_result("pyautogui", "gemini-1.5-pro-latest ", "screenshot", "./results/main_0219")
#results/main_0219/pyautogui/screenshot/gemini-1.5-pro-latest/chrome