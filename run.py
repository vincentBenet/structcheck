import structcheck

structcheck.scan([
    "-p", "\\\\NAS-SKIPPERNDT\Share - SkipperNDT",
    "-r", "\\\\NAS-SKIPPERNDT\Share - SkipperNDT\\report.txt",
    "-d", "\\\\NAS-SKIPPERNDT\Share - SkipperNDT\\report.json",
    "-c", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\Share - SkipperNDT.json",
    "-n", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\regex_names.json",
    "-v", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\regex_variables.json",
    "-s", "\\\\NAS-SKIPPERNDT\\homes\\admin_skipper\\styles.json",
])
