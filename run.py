import structcheck

structcheck.scan([
    "-p", "Y:\\",
    "-r", "Y:\\report.txt",
    "-d", "Y:\\report.json",
    "-c", "T:\\admin_skipper\\Share - SkipperNDT.json",
    "-n", "T:\\admin_skipper\\regex_names.json",
    "-v", "T:\\admin_skipper\\regex_variables.json",
    "-s", "T:\\admin_skipper\\styles.json",
])
