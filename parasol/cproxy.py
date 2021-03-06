import inspect
import msgpack as mp

class cproxy(Exception):

    def __init__(self, fd):
        self.fd = fd
    
    def glue(self, opname, *args):
        sop = mp.packb(opname)
        spara = ''
        for arg in args:
            spara += mp.packb(arg)
            spara += 'parasol'
        result = ''
        result = result.join([sop, 'parasol', spara, mp.packb('0')])
        return result
        
    def push(self, key, val):
        return self.glue('push', key, val)
    
    def push_multi(self, kvdict):
        return self.glue('push_multi', kvdict)
         
    def pull(self, key):
        return self.glue('pull', key)

    def pull_multi(self, keylst):
        return self.glue('pull_multi', keylst)
	
    def update(self, key, delta, func = ''):
        import sys
	self.self_flag = False
        def compact(s):
	    return s.strip(' ').strip('\t').replace(', ', ',').replace('self,', '')
	
	def check_legal(f):
	    import types
	    if inspect.getsource(f).find('self') != -1:
	        self.self_flag = True
	    def check_name(f):
	        return f.__name__ in ('accumulator', '<lambda>')
	    
	    def check_api(f):
	        nargs = len(inspect.getargspec(f).args)
	        if self.self_flag:
		    return nargs == 3
		else:
		    return nargs == 2
	    return check_name(f) and check_api(f)

        if func:
	    if not check_legal(func):
	        print 'Error in defining accumulator function.\n' \
		'Func fmt: accumulator(val, delta)'
		sys.exit(1)
	    funcstr = inspect.getsource(func)
	    fs = compact(funcstr)
	    return self.glue('update', key, delta, fs)
        return self.glue('inc', key, delta)
        
    def pushs(self, key):
        return self.glue('pushs', key)
        
    def pulls(self, key, val, uniq):
        return self.glue('pulls', key, val, uniq)
        
    def remove(self, key):
        return self.glue('remove', key)
        
    def clear(self):
        return self.glue('clear')        

    def pullall(self):
        return self.glue('pullall')

