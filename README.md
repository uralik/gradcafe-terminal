<p align="center">
<b><a href="#usage">Usage</a></b>
|
<b><a href="#screenshot">Screenshot</a></b>
</p>

# gradcafe-terminal

See the latest posts on http://thegradcafe.com for your chosen schools.  

## Usage

Modify the `UNIV_LIST` variable (line number `26`) to include the desired school names and their common variants.  

The following optional command-line arguments are supported.  

Usage: `gradcafe_terminal.py [-h] [-d DAYS]`  

Optional arguments:
`-h, --help`: Show this help message and exit
`-d DAYS, --days DAYS`: Maximum number of past days (from today) for which to fetch results. The default value is 7 days (1 week). Irrespective of the value chosen, a maximum of 250 results can be displayed.

## Screenshot
<div align="center">
	<img src="screenshots/1.png" alt="Screenshot of gradcafe-terminal.">
</div><br>
