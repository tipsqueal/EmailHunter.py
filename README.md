# hunter_python
### A Hunter API client written in Python

## Installation
Requirements:

* Python 3 (because it's 2016)


To install:
```
pip install hunter-python
```

To update:
```
pip install --upgrade hunter-python
```

## Usage

hunter_python supports the three main methods of the [Hunter](https://hunter.io/api/docs) API:
`search`, `find` and `verify`. There are two ways to use hunter_python:

* As a Python library
* As a command line (CLI) tool.

#### To use the hunter_python Python library:

Import the client and instantiate it:
```python
from hunter import HunterClient
```
```
client = HunterClient('my_api_key')
```

You can search:
```python
client.search('google.com')
```

By default 10 results are returned, so use offset to paginate:
```python
client.search('google.com', offset=10)
```

You can also limit the number of results:
```python
client.search('google.com', limit=5)
```

You can also change type (personal or generic):
```python
client.search('google.com', type_='personal')
```

You can find an email:
```python
client.find('google.com', 'Sergey', 'Brin')
```

And you can verify the deliverability of an email address:
```python
client.verify('sergey@google.com')
```

#### To use hunter_python as a CLI tool:

```
hunter [command name] [api_key] [other args]
```

The command name is `search`, `find` or `verify`, the api_key is the API key associated with your Hunter
account

The other arguments depend on the command you are using:
```
--domain       Required for search and find commands
--limit        Optional, used with search command
--offset       Optional, used with search command
--type         Optional, used with search command
--first_name   Required for find command
--last_name    Required for find command
--email        Required for verify command
--file         Path to a CSV to be used with the specified command.
               CSV must have a column for each argument used.
```

The file argument is useful when you want to make several requests of the same type. For example if you wanted to find
the email addresses for several people at an organization you would do the following:
```
hunter find [api_key] --file people.csv > emails.csv
```

Where `people.csv` looks like:
```
domain,first_name,last_name
google.com,larry,page
google.com,sergey,brin
facebook.com,mark,zuckerberg
```

The output will also be in a CSV format.

## License
Copyright © 2015 Alan Vezina

Released under The MIT License (MIT), see the LICENSE file for details
