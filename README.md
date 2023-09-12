# MAL_epub

Python script that has a 90% success rate at adding metadata to your epub file

Sometimes it doesn't work, but it's better than nothing

This little script was made with atrocious programming practices, so don't expect it to be pretty

but it kinda works so that's cool

## Usage

1. Download the script
2. Install the requirements
3. Put your client ID into the .env file
4. Run the script

## Requirements

- Python 3.6+
- [requests](https://pypi.org/project/requests/) (for scraping)
- [lxml](https://pypi.org/project/lxml/) (for scraping)

## More rambling

this script came to fruition because ebooklib is trash and you have to compeletly rewrite the epub file to add metadata

and im below the skill level to do that

and ebookmeta cant add covers or descriptions

so i made this

oh and also i have thought of making a calibre plugin but i dont know how to do that

## Known issues

- Sometimes the script will use the first author it finds, which is usually correct one but sometimes it isn't

## uh thanks for reading to the end i guess


