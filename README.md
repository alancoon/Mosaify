# Wallpapyr
Creates a mosaic of album covers using your most played tracks on Spotify (via Spotipy).  Written in Python 3.6.

To use, edit in your CLIENT_ID and CLIENT_SECRET (create an app: https://developer.spotify.com/my-applications/#!/applications), then run the Python script.

Wallpapyr arguments

positional arguments:
  user                  Your Spotify username

optional arguments:
  -h, --help            show this help message and exit
  -q {low,medium,high}, --quality {low,medium,high}
                        Quality of images, default is high
  -r, --rectangle       Enables rectangular wallpaper production, rather than
                        discarding excess images, program will create a
                        rectangular frame
  -o OUTPUT, --output OUTPUT
                        Specify an output filename, .jpg .jpeg .gif .png .bmp
                        accepted

![My collage created using Wallpapyr.](/out.png?raw=true "My collage")
