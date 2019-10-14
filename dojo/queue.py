import os
import pickle
import fcntl
import logging

from dojo.utils import logger
from dojo.constants import QUEUE_PATH


class SimpleQueue(object):
    """A Simple Queue structure
    
    It works by persisting, reading and writing items on a file through file descriptors' built-in interfaces and OS derived APIs
    
    For now it's limited by python's GIL and doesn't use any sort of
    multi-processing nor concurrency routines
    """
    def __init__(self, append=True):
        if not append and os.path.exists(QUEUE_PATH):
            os.remove(QUEUE_PATH)
        
        self.queue = []
        self._ensure_persistance()
        
    def __repr__(self):
        """Queue representation
        
        Built-in method override"""
        print(self._deserialize_list())
        
    def __str__(self):
        """Queue as string
        
        Built-in method override"""
        return self.__repr__()

    def _ensure_persistance(self):
        """Creates queue file
        
        If it doesn't exists already"""
        
        if not os.path.exists(QUEUE_PATH):
            with open(QUEUE_PATH, 'wb') as f:
                pickle.dump(self.queue, f, 0)
                
    def _lock_file(self, f):
        """Locks queue file
        
        fnctl is a Linux utility to manage file descriptors"""
        fcntl.flock(f, fcntl.LOCK_EX)
        
    def _unlock_file(self, f):
        """Unlocks queue file
        
        fnctl is a Linux utility to manage file descriptors"""
        f.flush()
        os.fsync(f.fileno())
        fcntl.flock(f, fcntl.LOCK_UN)
            
    def _deserialize_list(self):
        """Serialize queue file contents back into memory"""
        fd = open(QUEUE_PATH, 'rb')
        content = None
        self._lock_file(fd)
        try:
            content =  pickle.load(fd)
        except EOFError as ex:
            logger.error(ex)
            pass
            
        self._unlock_file(fd)
        fd.close()
        return content
        
    def _serialize_list(self):
        """De-serialize queue memory contents back to queue file"""
        fd = open(QUEUE_PATH, 'wb')
        self._lock_file(fd)
        pickle.dump(self.queue, fd, 0)
        self._unlock_file(fd)
        fd.close()
            
    def enqueue(self, item):
        """Puts a new item on queue"""
        read_obj = self._deserialize_list()
        if isinstance(self.queue, list):
            self.queue = read_obj
            try:
                self.queue.append(item)
            except AttributeError as ex:
                # persistance can write empty list as None
                logger.warning(ex)
                self.queue = []
                self.queue.append(item)
            finally:
                self._serialize_list()
    
    def dequeue(self):
        """Pops first (and oldest) item from queue
        
        If queue is empty, an empty list is returned"""
        read_obj = self._deserialize_list()
        
        if isinstance(self.queue, list):
            self.queue = read_obj
            try:
                item = self.queue.pop(0)
            except (IndexError, AttributeError) as ex:
                # empty queue
                logger.warning(ex)
                return []
            else:
                self._serialize_list()
                return item