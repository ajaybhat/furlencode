from time import sleep

__author__ = 'ajayb'
from subprocess import call
while True:
    call('curl http://ajaybhat.koding.io:5000',shell=True)
    sleep(2)