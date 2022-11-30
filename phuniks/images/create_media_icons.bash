#!/bin/bash

function fetch() {
  wget https://cdn.pixabay.com/photo/2012/04/16/11/59/dvd-icons-35680_960_720.png
}

function greyscale() {
  convert \
    dvd-icons-35680_960_720.png \
    -colorspace gray \
    -contrast-stretch 0 \
    dvd_greyscale.png
}

function colourize() {
  convert \
    dvd_greyscale.png \
    -colorspace RGB \
    -size 1x1 xc:'rgb(47, 167, 212)' \
    -fx 'u*v.p{0,0}' \
    dvd_coloured.png
  rm dvd_greyscale.png
}

function brighten() {
  convert \
    dvd_coloured.png \
    -brightness-contrast 20x0 \
    -contrast-stretch 0 \
    dvd_brightened.png
  rm dvd_coloured.png
}

function crop() {
  w=960 ; h=575 ; s=192
  convert dvd_brightened.png -crop ${s}x${s}+0+$((${h}-${s})) -trim dvd_start.png
  convert dvd_brightened.png -crop $((${s}-20))x${s}+$((${s}+10))+$((${h}-${s})) -trim dvd_play.png
  convert dvd_brightened.png -crop $((${s}))x${s}+$((${s}*3-20))+$((${h}-${s})) -trim dvd_pause.png
  convert dvd_brightened.png -crop $((${s}+10))x$((${s}-20))+$((${s}*4-10))+$((${h}-${s}+20)) -trim dvd_end.png
  convert dvd_brightened.png -crop $((${s}))x$((${s}))+$((${s}*4))+$((${h}-${s}*2+20)) -trim dvd_fast_forward.png
  convert dvd_brightened.png -crop $((${s}))x$((${s}))+0+$((${h}-${s}*2+20)) -trim dvd_rewind.png
  rm dvd_brightened.png
}

function expand() {
  for icon in start play pause end fast_forward rewind
  do
    identify dvd_${icon}.png
    convert dvd_${icon}.png -background None -gravity center -extent 192x149 dvd_${icon}_192x149.png
    convert dvd_${icon}_192x149.png -resize 20% dvd_${icon}_small.png
    rm dvd_${icon}.png dvd_${icon}_192x149.png
  done
}

#fetch
greyscale
colourize
brighten
crop
expand
#display dvd_play_192x149.png

