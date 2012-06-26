#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# utilities.py
#
# purpose:  Some handy functions used throughout this package.
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.tiddlyspot.com/
# created:  22-Jun-2011
# modified: Tue 26 Jun 2012 04:44:08 PM BRT
#
# obs:
#

import numpy as np


class match_args_return(object):
    r"""Function decorator to homogenize input arguments and to make the output
    match the original input with respect to scalar versus array, and masked
    versus ndarray."""

    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__
        self.__name__ = func.__name__

    def __call__(self, *args, **kw):
        # Check if is array
        self.array = np.any([hasattr(a, '__iter__') for a in args])

        # Check if is masked
        self.masked = np.any([np.ma.isMaskedArray(a) for a in args])
        newargs = [np.ma.atleast_1d(np.ma.masked_invalid(a)) for a in args]
        newargs = [a.astype(np.float) for a in newargs]
        ret = self.func(*newargs, **kw)
        if not self.masked:  # Return a filled array if not masked.
            ret = np.ma.filled(ret, np.nan)
        if not self.array:  # Return scalar if not array.
            ret = ret[0]

        return ret
