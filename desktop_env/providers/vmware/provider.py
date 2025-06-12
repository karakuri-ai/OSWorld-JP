import logging
import os
import platform
import re
import subprocess
import time

from desktop_env.providers.base import Provider

logger = logging.getLogger("desktopenv.providers.vmware.VMwareProvider")
logger.setLevel(logging.INFO)

WAIT_TIME = 3


def get_vmrun_type(return_list=False):
    if platform.system() == 'Windows' or platform.system() == 'Linux':
        if return_list:
            return ['-T', 'ws']
        else:
            return '-T ws'
    elif platform.system() == 'Darwin':  # Darwin is the system name for macOS
        if return_list:
            return ['-T', 'fusion']
        else:
            return '-T fusion'
    else:
        raise Exception("Unsupported operating system")


class VMwareProvider(Provider):
    @staticmethod
    def _execute_command(command: list, return_output=False):
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )

        if return_output:
            output = process.communicate()[0].strip()
            return output
        else:
            return None

    def start_emulator(self, path_to_vm: str, headless: bool, os_type: str):
        print("Starting VMware VM...")
        logger.info("Starting VMware VM...")

        while True:
            try:
                output = subprocess.check_output(f"vmrun {get_vmrun_type()} list", shell=True, stderr=subprocess.STDOUT)
                output = output.decode()
                output = output.splitlines()
                normalized_path_to_vm = os.path.abspath(os.path.normpath(path_to_vm))

                if any(os.path.abspath(os.path.normpath(line)) == normalized_path_to_vm for line in output):
                    logger.info("VM is running.")
                    break
                else:
                    logger.info("Starting VM...")
                    _command = ["vmrun"] + get_vmrun_type(return_list=True) + ["start", path_to_vm]
                    if headless:
                        _command.append("nogui")
                    VMwareProvider._execute_command(_command)
                    time.sleep(WAIT_TIME)

            except subprocess.CalledProcessError as e:
                logger.error(f"Error executing command: {e.output.decode().strip()}")

    def get_ip_address(self, path_to_vm: str) -> str:
        logger.info("Getting VMware VM IP address...")
        max_retries = 30  # Increase retry limit for VM startup
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # First check if VMware Tools are running
                if retry_count % 5 == 0:  # Check tools status every 5 attempts
                    tools_running = self.check_vmware_tools_status(path_to_vm)
                    if not tools_running:
                        logger.warning("VMware Tools are not running. VM may still be booting...")
                
                command = ["vmrun"] + get_vmrun_type(return_list=True) + ["getGuestIPAddress", path_to_vm, "-wait"]
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8"
                )
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    # Success - check if output looks like an IP address
                    ip_address = stdout.strip()
                    # Basic validation that we got an IP address, not an error message
                    if ip_address and not "Error" in ip_address and not "VMware Tools" in ip_address:
                        # Additional validation: check if it's a valid IP format
                        import re
                        ip_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
                        if re.match(ip_pattern, ip_address):
                            logger.info(f"VMware VM IP address: {ip_address}")
                            return ip_address
                        else:
                            raise Exception(f"Invalid IP address format: {ip_address}")
                    else:
                        raise Exception(f"Invalid IP address format: {ip_address}")
                else:
                    # Command failed
                    error_msg = stderr.strip() if stderr.strip() else stdout.strip()
                    raise Exception(f"vmrun getGuestIPAddress failed: {error_msg}")
                    
            except Exception as e:
                retry_count += 1
                logger.error(f"Attempt {retry_count}/{max_retries} - Failed to get VM IP address: {e}")
                
                if retry_count >= max_retries:
                    logger.error("Failed to get VM IP address after maximum retries.")
                    logger.error("This usually indicates one of the following issues:")
                    logger.error("1. VMware Tools are not installed in the virtual machine")
                    logger.error("2. The virtual machine is not fully booted yet")
                    logger.error("3. Network connectivity issues in the VM")
                    logger.error("4. VMware Workstation/Fusion is not properly configured")
                    logger.error(f"VM path: {path_to_vm}")
                    raise Exception("Failed to get VM IP address after maximum retries")
                
                time.sleep(WAIT_TIME)
                logger.info(f"Retrying to get VMware VM IP address... ({retry_count}/{max_retries})")

    def save_state(self, path_to_vm: str, snapshot_name: str):
        logger.info("Saving VMware VM state...")
        VMwareProvider._execute_command(
            ["vmrun"] + get_vmrun_type(return_list=True) + ["snapshot", path_to_vm, snapshot_name])
        time.sleep(WAIT_TIME)  # Wait for the VM to save

    def revert_to_snapshot(self, path_to_vm: str, snapshot_name: str):
        logger.info(f"Reverting VMware VM to snapshot: {snapshot_name}...")
        VMwareProvider._execute_command(
            ["vmrun"] + get_vmrun_type(return_list=True) + ["revertToSnapshot", path_to_vm, snapshot_name])
        time.sleep(WAIT_TIME)  # Wait for the VM to revert
        return path_to_vm

    def stop_emulator(self, path_to_vm: str):
        logger.info("Stopping VMware VM...")
        VMwareProvider._execute_command(["vmrun"] + get_vmrun_type(return_list=True) + ["stop", path_to_vm])
        time.sleep(WAIT_TIME)  # Wait for the VM to stop

    def check_vmware_tools_status(self, path_to_vm: str) -> bool:
        """Check if VMware Tools are running in the VM"""
        try:
            command = ["vmrun"] + get_vmrun_type(return_list=True) + ["checkToolsState", path_to_vm]
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8"
            )
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                tools_state = stdout.strip().lower()
                logger.info(f"VMware Tools state: {tools_state}")
                return tools_state == "running"
            else:
                logger.error(f"Failed to check VMware Tools state: {stderr.strip()}")
                return False
        except Exception as e:
            logger.error(f"Error checking VMware Tools status: {e}")
            return False
