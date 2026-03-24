#!/usr/bin/env python3
"""
Manual Mode - Setup OSWorld environment and wait for human interaction
Press Enter in the terminal when finished to evaluate and save results

Usage:

python run_manual.py \
      --provider_name vmware \
      --path_to_vm vmware_vm_data/Ubuntu0/Ubuntu0.vmx \
      --task_config evaluation_examples/examples/libreoffice_calc/357ef137-7eeb-4c80-a3bb-0951f26a8aff.json \
      --client_password password \
      --result_dir ./results/manual_test
"""
from desktop_env.desktop_env import DesktopEnv
import argparse
import json
import os
import datetime
import logging

# Configure root logger to capture all desktopenv logs
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)  # Set to DEBUG to see all logs

# Console handler for standard output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Change to DEBUG if you want all logs in console
formatter = logging.Formatter('[%(asctime)s %(levelname)s %(name)s] %(message)s')
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

# File handler for debug logs
os.makedirs("logs", exist_ok=True)
debug_handler = logging.FileHandler(
    os.path.join("logs", f"debug_manual_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
    encoding="utf-8"
)
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)
root_logger.addHandler(debug_handler)

# IMPORTANT: Explicitly set level for desktopenv loggers
logging.getLogger("desktopenv").setLevel(logging.DEBUG)
logging.getLogger("desktopenv.metric").setLevel(logging.DEBUG)
logging.getLogger("desktopenv.metric.general").setLevel(logging.DEBUG)
logging.getLogger("desktopenv.getters").setLevel(logging.DEBUG)

# Get logger for this module
logger = logging.getLogger("desktopenv.run_manual")

def evaluate_and_save(env, task_config, result_dir):
    """Evaluate the task and save results"""
    try:
        # Create result directory
        os.makedirs(result_dir, exist_ok=True)

        # Get final observation
        logger.info("Capturing final state...")
        obs = env._get_obs()

        # Save final screenshot
        timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
        screenshot_file = os.path.join(result_dir, f"final_state_{timestamp}.png")
        with open(screenshot_file, "wb") as f:
            f.write(obs['screenshot'])
        logger.info(f"Final screenshot saved to {screenshot_file}")

        # Evaluate
        logger.info("Running evaluation...")
        result = env.evaluate()
        logger.info(f"Evaluation Result: {result:.2f}")

        # Save result
        result_file = os.path.join(result_dir, "result.txt")
        with open(result_file, "w", encoding="utf-8") as f:
            f.write(f"{result}\n")
        logger.info(f"Result saved to {result_file}")

        # Save trajectory info
        traj_file = os.path.join(result_dir, "traj.jsonl")
        with open(traj_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "timestamp": timestamp,
                "instruction": task_config.get("instruction", "N/A"),
                "result": result,
                "screenshot_file": f"final_state_{timestamp}.png"
            }))
            f.write("\n")
        logger.info(f"Trajectory saved to {traj_file}")

        print("\n" + "="*60)
        print(f"EVALUATION COMPLETE")
        print("="*60)
        print(f"Result: {result:.2f}")
        print(f"Results saved to: {result_dir}")
        print("="*60 + "\n")

        return result

    except Exception as e:
        logger.error(f"Error during evaluation: {e}", exc_info=True)
        return None

def main():
    parser = argparse.ArgumentParser(description="OSWorld Manual Mode - Setup environment for human interaction")
    parser.add_argument("--provider_name", type=str, default="vmware", help="Provider name (vmware, docker, etc.)")
    parser.add_argument("--path_to_vm", type=str, required=True, help="Path to VM file")
    parser.add_argument("--os_type", type=str, default="Ubuntu", help="OS type")
    parser.add_argument("--action_space", type=str, default="pyautogui", help="Action space")
    parser.add_argument("--task_config", type=str, required=True, help="Path to task config JSON")
    parser.add_argument("--client_password", type=str, default="password", help="VM password")
    parser.add_argument("--result_dir", type=str, default=None, help="Directory to save results")
    args = parser.parse_args()

    # Load task config
    with open(args.task_config, 'r', encoding='utf-8') as f:
        task_config = json.load(f)

    # Setup result directory
    if args.result_dir is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        task_id = task_config.get('id', 'unknown')
        args.result_dir = os.path.join("./results", "run_manual", task_id, timestamp)

    # Initialize environment with GUI visible (headless=False)
    logger.info("Initializing OSWorld environment...")
    env = DesktopEnv(
        provider_name=args.provider_name,
        path_to_vm=args.path_to_vm,
        os_type=args.os_type,
        action_space=args.action_space,
        headless=False,  # Show GUI for human interaction
        client_password=args.client_password
    )

    try:
        # Force snapshot revert by marking environment as used
        # This ensures we always start from a clean state
        logger.info("Marking environment as used to force snapshot revert...")
        env.is_environment_used = True

        # Setup environment
        logger.info("Setting up environment with task...")
        obs = env.reset(task_config=task_config)
        logger.info(f"Task: {task_config.get('instruction', 'N/A')}")

        print("\n" + "="*60)
        print("MANUAL MODE ACTIVE")
        print("="*60)
        print(f"Task: {task_config.get('instruction', 'N/A')}")
        print(f"")
        print(f"VM is now running and visible.")
        print(f"You can interact with the VM directly through its window.")
        print(f"")
        print(f"When finished, return to this terminal:")
        print(f"  - Press Enter to complete normally")
        print(f"  - Type 'f' + Enter if task is infeasible/impossible")
        print(f"  - Press Ctrl+C to exit without evaluation")
        print("="*60 + "\n")

        # Wait for user to finish manual interaction
        user_input = input("Press Enter when done (or 'f' + Enter for FAIL): ").strip().lower()

        # Handle user input
        if user_input == "f":
            logger.info("User declared task as FAIL (infeasible)")
            print("\nRecording FAIL declaration...")
            env.step("FAIL")
        elif user_input == "":
            logger.info("User completed the task normally")
        else:
            logger.warning(f"Unknown input '{user_input}', treating as DONE")

        # Evaluate and save results
        logger.info("\n\nStarting evaluation...")
        evaluate_and_save(env, task_config, args.result_dir)

    except KeyboardInterrupt:
        logger.info("\n\nExiting without evaluation...")
    finally:
        env.close()
        logger.info("Environment closed.")

if __name__ == "__main__":
    main()
