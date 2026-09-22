#!/usr/bin/env python3
"""Compatibility entry point for the shared product showcase artwork.

Also preserves the original static-header paths for any existing consumers.
"""
from build_showcase_assets import ASSETS, header, main

if __name__ == '__main__':
    main()
    for theme in ('light', 'dark'):
        (ASSETS / f'profile-header-{theme}.svg').write_text(header(theme, True), encoding='utf-8')
