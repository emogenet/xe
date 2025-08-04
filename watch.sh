#!/bin/bash

last=$(md5sum README.md | awk '{print $1}')

inotifywait -r -m -e modify .  |
while read file_path file_event file_name
do 
  echo path=${file_path} name=${file_name} event=${file_event}
  if test 'README.md' = "${file_name}"
  then
    now=$(md5sum README.md | awk '{print $1}')
    if test "$last" = "$now"
    then
      echo "actually unchanged"
    else
      echo "changed, running pandoc"
      pandoc -f markdown README.md > README.html
      last="$now"
    fi
  fi
done

