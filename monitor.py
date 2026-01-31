import time
import os
from analyzer import get_rules, check_log_line

def start_monitoring(file_path):
    print(f" Live monitoring started: {file_path}")
    print("If you want to exit please Ctrl + C")
    
    rules = get_rules()
    
    if not rules:
        print(" Rules can't load  please check the rules.yaml")
        return
    try:
       
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            
            f.seek(0, 2) 
            last_size = os.path.getsize(file_path)
            
            while True:
                curr_size = os.path.getsize(file_path)
                
                
                if curr_size == last_size:
                    time.sleep(0.5)
                    continue
                
                
                if curr_size < last_size:
                    f.seek(0)
                
                line = f.readline()
                if not line:
                    
                    f.seek(f.tell())
                    continue
        
                
                check_log_line(line, rules)
               
                last_size = os.path.getsize(file_path)

    except FileNotFoundError:
        print("File can't found please check the gile path ")
    except KeyboardInterrupt:
        print("Altay Uyumaz o7")