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


## Enter Teuvo Kohonen

Note also what _isn't_ our goal here: perfect representation of 3D space on a 2D map. We are trying to minimize the distortion but we can't _ever_ hope to get rid of it completely. 

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
	* The **size** of a star on the map corresponds to its [absolute magnitude][].
	* Stars with a **little green dot** next to them are candidates to have a habitable, Earth-like planet on their orbit.[^10]

[^8]: This means that if you cut the map in half, the resulting map's aspect ratio will again be &radic;<span style="text-decoration:overline">2</span>:1.
[^9]: This number was arrived at by getting ratios between 2D and 3D distances of nearby (<5 light years) stars and by looking at the mean and median, and at the histogram of these values. By looking at mean alone (0.166) the result would be 1 light year per 6 hexes. But I went for median/modus (0.130/0.12) because I wanted the calculation to be accurate in as many cases as possible (as opposed to being accurate on average but very inaccurate in most cases). Please keep in mind this is only a rough approximation and should not be taken too seriously given the nature of the map. Also, it works better on stars that are relatively close to each other (which is also by design).
[^10]: This idea is taken from the aforementioned maps by Winchell Chung. The underlying data is provided by _[HabCat][]: A Catalog of Nearby Habitable Systems_ by Jill Tarter and Margaret Turnbull.

[HYG Database]: http://www.astronexus.com/hyg
[HabCat]: http://phl.upr.edu/projects/habcat
[spectral type]: http://hyperphysics.phy-astr.gsu.edu/hbase/starlog/staspe.html
[absolute magnitude]: http://en.wikipedia.org/wiki/Absolute_magnitude

## Gallery

TBA

## Download

Both download types below include an overview map (PDF), all the \_\_\_ sectors (PDFs), an index of the more well-known stars, and a CSV file with all the data.

* **'Scientific' bundle** (123MB, zip)
	* Stars are labeled by their standard catalogue codes (for example: HIP 89937) or by a very commonly used name if available (for example: Barnard's star). This makes it very easy to research each star on astrological databases such as [Simbad][]. This also makes the map pretty boring.
	* Also includes an index of all the 5000 stars.
* **'Literary' bundle** (123MB, zip)
	* Stars are either labeled by a proper name or by a constellation designation (for example: Chi Draconis). If none of those two is available, a cool-sounding catalogue code[^10] is chosen over a more commonly used one (for example: STU 10B is chosen over HIP 86162).

If you want to see or play around with the source, go to the GitHub repository.

[^11]: Those are picked from [Simbad][]'s _Identifiers_ section by a simple algorithm which prefers shorter names and letters before numbers. You should still be able to find the star behind the name but for example in Simbad sometimes you'll need to prepend '\*' or '\*\*' before the designation (STU 10B is [\*\* STU 10B][STU 10B] in Simbad).

[Simbad]: http://simbad.u-strasbg.fr/simbad/sim-fid
[STU 10B]: http://simbad.u-strasbg.fr/simbad/sim-basic?Ident=**+STU+10B


## What to do with this?

Wouldn't it be nice to see a fictional empire, federation, space-faring nation or civilization that inhabits stars that are actually close to each other? If you're writing a book, creating a game or running a role-playing game

There are exceptions to the rule, of course. The tabletop role-playing game [2300AD][] lets you play in a [realistic 3D map of nearby stars][], for example. But  the 3D aspect is confusing

[2300AD]: http://en.wikipedia.org/wiki/2300_AD
[realistic 3D map of nearby stars]: http://evildrganymede.net/2012/02/13/stellar-mapping-2300ad-near-star-map/

## Index of well-known stars


| Star name  | X, Y   | Sector  |
|------------|--------|---------|
| Proxima    | 13, 16 | Epsilon-VII  |
| Altair     | 233, 90 | Omicron-II  |

Stars that are well known but are outside the scope of the map (distance from Sol > 36 light years): XX, YY, ZZ.

## CC License

The underlying data is public domain, of course. I am releasing the computed 2D coordinates to public domain, too. Everything else (the hex maps, the indexes, this text) are Creative Commons Attribution 4.0.

## Contact


