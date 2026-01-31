import os
import yaml
import re 


def get_rules():

    
    config_path = '/app/config/rules.yaml'
    
    if not os.path.exists(config_path):
        print(f"The configiration file can't found : {config_path}")
        return []

    with open(config_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data.get('rules', [])
        except yaml.YAMLError as e:
            print(f"Eror when accesing yaml : {e}")
            return []


def check_log_line(line, rules):
    alerts = []
    for rule in rules:
        try:
            if rule.get('type') == 'regex':
                # I use regex re.search for better search 
                if re.search(rule['pattern'], line, re.IGNORECASE):
                    alert = {
                        'name': rule.get('name'),
                        'severity': rule.get('severity', 'info'),
                        'log': line.strip()
                    }
                    alerts.append(alert)

                    print(f"[{rule.get('severity', 'INFO').upper()}]: {rule.get('name')}")
                    print(f"Log: {line.strip()[:100]}...")
                    print("-" * 30)

        except re.error as e:
            print(f" There is  incorrect regex rule check the rule! {rule.get('name')}: {e}")
            
    return alerts

def analyze_file(file_path):
    print(f"\n File path check {file_path}")
    
    
    if not os.path.exists(file_path):
        print("  Check the filepath please !")
        return

    rules = get_rules()
    if not rules:
        print(" The rules file  config/rules.yaml are is empty please check the file.")
        return

    detection_count = 0
    line_num = 0
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                alerts = check_log_line(line, rules)
                detection_count += len(alerts)
                
    except Exception as e:
        print(f" Read error {e}")

    print("=" * 50)
    print(f"total scanned lines: {line_num}")
    print(f" Potential threats: {detection_count}")