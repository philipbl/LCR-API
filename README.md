# LCR API

An API for Leader and Clerk Resources for the LDS Church.

The following calls are supported, which correspond to a page in LCR:

- Birthday list
- Members moved out
- Members moved in
- Member list

There are two additional calls supported:

- Individual photo – Gets the photo for an individual. This is the same call that LCR uses to show a picture when you go to a member's page.

- Custom home and visiting teaching (*under development*) – Outputs all information for home and visiting teaching. The result is a dictionary:

```
{
    "families": <information for each family in ward>,
    "hp": <High Priest home teaching information>,
    "eq": <Elders Quorum home teaching information>,
    "rs": <Relief Society visiting teaching information>
}
```

More calls will be supported as I have time. Pull requests are welcomed!
