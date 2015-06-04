set -eu

if [ $# -ne 2 ]
then
  echo "usage: $0 idx_file svg_path"
  exit
fi

scripts_dir=$(dirname $0)

base=$(mktemp -d)/tanglegram
for i in $(seq $(cat $1| wc -l))
do
    $scripts_dir/plot-tangle.R $1 $i $base$i.svg
done
svg_stack.py $base* > $2
rm $base*
