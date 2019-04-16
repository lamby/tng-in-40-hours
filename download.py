#!/usr/bin/env python3
#
# https://medium.com/maxistentialism-blog/star-trek-the-next-generation-in-40-hours-c4a6762cbd3
#
# Copyright (C) 2019  Chris Lamb <chris@chris-lamb.co.uk>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import re
import glob
import subprocess

re_filename = re.compile(r'^\s*(\d+)\|(.*)$')

HASH = "60eed4a0fd18fa7c475a7a8f1ce09505a59ca4ee"
TORRENT = '{}.torrent'.format(HASH)

MAGNET = "magnet:?xt=urn:btih:{}&dn=Star+Trek%3A+The+Next+Generation+-+Complete+Series+1080p&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969".format(HASH)

FILENAMES = {
    './Star Trek The Next Generation/Star Trek TNG Season 01/Star.Trek.The.Next.Generation.S01E01-S01E02.Encounter.At.Farpoint.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 01/Star.Trek.The.Next.Generation.S01E23.Skin.Of.Evil.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 01/Star.Trek.The.Next.Generation.S01E26.The.Neutral.Zone.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 02/Star.Trek.The.Next.Generation.S02E08.A.Matter.Of.Honor.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 02/Star.Trek.The.Next.Generation.S02E16.Q.Who.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 03/Star.Trek.The.Next.Generation.S03E10.The.DefectorS.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 03/Star.Trek.The.Next.Generation.S03E13.Deja.Q.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 03/Star.Trek.The.Next.Generation.S03E15.Yesterdays.Enterprise.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 03/Star.Trek.The.Next.Generation.S03E16.The.Offspring.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 03/Star.Trek.The.Next.Generation.S03E17.Sins.Of.The.Father.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 03/Star.Trek.The.Next.Generation.S03E26S04E01.The.Best.Of.Both.Worlds.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 04/Star.Trek.The.Next.Generation.S04E02.Family.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 04/Star.Trek.The.Next.Generation.S04E11.Datas.Day.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 04/Star.Trek.The.Next.Generation.S04E12.The.Wounded.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 04/Star.Trek.The.Next.Generation.S04E21.The.Drumhead.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 04/Star.Trek.The.Next.Generation.S04E26.Redemption.Part.1.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 05/Star.Trek.The.Next.Generation.S05E01.Redemption.Part.2.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 05/Star.Trek.The.Next.Generation.S05E02.Darmok.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 05/Star.Trek.The.Next.Generation.S05E03.Ensign.Ro.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 05/Star.Trek.The.Next.Generation.S05E05.Disaster.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 05/Star.Trek.The.Next.Generation.S05E06.The.Game.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 05/Star.Trek.The.Next.Generation.S05E18.Cause.And.Effect.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 05/Star.Trek.The.Next.Generation.S05E19.The.First.Duty.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 05/Star.Trek.The.Next.Generation.S05E23.I.Borg.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 05/Star.Trek.The.Next.Generation.S05E24.The.Next.Phase.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 05/Star.Trek.The.Next.Generation.S05E25.The.Inner.Light.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 05/Star.Trek.The.Next.Generation.S05E26.Times.Arrow.Part.1.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 06/Star.Trek.The.Next.Generation.S06E01.Times.Arrow.Part.2.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 06/Star.Trek.The.Next.Generation.S06E07.Rascals.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 06/Star.Trek.The.Next.Generation.S06E10.Chain.Of.Command.Part.1.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 06/Star.Trek.The.Next.Generation.S06E11.Chain.Of.Command.Part.2.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 06/Star.Trek.The.Next.Generation.S06E12.Ship.In.A.Bottle.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 06/Star.Trek.The.Next.Generation.S06E15.Tapestry.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 06/Star.Trek.The.Next.Generation.S06E20.The.Chase.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 06/Star.Trek.The.Next.Generation.S06E21.Frame.Of.Mind.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 06/Star.Trek.The.Next.Generation.S06E25.Timescape.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 06/Star.Trek.The.Next.Generation.S06E26.Descent.Part.1.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 07/Star.Trek.The.Next.Generation.S07E01.Descent.Part.2.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 07/Star.Trek.The.Next.Generation.S07E11.Parallels.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 07/Star.Trek.The.Next.Generation.S07E15.Lower.Decks.mp4',
    './Star Trek The Next Generation/Star Trek TNG Season 07/Star.Trek.The.Next.Generation.S07E25S07E26.All.Good.Things.mp4',
}

if not os.path.exists(TORRENT):
    subprocess.check_call((
        'aria2c',
        '--bt-metadata-only=true',
        '--bt-save-metadata=true',
        MAGNET,
    ))

output = subprocess.check_output((
    'aria2c',
    '--show-files',
    TORRENT,
)).decode('utf-8')

# Parse "index numbers" for files in .torrent
indexes = {}
for x in output.splitlines():
    m = re_filename.match(x)
    if m is not None:
        indexes[m.group(2)] = m.group(1)

# Filter to these episodes
to_download = {indexes[x] for x in FILENAMES}

# Perform the main download
subprocess.check_call((
    'aria2c',
    '--select-file={}'.format(','.join(sorted(to_download))),
    TORRENT,
))

# In multi file torrent, the adjacent files specified by this option may also be
# downloaded. This is by design, not a bug. A single piece may include several
# files or part of files, and aria2 writes the piece to the appropriate files.
#
#   -- <https://aria2.github.io/manual/en/html/aria2c.html#cmdoption-select-file>
#
for filename in glob.glob('./**/*.mp4', recursive=True):
    if filename not in FILENAMES:
        os.remove(filename)
