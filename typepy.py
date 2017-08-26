#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 17:29:00 2017

@author: misakawa
"""

class strict:
	@staticmethod
	def args(*typeargs : (*(),), **typekwargs:dict): 
	        def _1(func):
	            def _2(*args, **kwargs):
	                for arg_idx, (arg,typearg) in enumerate(zip(args, typeargs)):
	                    if not isinstance(arg,  typearg):
	                        raise TypeError(f"Type of argnument {arg_idx} should {typearg}")
	                for key in kwargs:
	                    if not isinstance(kwargs[key], typekwargs[key]):
	                        raise TypeError(f"Type of argnument  named {key} should {typekwargs[key]}")
	                return func(*args,**kwargs)
	            return _2
	        return _1
	    
	def ret(*typerets):
	        def _1(func):
	            def _2(*args, **kwargs):
	                ret = func(*args, **kwargs)
	                if len(typerets) > 1:
	                    for ret_idx,(ret_i, typeret) in enumerate(zip(ret, typerets)):
	                        if not isinstance(ret_i, typeret):
	                            raise TypeError(f"Type of return value {ret_idx} should {typeret}")
	                else:
	                    if not isinstance(ret, typerets[0]):
	                        raise TypeError(f"Type of return value should be {typerets[0]}")
	                return ret
	            return _2
	        return _1