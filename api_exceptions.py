"""
Stores dictionaries of all permalink exceptions I've found in the Ravelry API.

The Ravelry API appears to lack permalinks for the following categories: yarn weight, pattern source, pattern attributes (and all children).
While I have tried to match the permalinks of these categories to those on the website through .slugify(), there are several exceptions 
to the slugified forms. The slugified form is checked against these dictionaries to determine whether an exception exists for this parameter.

"""

exceptions_categories = {'any-gauge' : 'any', 'pamphlet' : 'booklet', 'ebook' : 'eBook'}

exceptions_attributes = {'adaptive-design' : 'adaptive', 'medical-device-support' : 'medical-device-accessory', 
                         'mobility-aid-support' : 'mobility-aid-accessory', 'intarsia': 'Intarsia', 'double-knitting' : 'doubleknit',
                         'provisional-cast-on' : 'provisional', 'three-needle-bind-off' : 'three-needle-bind', 'twined-knitting' : 'twined',
                         'worked-in-the-round' : 'in-the-round', 'broomstick-crochet' : 'broomstick', 'bruges-crochet' : 'bruges',
                         'clones-knot' : 'clones', 'cro-hook' : 'crohook', 'cro-tatting' : 'crotat', 'front' : 'post-stitch',
                         'lovers-knot' : 'lovers', 'pineapple-crochet' : 'pineapple', 'slip-stitch-crochet' : 'slip-stitch',
                         'back-fastening' : 'backfastening', 'braids' : 'braids-plaiting', 'double-breasted' : 'doublebreasted',
                         'empire-waist' : 'empire', 'racer-back' : 'racerback', 'waist-shaping' : 'waist', 'collared' : 'collar',
                         'peter-pan' : 'peterpan', 'shawl-collar' : 'shawl', 'shirt' : 'shirt-collar', 'halter' : 'halter-neck', 
                         'henley' : 'henley-neck', 'mock-turtle' : 'mock-turtleneck', 'surplice' : 'surplice-neck', 'turtle-neck' : 'turtleneck',
                         'any-pockets' : 'pockets', 'hidden' : 'hidden-pocket', 'patch' : 'patch-pocket', 'set-in' : 'set-in-pocket',
                         'tubular' : 'tubular-pocket', '3' : '3-4-sleeve', 'nalgar-ez-notation' : 'nalgar-sleeve', 'any-sleeves' : 'sleeves',
                         'bracelet-length' : 'bracelet-sleeve', 'cap' : 'cap-sleeve', 'cuffed' : 'cuffed-sleeve', 'drop' : 'drop-sleeve',
                         'elbow' : 'elbow-sleeve', 'flutter' : 'flutter-sleeve', 'long' : 'long-sleeve', 'modified-drop' : 'modified-drop-sleeve',
                         'puffed' : 'puffed-sleeve', 'raglan' : 'raglan-sleeve', 'set-in' : 'set-in-sleeve', 'short' : 'short-sleeve',
                         'tulip' : 'tulip-sleeve', 'dolman' : 'dolman-sleeve', 'bobble' : 'bobble-or-popcorn', 'brioche' : 'brioche-tuck',
                         'mature-content' : 'mature', 'has-schematic' : 'schematic', 'photo-tutorial' : 'phototutorial', 
                         'recipe---percentage' : 'pattern-recipe', 'screen-reader-access' : 'screen-reader', 'cowichan-salish' : 'cowichan',
                         'fair-isle' : 'fairisle', 'shetland' : 'Shetland', 'circle' : 'circle-shaped', 'crescent' : 'crescent-shape',
                         'cube' : 'cube-shaped', 'half-circle' : 'halfcircle-shape', 'pentagon' : 'pentagon-shape', 'sphere' : 'sphere-shaped',
                         'star' : 'star-shaped', 'triangle' : 'triangle-shaped', 'no-shaping' : 'noshaping', 'starting-in-middle' : 'start-in-middle',
                         'top' : 'top-cuff-down', 'crochet' : 'crochet-techniques', 'two-at-a-time' : '2-at-a-time', 'wide' : 'wide-toe'}

exceptions_fit = {'child-4-12' : 'child', 'teen-13-17' : 'teen', 'doll' : 'doll-size', 'toddler-1-3' : 'toddler', 'newborn' : 'newborn-size',
                   'maternity-fit' : 'maternity', 'oversized-fit' : 'oversized','petite-fit' : 'petite', 'plus-fit' : 'plus', 'tall-fit' : 'tall'}