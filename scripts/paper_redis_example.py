#!/usr/bin/env python
"""
List data available in redis
"""

import redis as redis_lib
import numpy as np
import matplotlib as mpl
import argparse

parser = argparse.ArgumentParser(description='List data available in redis')

args = parser.parse_args()

redis = redis_lib.Redis('redishost')

keys = redis.keys()

# alphabetize
keys.sort()

print '#######################'
print '# All the keys!       #'
print '#######################'
for key in keys:
  print key,
  try:
    # some of the items in redis are hash tables:
    print redis.hkeys(key)
  except:
    # others are just values
    print redis.get(key)

print '#############################'
print '# An example visdata entry  #'
print '#############################'
# visdata are autocorrelations, stored in hashes with 'time' and 'data' entries
print 'visdata://22/22/xx:'
visdata = redis.hgetall('visdata://22/22/xx')
print 'time:', visdata['time']
# the data are stored as binary dumps
print 'data:', np.fromstring(visdata['data'], dtype=np.float32)

# hashpipe status buffers are also hashes, with all kinds of keys
print '#############################'
print '# An example hashpipe entry #'
print '#############################'
print 'hashpipe://px4/0/status'
hashpipestatus = redis.hgetall('hashpipe://px4/0/status')
# all the entries in this dictionary are strings, so convert as necessary
for key, val in hashpipestatus.iteritems():
  print '%10s:'%key, val

# There also appear to be an entry for the ROACH F-engine sync time
print '#############################'
print '# F-engine sync time        #'
print '#############################'
feng_init = redis.get('roachf_init_time')
print 'roachf_init_time:', feng_init, type(feng_init)

# and finally a key for 
print '#############################'
print '# paper_redis_monitor       #'
print '#############################'
monitor = redis.hgetall('paper_redis_monitor://status')
# this hash has a timestamp entry, and a generic message'
for key, val in monitor.iteritems():
  print '%10s:'%key, val
  print '---'


# Write something new to redis!
redis.set('fake_key', 'fake_value')
# or write a hash
redis.hset('fake_hash', 'fake_key_in_hash', 'fake_value')

