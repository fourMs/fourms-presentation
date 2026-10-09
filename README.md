# fourMs Lab presentation

A generic presentation of the fourMs Lab (Music, Mind, Motion, Machines) at the University of Oslo, a lab for artistic and scientific research on music, mind, motion and machines and a national research infrastructure, the central lab of RITMO, the Centre for Interdisciplinary Studies in Rhythm, Time and Motion. Built with [reveal.js](https://revealjs.com/) 5, vendored in `lib/`.

Open `index.html` in a browser, or serve the folder and open it there. Right moves to the next question, down goes deeper. `S` opens the speaker notes, which carry the detail; `D` toggles dark mode. Add `?venue=…&date=…` to the address to put the occasion on the title slide.

## Structure

The deck follows a set of questions, each a vertical stack: Why? What? How? Who?, then MusicLab and the Norwegian Championship of Standstill, Learn?, When? and Next?. The top slide of each stack is enough for a short talk; the slides below go deeper.

## Content and numbers

The content comes from the lab's public web pages (fourms.uio.no), MusicLab's (musiclab.uio.no), RITMO's annual reports and final report, and the lab's description of itself from 2020. Every number on the slides is generated, and so is the equipment list (`data/equipment.tsv`, from the lab's two equipment pages): `tools/make_numbers.py` writes `js/numbers.js` from `data/facts.tsv`, where each row names its source, counts the MusicLab events in the final report's list of events, and counts the Oslo Standstill Database (recordings, collections, years) in the harmonised measures table of the Still Standing book project. The user numbers are from 2020 and are labelled so.

`tools/make_figures.py` copies the photographs from the RITMO and fourMs photo archive, the annual reports and an earlier fourMs Lab introduction deck, and draws the history timeline from `data/history.tsv`. The fourMs logo and its light-trace image are in `logo/`, with the UiO logo and the RITMO emblem.

## Visual profile

The colours of the fourMs logo: orange-red `#B22309`, light green `#9FD54F` and yellow `#F2DF30` on a warm near-black `#130102`, with the deep red of the logo's tagline `#961C07` for text. Green and yellow are fills, never text on white.

## Build a PDF

    python3 -m venv .venv && .venv/bin/pip install -r tools/requirements.txt
    .venv/bin/python tools/build_pdf.py --venue Oslo --date "1 January 2027"

The PDF is made of screenshots from headless Chrome, so it has no text layer.

## Credits

Photographs from RITMO's and the fourMs Lab's photo archives and from RITMO's published annual reports. Built with reveal.js (MIT licence).
