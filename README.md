# phantom_report
Python script to create a timeline PDF report from Phantom.us.


## Prerequisites
(TBC)

### WeasyPrint (https://weasyprint.org)
On Mac:
- `brew update`
- `brew install cairo pango gdk-pixbuf libxml2 libxslt libffi`
- `pip3 install WeasyPrint`


## Usage
`phantom_report.py <ContainerID> <ReportName>.pdf`
`phantom_report.py 12345 report_12345.pdf`
