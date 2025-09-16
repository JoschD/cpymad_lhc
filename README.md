# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/JoschD/cpymad_lhc/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------ | -------: | -------: | ------: | --------: |
| cpymad\_lhc/\_\_init\_\_.py         |        7 |        0 |    100% |           |
| cpymad\_lhc/corrector\_limits.py    |       72 |       72 |      0% |    13-168 |
| cpymad\_lhc/coupling\_correction.py |       90 |       90 |      0% |     9-282 |
| cpymad\_lhc/coupling\_knob.py       |       84 |       84 |      0% |     8-208 |
| cpymad\_lhc/general.py              |      245 |      154 |     37% |78-122, 138-197, 211-230, 249-297, 412-426, 437-451, 467, 483-501, 514-519, 547-552, 562, 578 |
| cpymad\_lhc/io.py                   |        8 |        0 |    100% |           |
| cpymad\_lhc/ir\_orbit.py            |      137 |       69 |     50% |110, 193, 258-264, 275-281, 286-316, 321-332, 337-341, 346-362 |
| cpymad\_lhc/logging.py              |       98 |        1 |     99% |        60 |
|                           **TOTAL** |  **741** |  **470** | **37%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/JoschD/cpymad_lhc/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/JoschD/cpymad_lhc/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/JoschD/cpymad_lhc/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/JoschD/cpymad_lhc/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FJoschD%2Fcpymad_lhc%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/JoschD/cpymad_lhc/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.