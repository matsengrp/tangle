# puts line counts into a nice format
wc -l $@  | head -n -1 | column -t | cut -f 1 -d' ' | xargs echo | tr ' ' ','
