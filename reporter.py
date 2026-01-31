import csv
import os
import re
from datetime import datetime
from analyzer import get_rules, check_log_line

def parse_log_details(line):
    
    # Generally there is an IP in both log types so I found IP first
    ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
    ip = ip_match.group(1) if ip_match else "unknown"

    # In here my web site Nginx/ Apache so I check for this auth log or web log using date 
    web_date_match = re.search(r'\[(.*?)\]', line)
    
    if web_date_match:
        log_date = web_date_match.group(1)
        
        # Get the other info 
        parts = re.findall(r'"(.*?)"', line)
        request_info = parts[0] if len(parts) > 0 else "unknown"
        user_agent = parts[-1] if len(parts) >= 3 else "unknown"
        
        return log_date, ip, request_info, user_agent

    # In here I make the system log part (Auth.log / Syslog) ---
    else:
      # general system logs are start with date 
        log_date = line[:15]
        
       # after ]: is my message part 
        msg_match = re.search(r']:\s(.*)', line)
        if msg_match:
            request_info = msg_match.group(1) 
        else:
            request_info = line.strip()[:50] 

        user_agent = "System log user agent none "
        
        return log_date, ip, request_info, user_agent

def export_to_csv(file_path):
    
   
    if not os.path.exists(file_path):
        print("Please check the file path please")
        return

   
    rules = get_rules()
    if not rules:
        print("Rules are empty please check the rules")
        return

    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"Report{timestamp}.csv"
    
    report_path = os.path.join('/app/reports', report_filename)

    detected_rows = []

    try:
       
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
            
                alerts = check_log_line(line, rules)
            
                if alerts:
                   
                    log_date, ip, request_info, user_agent = parse_log_details(line)

                    for alert in alerts:
                        detected_rows.append({
                            'Detection Date': datetime.now().strftime("%Y-%m-%d %H:%M"), 
                            'Log Date': log_date,
                            'Line Number': line_num,
                            'IP Address': ip,
                            'Threat Type': alert['name'],
                            'Severity': alert['severity'].upper(),
                            'Request Info': request_info,
                            'Device Info (User-Agent)': user_agent,
                            'Raw Log': line.strip()[:100] + "..." 
                        })
                    
        if detected_rows:
            with open(report_path, mode='w', newline='', encoding='utf-8-sig') as csv_file:
                fieldnames = ['Detection Date', 'Log Date', 'Line Number', 'IP Address', 'Threat Type', 'Severity', 'Request Info', 'Device Info (User-Agent)', 'Raw Log']
                
               
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
                
                writer.writeheader()
                for row in detected_rows:
                    writer.writerow(row)
            
            print(f" Your report is created {report_filename}")
            print(f"File Path : {report_path}")
            print(f" Total {len(detected_rows)} threats added your report.")
          
        else:
            print("Your logs are clean for this rules")

    except Exception as e:
        print(f" Reporting eror {e}")