# puts line counts into a nice format
wc -l $@ | column -t | cut -f 1 -d' ' | xargs echo | tr ' ' ','
