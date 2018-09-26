#!/usr/bin/python
"""
Script for starting web-application.
"""
import os

from skill.api.server import Server



def main():
    """
    Wrapper function for starting a server.
    """
    print('Starting server.')
    server = Server()
    
    workers = int(os.getenv('WORKERS', 1))
    server.run(host=os.getenv('HOST', '0.0.0.0'), access_log=True, workers=workers)

if __name__ == '__main__':
    main()
