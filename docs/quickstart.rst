Quick Start
===========

Basic Usage
-----------

Extract GPS data from a GoPro video:

.. code-block:: python

   from gpmf import io, gps

   # Extract GPMF stream from video file
   stream = io.extract_gpmf_stream("GOPR0001.MP4")

   # Extract GPS blocks
   gps_blocks = list(gps.extract_gps_blocks(stream))

   # Parse GPS data from blocks
   for block in gps_blocks:
       gps_data = gps.parse_gps_block(block)
       print(f"Lat: {gps_data.latitude[0]:.6f}, Lon: {gps_data.longitude[0]:.6f}")

Export to GPX
-------------

Export GPS track to GPX format for use in Strava, Garmin Connect, etc.:

.. code-block:: python

   import gpxpy

   from gpmf import io, gps

   # Extract and parse GPS data
   stream = io.extract_gpmf_stream("GOPR0001.MP4")
   gps_blocks = [gps.parse_gps_block(b) for b in gps.extract_gps_blocks(stream)]

   # Create GPX
   gpx = gpxpy.gpx.GPX()
   track = gpxpy.gpx.GPXTrack()
   gpx.tracks.append(track)
   
   segment = gps.make_pgx_segment(gps_blocks)
   track.segments.append(segment)

   # Save to file
   with open("track.gpx", "w") as f:
       f.write(gpx.to_xml())

Visualize GPS Track
-------------------

Plot GPS track on an interactive map:

.. code-block:: python

   from gpmf import gps_plot, io

   # Extract stream
   stream = io.extract_gpmf_stream("GOPR0001.MP4")

   # Plot track on map
   gps_plot.plot_gps_trace_from_stream(
       stream, 
       output_file="gps_track.png",
       title="My GoPro Track"
   )

Command Line Interface
----------------------

Extract GPS data using the CLI:

.. code-block:: bash

   # Extract GPS to CSV
   python -m gpmf extract GOPR0001.MP4 --output gps_data.csv

   # Export to GPX
   python -m gpmf export GOPR0001.MP4 --format gpx --output track.gpx

   # Visualize track
   python -m gpmf plot GOPR0001.MP4 --output track.png
