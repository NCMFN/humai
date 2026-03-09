import os
import sys
import subprocess

def run_script(script_name, *args):
    """Helper to run a validation script."""
    print(f"\n--- Running {os.path.basename(script_name)} ---")
    cmd = [sys.executable, script_name] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")
    return result.returncode == 0

def humanize_text(input_file, output_file):
    print(f"Reading input from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Provide instructions to the user to copy/paste the text to Claude to perform humanization
    # Since we don't have an API key or a way to call Claude directly from here.

    print("\n" + "="*80)
    print("ACTION REQUIRED: MANUAL LLM PASS")
    print("="*80)
    print("Because this script does not have access to an LLM API directly, you must")
    print("perform the Pass 1 (Diagnosis) and Pass 2 (Reconstruction) using an LLM.")
    print("Please follow these steps:")
    print("1. Create a prompt for an LLM (like Claude) using the contents of SKILL.md")
    print("   and the reference files in the `references/` directory.")
    print("2. Ask the LLM to humanize the contents of `original_chapter_8.txt`.")
    print("3. Save the resulting text to `humanized_chapter_8.txt`.")
    print("4. Re-run this script with the --validate flag to run the checks.")
    print("="*80 + "\n")

def run_validations(original_file, humanized_file):
    print(f"Running validations on {humanized_file} against {original_file}...")

    # Paths to validation scripts
    check_facts_script = os.path.join("validation", "check_facts.py")
    scan_banned_phrases_script = os.path.join("validation", "scan_banned_phrases.py")
    measure_readability_script = os.path.join("validation", "measure_readability.py")
    flag_changes_script = os.path.join("validation", "flag_changes.py")
    taboo_phrases_file = os.path.join("references", "taboo-phrases.md")

    success = True

    # 1. Check Facts
    if not run_script(check_facts_script, original_file, humanized_file):
        success = False

    # 2. Scan Banned Phrases
    if not run_script(scan_banned_phrases_script, humanized_file, taboo_phrases_file):
        success = False

    # 3. Measure Readability
    if not run_script(measure_readability_script, humanized_file):
        success = False

    # 4. Flag Changes
    if not run_script(flag_changes_script, original_file, humanized_file):
        success = False

    if success:
        print("\nAll validations PASSED! The text is humanized and compliant.")
    else:
        print("\nSome validations FAILED. Please review the output above and revise the text.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python router.py <original_file> <humanized_file> [--validate]")
        sys.exit(1)

    original_file = sys.argv[1]
    humanized_file = sys.argv[2]

    if len(sys.argv) == 4 and sys.argv[3] == "--validate":
        if not os.path.exists(humanized_file):
            print(f"Error: {humanized_file} not found. Please create it first.")
            sys.exit(1)
        run_validations(original_file, humanized_file)
    else:
        humanize_text(original_file, humanized_file)
