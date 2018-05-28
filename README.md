# phantom_report
Python script to create a timeline PDF report from Phantom.us.


## Prerequisites
(TBC)

### WeasyPrint (https://weasyprint.org)
On Mac:
- `brew update`
- `brew install cairo pango gdk-pixbuf libxml2 libxslt libffi`
- `pip3 install WeasyPrint`

On CentOS:
- `sudo yum install weasyprint`
- `pip3 install WeasyPrint`

## Installation
- `git clone https://github.com/Julien-Bernard/phantom_report.git`
- `cd phantom_report`
- `cp config_ori.py config.py`
- `vim config.py` (edit settings)


## Usage
- `phantom_report.py <ContainerID> <ReportName>.pdf`
- `phantom_report.py 12345 report_12345.pdf`
