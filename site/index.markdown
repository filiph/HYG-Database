---
layout: minimal
title: Star Map 2D
description: "Star Map 2D is a self-organizing map of 5000 known stars closest to Sol."
---

# Star Map 2D <small>// A self-organizing map of 5000 closest stars</small>

<!-- <h1><img src="img/egamebook-title.png" alt="Egamebook" /></h1> -->
<!-- <img class="book" src="img/book-illustration.jpg" alt="Illustration of a book" /> -->

<div class="right-tooth">

<ul class="choices">
	<li class="button preferred"><a href="#download"><strong>Download</strong> the map (0.1)</a></li>
	<li class="button"><a href="#gallery">See the gallery</a></li>
	<li class="button"><a href="#">Show code on GitHub</a></li>
</ul>

<p class="nav">
	<a href="#specifications">Specifications</a>
	<a href="#cc-license">CC License</a>
	<a href="#contact">Contact</a>
</p>
<!-- 	<picture>
	  <source media="(min-width: 32em)" srcset="img/vertical-large.jpg">
	  <img src="img/vertical-small.jpg" alt="A screenshot of an obfuscated view from the Digital Universe software package." />
	</picture> -->
</div>

Our sci-fi books, movies and games are filled with exploration of the galaxy and the universe at large. It's all _planet this_ and _star system that_, and how many parsecs between them.

**But notice one thing:** those places are either completely made up[^1] or they are random stars taken from our night sky without any context.[^2]

[^1]: For example: most Star Trek's star systems (such as [Kaldra][]) or most Doctor Who's star systems (such as [4-X-Alpha-4][]). 
[^2]: For example [Arrakis][] is supposed to be orbiting Canopus, or [Whistle Stop][] is supposedly in the Nu Phoenicis star system. Those are real stars, yes, but they're only there for the sake of verisimilitude. In other words, those star systems were probably picked solely based on having cool sounding names and being in the star atlas. Briefly looking at [planets from Frank Herbert's Dune][Dune planets], it looks like they're all over the place – it's probably safe to say Frank Herbert didn't try to create a coherent topology of his fictional universe. Nor did almost anyone else. Because it's _hard_.

[Kaldra]: http://en.wikipedia.org/wiki/List_of_Star_Trek_planets_(G%E2%80%93L)
[4-X-Alpha-4]: http://en.wikipedia.org/wiki/List_of_Doctor_Who_planets
[Arrakis]: http://en.wikipedia.org/wiki/Arrakis
[Whistle Stop]: http://en.wikipedia.org/wiki/List_of_Heinlein_planets#Time_for_the_Stars
[Dune planets]: http://en.wikipedia.org/wiki/List_of_Dune_planets

The reason is that most people (including writers, screenwriters and game masters) _don't actually have any idea what the topology of our star neighbourhood is like._ The three dimensions are super confusing. Is Sirius close to Mirzam? They _are_ on the night sky (Mirzam is a bright star right next to Sirius) but they are most definitely _not_ in 3D space (Sirius is 9 light years away, Mirzam is 500).[^3]

[^3]: That's just one example out of thousands. You probably know that Proxima Centauri is the closest star to Sol – but do you know many other pairs of stars that are close to each other? Okay, you probably know that Proxima Centauri is closest to Alpha and Beta Centauri. But then? What are the stars closest to Sirius, for example?

<figure class="right-tooth">
	<a href="img/digital-universe-orig.png">
		<picture>
		  <source media="(min-width: 32em)" srcset="img/digital-universe-large.jpg">
		  <img src="img/digital-universe-large.jpg" alt="A screenshot of an obfuscated view from the Digital Universe software package.">
		</picture>
	</a>
	<figcaption>Digital Universe does an excellent job in letting you navigate the universe in 3D – but it's still very hard to do things that would be simple on a 2D map.</figcaption>
</figure>

Even if you have a 3D atlas of stars which allows you to travel freely through virtual space, like [Digital Universe][] or [Redshift][], that experience is no less confusing. Humans are not good at navigating through _true_ three-dimensional space.[^4] Even simple things like trying to find clusters of stars are extremely difficult.

[^4]: By 'true three-dimensional space' I mean space that is similar in all directions. Of course humans live in 3D, but in practice, we mostly inhabit a plane (Earth's surface). Of the 3 dimensions, one is much less navigable than the other two (we can't easily fly, our buidlings are made of flat floors, etc.). See [2D is Better Than 3D][] by Jakob Nielsen.

[2D is Better Than 3D]: http://www.nngroup.com/articles/2d-is-better-than-3d/

[Digital Universe]: http://www.amnh.org/our-research/hayden-planetarium/digital-universe/
[Redshift]: https://itunes.apple.com/en/app/redshift-astronomy/id390436752?mt=8

Compare this to a traditional (2D) map. It's very easy for us humans to see that two cities are close to each other, for example. At a glance, we can see clusters, gaps, strings, and so on. We can plan and reason about the map.

## The problem of 2D star maps

There are 2D star maps already, of course – [Winchell D. Chung's maps][Winchell maps] being probably the best examples. So why make another?

[Winchell maps]: http://www.projectrho.com/public_html/starmaps/mapindex.php

The problem is that the currently available 2D maps are _views_. They show each star at its proper X and Y coordinates, but they completely discard the Z (depth) coordinate. In this respect they are almost as bad a representation of reality as the night sky. Two adjancent stars are often actually quite far from each other – but the viewer doesn't know this until after they _read_ that information.[^5]

[^5]: These maps often have a small number next to each star that gives its Z coordinate. The viewer needs to pay very close attention to these numbers all the time.

<figure class="right-tooth">
	<a href="http://en.wikipedia.org/wiki/Sun#mediaviewer/File:The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg">
		<picture>
		  <source media="(min-width: 32em)" srcset="img/sun-large.jpg">
		  <img src="img/sun-small.jpg" alt="An image of the Sun.">
		</picture>
	</a>
<!-- 	<figcaption>The Sun, also known as Sol. (Image by NASA Solar Dynamics Observatory.)</figcaption> -->
</figure>

So again, similarly to 3D virtual atlases, with 2D views it's not easy to do basic things at a glance. 

## The perfect map

It's obvious that _any_ 2D map of 3D space will be imperfect. But we can still do better than a view. Let these be our goals for the map:

* Instances of outright lies (for example, Sirius and Mirzam rendered next to each other) are minimized.
* It is possible to make basic observations about the depicted stars at a glance, with a reasonable level of certainty. For example:
	* Identify clusters of stars.
	* See if star is solitary (no close neighbours).
	* See what stars are neighbouring any given star.
* If star C is three times farther away from star B than star A in space, we want to see the same thing on the map.[^6] 

[^6]: This is our fitness function. Let's pick random stars A, B and C. Compute distance from A to B in 3D space (<em>a<sub>3d</sub></em>) and on the 2D map (<em>a<sub>2d</sub></em>). Do the same for B to C, for both 3D (<em>b<sub>3d</sub></em>) and 2D (<em>b<sub>2d</sub></em>). The goal is to minimize the difference between the ratios <em>a<sub>3d</sub>/b<sub>3d</sub></em> and <em>a<sub>2d</sub>/b<sub>2d</sub></em>.

Note also what _isn't_ our goal here: perfect representation of 3D space on a 2D map. We are trying to minimize the distortion but we can't _ever_ hope to get rid of it completely. 

## Enter Teuvo Kohonen

But even when we limit our goals and recognize that the map can't be perfect, it's very hard to create a suitable map for even a few stars, and virtually _impossible_ to do so for thousands of them&hellip;

<p class="scream">&hellip; UNLESS YOU HAVE THINKING MACHINES THAT CAN DO THE WORK FOR YOU.</p>

Which we have. Thanks to the amazing thing that is general purpose computing, and thanks to a particularly clever algorithm by the Finnish academician [Teuvo Kohonen][], we can leave the work to the machines.

<figure class="right-tooth">
	<a href="http://en.wikipedia.org/wiki/Self-organizing_map#mediaviewer/File:Synapse_Self-Organizing_Map.png">
		<picture>
		  <source media="(min-width: 32em)" srcset="img/synapse-large.png">
		  <img src="img/synapse-small.png" alt="A screenshot of 20 heatmaps of a single self-organizing map."> <!-- TODO: convert to JPG -->
		</picture>
	</a>
	<figcaption>A classic application of a self-organizing map is in combination with heatmaps.</figcaption>
</figure>

A [self-organizing map][] is an artificial neural network that learns to represent multi-dimensional data on a (usually 2D) map. It can be used to analyze huge data tables – for example, a university's students can be plotted on a self-organizing map according to their grades in different courses. Such a map can then help in finding students with similar strengths and weaknesses.

[Teuvo Kohonen]: http://en.wikipedia.org/wiki/Teuvo_Kohonen
[self-organizing map]: http://en.wikipedia.org/wiki/Self-organizing_map

Turns out a star's 3D coordinates can be seen as multi-dimensional data. Because that's exactly what they are. :)

I simply applied a well-documented algorithm to an obvious-in-retrospect dataset.

Of course, it wasn't that simple to actually arrive to something usable. It took me 5 months to arrive at the winning formula[^7] – there are many parameters that have to be chosen by experimentation, and every training of such a large Kohonen network takes anything from half a day to more than a _month_ of continuous CPU usage.

[^7]: Weekends and evenings, April to August 2014.

## Specifications

* The map consists of **848x600 hexagonal tiles**.
	* The aspect ratio is &radic;<span style="text-decoration:overline">2</span>:1,[^8] same as the international paper size A standard (A4, A3, A2, etc.).
* The map is **toroidal** ('wrap around').
  * In other words, opposite edges of the map are connected. This means that, for example, 'going through' the top edge 'teleports' you to the bottom. If you remember the game Asteroids, you probably know what I mean.
  * The reason for this is because it is easier for the 2D self-organizing map to be weaved through the 3D space if it's toroidal, which means less distortion.
* There are exactly **5000 stars** on the map.
	* They are Sol (the Sun) and the 4999 known stars closest to it from David Nash's [HYG Database][]. 
	* It's a sphere of stars 72 light years in diameter, with Sol at its center.
* One light year in space is _approximately_ **8 hexes** on the map.[^9]
	* In other words, one hex is around 0.125 light years.
* Legend:
	* Stars are **color-coded** by [spectral type][]. 
	* The **size** of a star on the map corresponds to its [absolute magnitude][] – larger is brighter.
	* Stars with a **little green dot** next to them are candidates to have a habitable, Earth-like planet on their orbit.[^10]

[^8]: This means that if you cut the map in half, the resulting map's aspect ratio will again be &radic;<span style="text-decoration:overline">2</span>:1.
[^9]: This number was arrived at by getting ratios between 2D and 3D distances of nearby (<5 light years) stars and by looking at the mean and median, and at the histogram of these values. By looking at mean alone (0.166) the result would be 1 light year per 6 hexes. But I went for median/modus (0.130/0.12) because I wanted the calculation to be accurate in as many cases as possible (as opposed to being accurate on average but very inaccurate in most cases). Please keep in mind this is only a rough approximation and should not be taken too seriously given the nature of the map. Also, it works better on stars that are relatively close to each other (which is also by design).
[^10]: This idea is taken from the aforementioned maps by Winchell Chung. The underlying data is provided by _[HabCat][]: A Catalog of Nearby Habitable Systems_ by Jill Tarter and Margaret Turnbull.

[HYG Database]: http://www.astronexus.com/hyg
[HabCat]: http://phl.upr.edu/projects/habcat
[spectral type]: http://hyperphysics.phy-astr.gsu.edu/hbase/starlog/staspe.html
[absolute magnitude]: http://en.wikipedia.org/wiki/Absolute_magnitude

## Gallery

<figure class="full-width">
	<a href="img/sol-screenshot.gif">
		<picture>
		  <img src="img/sol-screenshot.gif" alt="Screenshot of Sol's neigbourhood.">
		</picture>
	</a>
	<figcaption>Sol (our home star) and the 3 closest stars. You can see that while Sol has the little green planet beside it, the other star systems don't. This means it doesn't look like those star systems have a habitable, Earth-like planet.</figcaption>
</figure>

<figure class="full-width">
	<a href="img/12-13-Mu-XIII.png">
		<picture>
		  <img src="img/12-13-Mu-XIII-x1.gif" srcset="img/12-13-Mu-XIII-x1.gif 1x, img/12-13-Mu-XIII-x2.gif 2x, img/12-13-Mu-XIII-x4.gif 4x" alt="Screenshot of the whole Mu-XIII sector."/>
		</picture>
	</a>
	<figcaption>The whole Mu-XIII sector. (Click for bigger.) Note the little links at the edges of the map – they tell you which sector is neighboring on that side.</figcaption>
</figure>

<!-- <figure class="full-width">
	<a href="img/10-13-Kappa-XIII.png">
		<picture>
		  <img src="img/10-13-Kappa-XIII-x1.gif" srcset="img/10-13-Kappa-XIII-x1.gif 1x, img/10-13-Kappa-XIII-x2.gif 2x" alt="Screenshot of an area around Altair."/>
		</picture>
	</a>
	<figcaption>Looks like there is a potentially habitable star system not far from the otherwise solitary Altair.</figcaption>
</figure> -->

## Download

Both download types below include <del>an overview map (PDF)</del> <span class="warning">NOT AVAILABLE YET</span>, all the 576 sectors (PDFs), an index of the more well-known stars, and <del>a CSV file with all the data</del> <span class="warning">NOT AVAILABLE YET</span>.

* **'Scientific' bundle** <span class="warning">NOT AVAILABLE YET</span>
	* Stars are labeled by their standard catalogue codes (for example: HIP 89937) or by a very commonly used name if available (for example: Barnard's star). This makes it very easy to research each star on astrological databases such as [Simbad][]. This also makes the map pretty boring.
	* Also includes an index of all the 5000 stars.
* [**'Literary' bundle** (v1.1, 20MB, zip)][latestLiterary]
	* Stars are either labeled by a proper name or by a constellation-based name (for example: Chi Draconis). If none of those two is available, a cool-sounding catalogue code[^11] is chosen over a more commonly used one (for example: STU 10B is chosen over HIP 86162).

[latestLiterary]: /download/2d-star-map-v1.1-literary.zip

The PDF files do _not_ contain the font (Input Sans Condensed) that you see in the screenshots above. You can [download the font here][inputfont] (free for personal use).

[inputfont]: http://input.fontbureau.com/

<figure class="right-tooth">
		<picture>
		  <img src="img/bodega_04_WIP.jpg" alt="An artist rendering of a spaceship.">
		</picture>
<!-- 	<figcaption>Bodega.</figcaption> -->
</figure>

If you want to see or play around with the source, go to the GitHub repository.

[^11]: Those are picked from [Simbad][]'s _Identifiers_ section by a simple algorithm which prefers shorter names and letters before numbers. You should still be able to find the star behind the name but for example in Simbad sometimes you'll need to prepend '\*' or '\*\*' before the designation (STU 10B is [\*\* STU 10B][STU 10B] in Simbad).

[Simbad]: http://simbad.u-strasbg.fr/simbad/sim-fid
[STU 10B]: http://simbad.u-strasbg.fr/simbad/sim-basic?Ident=**+STU+10B

## What to do with this?

Wouldn't it be nice to see a fictional empire, federation, space-faring nation or civilization that inhabits stars that are actually close to each other? If you're writing a book, screenwriting, creating a game or running a role-playing adventure set in space, consider using the map. (I'd be thrilled if you tell me.)

This was, by the way, my original motivation for creating the 2D Star Map in the first place. I am using this for my gamebook / free exploration game called _The Bodega Incident_. You can learn more about that project at [egamebook.com][].

[egamebook.com]: http://egamebook.com/

If you're a (hobby) astronomer, you might like the idea of seeing stars in their context without having to fire up 3D software every time.

**Suggested use:** 

1. **Pick** a star and find out which sector it is in.
	* Or, just pick a sector randomly.
2. **Print** out the sector and it's neighbours.
	* Based on the epicness of your project, you can print out just 1, or four, or 16 papers.
3. **Arrange** them on the table.
	* The little notes on the sides are a hint for you about what comes where.
	* Keep in mind that each page has a 1-hex border at each side that belongs to the neighbouring sector.
4. Start planning your galactic conquest (or whatever else it is you're doing).


## Index of well-known stars

| Star name                 | X, Y     | Sector                 |
|---------------------------|----------|------------------------|
| 268 G. Cet                | 425, 275 | Mu-XII [12:12]         |
| 33 G. Lib                 | 51, 565  | Beta-XXIII [2:23]      |
| 82 G. Eri                 | 798, 44  | Psi-II [23:2]          |
| 96 G. Psc                 | 380, 275 | Lambda-XII [11:12]     |
| Aldebaran                 | 563, 144 | Pi-VI [16:6]           |
| Alderamin                 | 379, 559 | Lambda-XXIII [11:23]   |
| Algol                     | 485, 84  | Xi-IV [14:4]           |
| Alhena                    | 615, 96  | Sigma-IV [18:4]        |
| Alioth                    | 473, 480 | Xi-XX [14:20]          |
| Alkaid                    | 450, 468 | Nu-XIX [13:19]         |
| Alnair                    | 120, 217 | Delta-IX [4:9]         |
| Alphekka                  | 351, 439 | Kappa-XVIII [10:18]    |
| Alpheratz                 | 340, 85  | Kappa-IV [10:4]        |
| Altair                    | 348, 317 | Kappa-XIII [10:13]     |
| Ankaa                     | 105, 149 | Gamma-VI [3:6]         |
| Arcturus                  | 424, 382 | Mu-XVI [12:16]         |
| Barnard's Star            | 393, 318 | Lambda-XIII [11:13]    |
| Capella                   | 521, 25  | Omicron-II [15:2]      |
| Caph                      | 411, 11  | Mu-I [12:1]            |
| Castor                    | 632, 9   | Sigma-I [18:1]         |
| Denebola                  | 511, 368 | Omicron-XV [15:15]     |
| Diphda                    | 166, 139 | Epsilon-VI [5:6]       |
| Fomalhaut                 | 109, 21  | Delta-I [4:1]          |
| Groombridge 1618          | 458, 326 | Nu-XIV [13:14]         |
| Groombridge 1830          | 478, 358 | Xi-XV [14:15]          |
| Hamal                     | 427, 127 | Mu-VI [12:6]           |
| Kapteyn's Star            | 784, 32  | Chi-II [22:2]          |
| Kruger 60                 | 399, 310 | Mu-XIII [12:13]        |
| Lacaille 8760             | 89, 597  | Gamma-XXIV [3:24]      |
| Lacaille 9352             | 378, 300 | Lambda-XIII [11:13]    |
| Lalande 21185             | 439, 321 | Nu-XIII [13:13]        |
| Luyten's Star             | 471, 308 | Xi-XIII [14:13]        |
| Merak                     | 519, 501 | Omicron-XXI [15:21]    |
| Mizar                     | 458, 474 | Nu-XIX [13:19]         |
| Phad                      | 507, 485 | Omicron-XX [15:20]     |
| Pollux                    | 528, 312 | Omicron-XIII [15:13]   |
| Procyon                   | 467, 310 | Nu-XIII [13:13]        |
| Proxima Centauri          | 411, 313 | Mu-XIII [12:13]        |
| Rasalhague                | 284, 389 | Theta-XVI [8:16]       |
| Regulus                   | 640, 451 | Sigma-XIX [18:19]      |
| Rigel Kentaurus A         | 411, 314 | Mu-XIII [12:13]        |
| Rigel Kentaurus B         | 411, 314 | Mu-XIII [12:13]        |
| Sirius                    | 447, 306 | Nu-XIII [13:13]        |
| Sol                       | 414, 312 | Mu-XIII [12:13]        |
| Unukalhai                 | 138, 472 | Delta-XIX [4:19]       |
| Van Maanen's Star         | 393, 290 | Lambda-XII [11:12]     |
| Vega                      | 356, 339 | Kappa-XIV [10:14]      |
| Vindemiatrix              | 756, 483 | Chi-XX [22:20]         |
| p Eridani                 | 14, 39   | Alpha-II [1:2]         |

Stars that are well known but are outside the scope of the map:[^12] <small>Achernar (44), Acrux (98), Adhara (132), Alcyone (112), Algenib (102), Algieba (38), Alnath (40), Alnilam (411), Alnitak (250), Alphard (54), Antares (185), Arneb (393), Bellatrix (74), Betelgeuse (131), Canopus (95), Deneb (990), Dubhe (37), Enif (206), Etamin (45), Hadar (161), Izar (64), Kaus Australis (44), Kochab (38), Markab (42), Menkar (67), Mirach (61), Mirphak (181), Nihal (48), Nunki (68), Polaris (132), Rasalgethi (117), Rigel (236), Saiph (221), Scheat (61), Shaula (215), Shedir (70), Spica (80), Tarazed (141).</small>

[^12]: The scope of the map ends with the 5000th star of the HYG catalog when sorted by distance from Sol. All stars farther away than 35.7 light years are not included. (The number in parenthesis after the star's name is the distance in light years.)

## CC License

The underlying data is public domain, of course. I am releasing the computed 2D coordinates to public domain, too. Everything else (the hex maps, the indexes, this text) are Creative Commons Attribution 4.0.

## Contact

I am Filip H. and you can reach me at filip dot hracek at gmail dot com or on [Google+][filipgplus].

[filipgplus]: https://plus.google.com/u/0/+filiphracek