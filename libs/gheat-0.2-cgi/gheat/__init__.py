import os

os.environ['PYTHON_EGG_CACHE'] = '/tmp'
import pymongo

# Configuration
# =============
# Set some things that backends will need.

conf = {}

ALWAYS_BUILD = ('true', 'yes', '1')
ALWAYS_BUILD = conf.get('_always_build', '').lower() in ALWAYS_BUILD

BUILD_EMPTIES = ('true', 'yes', '1')
BUILD_EMPTIES = conf.get('_build_empties', 'true').lower() in BUILD_EMPTIES

os.umask(0002)

SIZE = 256 # size of (square) tile; NB: changing this will break gmerc calls!
MAX_ZOOM = 31 # this depends on Google API; 0 is furthest out as of recent ver.


# Database
# ========

def get_cursor():
    mconn = pymongo.Connection()
    return mconn.heatmaps.points

from gheat import pygame_ as backend

# Set up color schemes and dots.
# ==============================

color_schemes = dict()          # this is used below
_color_schemes_dir = os.path.join('etc', 'color-schemes')
for fname in os.listdir(_color_schemes_dir):
    if not fname.endswith('.png'):
        continue
    name = os.path.splitext(fname)[0]
    fspath = os.path.join(_color_schemes_dir, fname)
    color_schemes[name] = backend.ColorScheme(name, fspath)

def load_dots(backend):
    """Given a backend module, return a mapping of zoom level to Dot object.
    """
    return dict([(zoom, backend.Dot(zoom)) for zoom in range(MAX_ZOOM)])
dots = load_dots(backend) # factored for easier use from scripts

ROOT = "/var/cache/heatmap"

def get_tile(path):
    fspath = ROOT + path

    if path.endswith('.png') and 'empties' not in path and not os.path.exists(fspath): 
                        # let people hit empties directly if they want; why not?


        # Parse and validate input.
        # =========================
        # URL paths are of the form:
        #
        #   /<mapname>/<color_scheme>/<zoom>/<x>,<y>.png
        #
        # E.g.:
        #
        #   /nyctrip/classic/3/0,1.png

        raw = path[:-4] # strip extension
        try:
            assert raw.count('/') == 4, "%d /'s" % raw.count('/')
            foo, dbname, color_scheme, zoom, xy = raw.split('/')
            assert color_scheme in color_schemes, ( "bad color_scheme: "
                                                  + color_scheme
                                                   )
            assert xy.count(',') == 1, "%d /'s" % xy.count(',')
            x, y = xy.split(',')
            assert zoom.isdigit() and x.isdigit() and y.isdigit(), "not digits"
            zoom = int(zoom)
            x = int(x)
            y = int(y)
            assert 0 <= zoom <= 30, "bad zoom: %d" % zoom
        except AssertionError, err:
            return str(err)


        # Build and save the file.
        # ========================
        # The tile that is built here will be served by the static handler.

        color_scheme = color_schemes[color_scheme]
        tile = backend.Tile(color_scheme, dots, zoom, x, y, fspath, dbname)
        if tile.is_empty():
            emptypath = color_scheme.get_empty_fspath(zoom)
            if not os.path.exists(os.path.dirname(fspath)):
                os.makedirs(os.path.dirname(fspath))
            os.symlink(emptypath,fspath)
        else:
            tile.rebuild()
            tile.save()

    return fspath
