import os

#get all paths

script_dir = os.path.dirname(os.path.abspath("main.py"))

bank_relative_path = "../data/bank.json"
bank_path = os.path.normpath(os.path.join(script_dir, bank_relative_path))

xp_relative_path = "../data/xp.json"
xp_path = os.path.normpath(os.path.join(script_dir, xp_relative_path))

config_relative_path = "config.yaml"
config_path = os.path.normpath(os.path.join(script_dir, config_relative_path))

# Set environ varibles for json and config.
os.environ["BANK_PATH"] = bank_path
os.environ["XP_PATH"] = xp_path
os.environ["CONFIG_PATH"] = config_path




