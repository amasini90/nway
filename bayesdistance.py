"""
Probabilistic Cross-Identification of Astronomical Sources

Reference: Budavari & Szalay (2008), ApJ, 679:301-309
Authors: Johannes Buchner (C) 2013
Authors: Tamas Budavari (C) 2012
"""

import numpy
from numpy import log, pi, exp, logical_and, where

log_arcsec2rad = log(3600 * 180 / pi)

def log_posterior(prior, log_bf):
	return -log( 1 + (1 - prior) * exp(-log_bf - log(prior)))

def posterior(prior, log_bf):
	return 1. / (1 + (1 - prior) * exp(-log_bf - log(prior)))

"""
Natural log of the 2-way Bayes factor, see eq.(16)
psi separation 
s1 and s2=accuracy of coordinates
"""
def log_bf2(psi, s1, s2):
	s = s1*s1 + s2*s2;
	return log(2) + 2 * log_arcsec2rad - log(s) - psi*psi / 2 / s

"""
Natural log of the 3-way Bayes factor, see eq.(17)
"""
def log_bf3(p12,p23,p31, s1,s2,s3):
	ss1 = s1*s1
	ss2 = s2*s2
	ss3 = s3*s3
	s = ss1*ss2 + ss2*ss3 + ss3*ss1
	q = ss3 * p12**2 + ss1 * p23**2 + ss2 * p31**2
	return log(4) + 4 * log_arcsec2rad - log(s) - q / 2 / s

"""
Natural log of the multi-way Bayes factor, see eq.(18)
"""
def log_bf(p, s):
	n = len(s)
	w = [numpy.asarray(si, dtype=numpy.float)**-2. for si in s]
	norm = (n-1) * log(2) + 2 * (n - 1) * log_arcsec2rad
	
	wsum = numpy.sum(w, axis=0)
	s = numpy.sum(log(w), axis=0) - log(wsum)
	q = 0
	for i, wi in enumerate(w):
		for j, wj in enumerate(w):
			if i < j:
				q += wi * wj * p[i][j]**2
	exponent = - q / 2 / wsum
	return norm + s + exponent

def test_log_bf():
	import numpy.testing as test
	sep = numpy.array([0., 0.1, 0.2, 0.3, 0.4, 0.5])
	for psi in sep:
		print psi
		print '  ', log_bf2(psi, 0.1, 0.2), 
		print '  ', log_bf([[None, psi]], [0.1, 0.2]), 
		test.assert_almost_equal(log_bf2(psi, 0.1, 0.2), log_bf([[None, psi]], [0.1, 0.2]))
	for psi in sep:
		print psi
		bf3 = log_bf3(psi, psi, psi, 0.1, 0.2, 0.3)
		print '  ', bf3
		g = log_bf([[None, psi, psi], [psi, None, psi], [psi, psi, None]], [0.1, 0.2, 0.3])
		print '  ', g
		test.assert_almost_equal(bf3, g)
	q = numpy.zeros(len(sep))
	print log_bf(numpy.array([[numpy.nan + sep, sep, sep], [sep, numpy.nan + sep, sep], [sep, sep, numpy.nan + sep]]), 
		[0.1 + q, 0.2 + q, 0.3 + q])


