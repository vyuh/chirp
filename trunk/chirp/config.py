"""
Copyright (c) 2007-2009 Egor Pomortsev <illicium@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import ConfigParser, os

class ChirpConfig:
    CONFIG_FILE = '~/.config/chirp/chirp.conf'
    DEFAULTS = {
        # [appearance]
        'list_striped': 'no',
        'avatar_rounded': 'true',
        'avatar_size': 'large',
        'format': '<b>$username</b>\n$message'
    }

    def __init__(self):
        self.config = ConfigParser.SafeConfigParser(self.DEFAULTS)
        self.config.read(os.path.expanduser(self.CONFIG_FILE))

    def get(self, section, option, type=None):
        try:
            if not self.config.has_section(section): section = 'DEFAULT'

            if type == int:
                return self.config.getint(section, option)
            elif type == float:
                return self.config.getfloat(section, option)
            elif type == bool:
                return self.config.getboolean(section, option)
            else:
                return self.config.get(section, option)
        except:
            return None

    def getAvatarPixelSize(self):
        setting = self.get('appearance', 'avatar_size')
        if setting == 'tiny':
            return 16
        elif setting == 'small':
            return 24
        elif setting == 'large':
            return 48
        else:
            return -1
