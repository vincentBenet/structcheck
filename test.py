import structcheck

scans = [
    r"C:\Users\vince\Desktop\structcheck\tests\data_fail\datetime_file",
    r"C:\Users\vince\Desktop\structcheck\tests\data_fail\datetime_folder",
    r"C:\Users\vince\Desktop\structcheck\tests\data_succes\datetime",
    r"C:\Users\vince\Desktop\structcheck\tests\data_succes\ignored",
    r"C:\Users\vince\Desktop\structcheck\tests\data_succes\regex",
    r"C:\Users\vince\Desktop\structcheck\tests\data_succes\standard",
]

for scan in scans:
    txt, reports, logs = structcheck.scan(["-p", scan])
    
    print(f"{reports = }")
    print(f"{logs = }")
