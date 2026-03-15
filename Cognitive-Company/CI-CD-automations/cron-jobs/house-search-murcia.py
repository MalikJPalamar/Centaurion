#!/usr/bin/env python3
"""
Murcia House Search - El Valle Golf Resort Area
Searches for houses within 15km radius with 6+ rooms, 300-600 sqm
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

def search_houses():
    """Search for houses in Murcia region near El Valle Golf Resort"""

    # Search criteria
    # Location: Murcia, El Valle Golf Resort area (approx coordinates: 37.85, -1.25)
    # We'll use idealista as the main source

    base_url = "https://www.idealista.com/search.htm"

    params = {
        "location": "Murcia",
        "maxPrice": "",
        "minSize": "300",
        "maxSize": "600",
        "numRooms": "6-mas",
        "dist": "15000",  # 15km radius
    }

    search_url = f"{base_url}?{urllib.parse.urlencode(params)}"

    results = {
        "date": datetime.now().isoformat(),
        "search_url": search_url,
        "criteria": {
            "location": "Murcia, El Valle Golf Resort area",
            "radius": "15 km",
            "min_rooms": 6,
            "min_size_sqm": 300,
            "max_size_sqm": 600
        },
        "listings": [],
        "notes": "Manual search recommended at: https://www.idealista.com/inmueble/es-*/?-dist=15000&location=El%20Valle%20Golf%20Resort&maxSize=600&minSize=300&numRooms=6-mas"
    }

    # Alternative: Rightmove style search
    results["alternative_searches"] = [
        {
            "site": "Idealista",
            "url": "https://www.idealista.com/inmueble/es-murcia/?dist=15000&maxSize=600&minSize=300&numRooms=6-mas"
        },
        {
            "site": "Fotocasa",
            "url": "https://www.fotocasa.es/es/comprar/viviendas/murcia/murcia/?minSurface=300&maxSurface=600&minRooms=6"
        },
        {
            "site": "Habitaclia",
            "url": "https://www.habitaclia.com/comprar/murcia/index.htm?superficieMax=600&superficieMin=300&habitacionesMin=6"
        },
        {
            "site": "Google Maps - El Valle Golf Resort",
            "url": "https://www.google.com/maps/search/golf+resort/@37.85,-1.25,14z"
        }
    ]

    return results

if __name__ == "__main__":
    print("=" * 60)
    print("Murcia House Search - El Valle Golf Resort Area")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    results = search_houses()

    print("Search Criteria:")
    print(f"  Location: {results['criteria']['location']}")
    print(f"  Radius: {results['criteria']['radius']}")
    print(f"  Rooms: {results['criteria']['min_rooms']}+")
    print(f"  Size: {results['criteria']['min_size_sqm']}-{results['criteria']['max_size_sqm']} sqm")
    print()
    print("Search Links:")
    for alt in results["alternative_searches"]:
        print(f"  {alt['site']}: {alt['url']}")
    print()
    print("=" * 60)
    print("Note: Automated scraping not available. Please use the search links above.")
    print("=" * 60)
