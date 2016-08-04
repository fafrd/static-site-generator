A very simple static blog generator in python. takes markdown, outputs html.

very similar to https://github.com/botherder/habu, I lifted some code from that but I've added enough features to consider it my own

## usage
place posts as markdown in the posts/directory. the first line should be
`title: First post`
then an empty line, then markdown code

add sections of code like [code:bash]some bash script[/code]. (substitute python, xml, whatever for bash)

you'll want to change the template in the templates/ folder

generate with
`python ./generate.py -d /path/to/web/root`

## example
http://kianbradley.com

## todo
I want to implement a tag system. that would be nifty.

I need to fix how dates work. Right now it just takes the current date for every blog entry, which is less than ideal
