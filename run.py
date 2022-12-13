import structcheck

structcheck.scan([
    "-p", "\\\\NAS-SKIPPERNDT\\Share - SkipperNDT",
    "-r", "\\\\NAS-SKIPPERNDT\\Share - SkipperNDT\\report.txt",
    "-d", "\\\\NAS-SKIPPERNDT\\Share - SkipperNDT\\report.json",
    "-c", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\Share - SkipperNDT.json",
    "-n", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\regex_names.json",
    "-v", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\regex_variables.json",
    "-s", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\styles.json",
])

structcheck.scan([
    "-p", "\\\\NAS-SKIPPERNDT\\Process",
    "-r", "\\\\NAS-SKIPPERNDT\\Process\\report.txt",
    "-d", "\\\\NAS-SKIPPERNDT\\Process\\report.json",
    "-c", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\Process.json",
    "-n", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\regex_names.json",
    "-v", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\regex_variables.json",
    "-s", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\styles.json",
])

structcheck.scan([
    "-p", "\\\\NAS-SKIPPERNDT\\Data",
    "-r", "\\\\NAS-SKIPPERNDT\\Data\\report.txt",
    "-d", "\\\\NAS-SKIPPERNDT\\Data\\report.json",
    "-c", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\Data.json",
    "-n", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\regex_names.json",
    "-v", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\regex_variables.json",
    "-s", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\styles.json",
])

