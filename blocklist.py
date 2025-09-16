"""
blocklist.py

This file just contains the blocklist of the JWT token.
It will be imported by app and the logout resource 
so that tokens can be added to blocklist when the user logs out.
"""

BLOCKLIST = set() #### Use DB later