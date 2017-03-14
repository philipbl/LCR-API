# LCR API

A Python API for Leader and Clerk Resources for the LDS Church. I've only tested it with Python 3.5.

The following calls are supported, which correspond to a page in LCR:

- Birthday list
- Members moved out
- Members moved in
- Member list

There are two additional calls supported:

- Individual photo – Gets the photo for an individual. This is the same call that LCR uses to show a picture when you go to a member's page.

- Custom home and visiting teaching – Outputs all information for home and visiting teaching. This call isn't very good and I need to improve it in the future. The result is a dictionary:

```
{
    "families": <information for each family in ward>,
    "hp": <High Priest home teaching information>,
    "eq": <Elders Quorum home teaching information>,
    "rs": <Relief Society visiting teaching information>
}
```

More calls will be supported as I have time. Pull requests are welcomed!

## Disclaimer

This code is rough around the edges. I don't handle any cases where a person using this code doesn't have permissions to access the reports, so I don't know what will happen.

## Install

To install, run

```
pip3 install https://github.com/philipbl/LCR-API/archive/master.zip
```

## Usage

```python
from lcr import API as LCR

lcr = LCR("<LDS USERNAME>", "<LDS PASSWORD>", <UNIT NUMBER>)

move_ins = lcr.members_moved_in()

for member in move_ins:
    print("{}: {}".format(member['spokenName'], member['textAddress']))
```


### To Do
- Add more tests
- Refactor code
- Set up session cookies for repeated log ins
- Support more reports and calls

