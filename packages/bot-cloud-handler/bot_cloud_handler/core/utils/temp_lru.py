#
# Copyright (C) Halk-lai Liff <halkliff@pm.me> &
# Werberth Lins <werberth.lins@gmail.com>, 2022-present
#
# Distributed under Apache v2.0(2004) License, found at the root tree of
# this source, by the name of LICENSE
# You can also find a copy of this license at GNU's site, as it follows
# <https://www.apache.org/licenses/LICENSE-2.0>
#
# THIS SOFTWARE IS PRESENTED AS-IS, WITHOUT ANY WARRANTY, OR LIABILITY FROM ITS AUTHORS
# EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
# IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
# ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
#
# IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
# WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
# THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
# GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
# USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
# DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
# PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
# EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGES.
#

from collections import OrderedDict


__all__ = ["temp_lru_cache"]


class temp_lru_cache(dict):
    """
    A temporary, multi utility LRU Cache class to cache information temporarily in
    dicts. Different from the lru_cache decorators, this class is instantiated and is
    not meant to be used to cache function results to avoid extensive workloads;
    instead is served to cache dynamic information, like I/O info that can change
    overtime.
    """

    _data = OrderedDict()

    def __init__(self, max_size: int):
        self.max_size = max_size

    def __getitem__(self, key):
        item = self._data.get(key)
        if item is not None:
            self._data.move_to_end(key)
        return item

    def __setitem__(self, key, value):
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.max_size:
            self._data.popitem(last=False)

    def __delitem__(self, key):
        if key in self._data:
            del self._data[key]

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        return self.__setitem__(key, value)

    def __delattr__(self, item):
        return self.__delitem__(item)
