#! /usr/bin/python
#
# wuhong<wuhong@douban.com>
#
# python demo version of key-value store in memory
#

class pykv(Exception):

    def __init__(self):
        self.pdict = {}

    def set(self, key, val):
        self.pdict[key] = val
        return True
   
    def set_multi(self, kvdict):
        for key in kvdict.keys():
            self.set(key, kvdict[key])

    def get(self, key):
        return self.pdict.get(key)
    
    def get_multi(self, keylst):
        lst = []
        for key in keylst:
            lst.append(self.get(key))
        return lst
    
    # delta can be negative value 
    def incr(self, key, delta):
        if key not in self.pdict:
            return False
        try:
            self.pdict[key] += delta
        except:
            # not integer
            return False
        return True
    
    def gets(self, key):
        v = self.get(key)
        if v:
            return v, hash(repr(v))
    
    def cas(self, key, val, uniq):
        r = self.gets(key)
        if r:
            if uniq == r[1]:
                return self.set(key, val)
            else:
                return False

    def delete(self, key):
        if key in self.pdict:
            del self.pdict[key]

    def finalize(self):
        self.pdict.clear()

if __name__ == '__main__':
    kvdict = pykv()

    kvdict.set('hello', 'world')
    kvdict.set('key', 'value')
    print kvdict.get('hello')
    print kvdict.get('key')
    
    kvdict.delete('key')     
    print kvdict.get('key')

    val, uniq = kvdict.gets('hello')
    r = kvdict.cas('hello', 'kitty', uniq)
    
    # writing at same time
    while not r:
        val, uniq = kvdict.gets('hello')
        r = kvdict.cas('hello', 'mickey', uniq)

    print kvdict.get('hello')
    
    kvdict.set('python', 1)
    kvdict.incr('python', 3)
    kvdict.incr('python', -1)
    print kvdict.get('python')
    
    kvdict.finalize()