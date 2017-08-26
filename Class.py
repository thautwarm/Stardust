#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 21:35:20 2017

@author: misakawa
"""

def _gettype(self, *protos):
    def _type(x):return x._class_
    _type.mro = []
    def get_proto_stream():
        yield self
        for proto in protos:
            yield from proto._class_.mro
    for proto in get_proto_stream():
        if proto in _type.mro:
            pass
        else:
            _type.mro.append(proto)
    return _type

def funcwrapper(self, obj):
    def _f(*args, **kwargs):
        return obj(self, *args, **kwargs)
    return _f

def _class(*protos, **_ignored):
    def _make_class(cls):
        def class_closure(*args, **kwargs):
            def inst_closure():pass
            for key in class_closure.__dict__:
                obj = class_closure.__dict__[key]
                if callable(obj) and not hasattr(obj, 'mro'):
                    setattr(inst_closure, key, funcwrapper(inst_closure, obj) )
                else:
                    setattr(inst_closure, key, obj)
            inst_closure._init_(*args, **kwargs)
            inst_closure._class_ = class_closure
            return inst_closure
        
        class_closure.__name__= cls.__name__
        class_closure._class_ = _gettype(class_closure, *protos)
        for proto in protos:
            for key in proto.__dict__:
                if key == '_class_':
                    continue
                class_closure.__dict__[key] = proto.__dict__[key]
        local_objs = cls()
        for key in local_objs:
            if key == '_class_':
                    continue
            class_closure.__dict__[key] = local_objs[key]
        return class_closure
    return _make_class

def _isinstance(x, A):
        return A in x._class_._class_.mro
    
@_class()
def cls1():
    def _init_(self, v):
        self.v = v
    def method(self, v):
        return self.v+v
    return locals()

@_class(cls1)
def cls2():
    def _init_(self, v):
        self.v = v
    def method(self, v):
        return self.v*v
    return locals()
