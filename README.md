# LCR API

A Python API for Leader and Clerk Resources for the LDS Church. I've only tested it with Python 3.5+.

The following calls are supported, which correspond to a page in LCR:

- Birthday list
- Members moved out
- Members moved in
- Member list
- Calling list

There is one additional call supported:

- Individual photo – Gets the photo for an individual. This is the same call that LCR uses to show a picture when you go to a member's page.

More calls will be supported as I have time. Pull requests are welcomed!

## Disclaimer

This code is rough around the edges. I don't handle any cases where a person using this code doesn't have permissions to access the reports, so I don't know what will happen.

## Install

To install, run

```
pip3 install lcr-api
```

## Usage

```python
from lcr import API as LCR

lcr = LCR("<LDS USERNAME>", "<LDS PASSWORD>", <UNIT NUMBER>)

months = 5
move_ins = lcr.members_moved_in(months)

for member in move_ins:
    print("{}: {}".format(member['spokenName'], member['textAddress']))
```


### To Do
- Add more tests
- Support more reports and calls

