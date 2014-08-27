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
	<li class="button preferred"><a href="#"><strong>Download</strong> the map</a></li>
	<li class="button"><a href="#">See on GitHub</a></li>
</ul>


<!-- 	<picture>
	  <source media="(min-width: 32em)" srcset="img/vertical-large.jpg">
	  <img src="img/vertical-small.jpg" alt="A screenshot of an obfuscated view from the Digital Universe software package." />
	</picture> -->
</div>

Our sci-fi books, movies and role-playing adventures are filled with exploration of the galaxy and the universe at large. It's all _planet this_ and _star system that_, and how many parsecs between them.

**But notice one thing:** those places are either completely made up[^1] or they are random stars taken from our night sky without any context.[^2]

[^1]: For example: most Star Trek's star systems (such as [Kaldra][]) or most Doctor Who's star systems (such as [4-X-Alpha-4][]). 
[^2]: For example [Arrakis][] is supposed to be orbiting Canopus, or [Whistle Stop][] is supposedly in the Nu Phoenicis star system. Those are real stars, yes, but they're only there for the sake of verisimilitude. In other words, those star systems were probably picked solely based on having cool sounding names and being in the star atlas. Briefly looking at [planets from Frank Herbert's Dune][Dune planets], it looks like they're all over the place – it's probably safe to say Frank Herbert didn't try to create a coherent topology of his fictional universe. Nor did almost anyone else. Because it's _hard_.

[Kaldra]: http://en.wikipedia.org/wiki/List_of_Star_Trek_planets_(G%E2%80%93L)
[4-X-Alpha-4]: http://en.wikipedia.org/wiki/List_of_Doctor_Who_planets
[Arrakis]: http://en.wikipedia.org/wiki/Arrakis
[Whistle Stop]: http://en.wikipedia.org/wiki/List_of_Heinlein_planets#Time_for_the_Stars
[Dune planets]: http://en.wikipedia.org/wiki/List_of_Dune_planets

The reason is that _most of us don't actually have any idea what the topology of our star neighbourhood is like._ The three dimensions are super confusing. Is Sirius close to Mirzam? They _are_ on our night sky (Mirzam is a bright star right next to Sirius) but they are most definitely _not_ in 3D space (Sirius is 9 light years away, Mirzam is 500).[^3]

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

The problem is that currently available 2D maps are _views_. They show each star at its proper X and Y coordinates, but they completely discard the Z (depth) coordinate. In this respect they are almost as bad a representation of reality as the night sky. Two adjancent stars are often actually quite far from each other – but the viewer doesn't know this until after they _read_ that information.[^5]

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
* If star C is three times farther away from star B than star A, we want to see the same thing on the map.[^6] 

[^6]: This is our fitness function. Let's pick random stars A, B and C. Compute distance from A to B in 3D space (<em>a<sub>3d</sub></em>) and on the 2D map (<em>a<sub>2d</sub></em>). Do the same for B to C, for both 3D (<em>b<sub>3d</sub></em>) and 2D (<em>b<sub>2d</sub></em>). The goal is to minimize the difference between the ratios <em>a<sub>3d</sub>/b<sub>3d</sub></em> and <em>a<sub>2d</sub>/b<sub>2d</sub></em>.


## Enter Teuvo Kohonen

Note also what _isn't_ our goal here: perfect representation of 3D space on a 2D map. We are trying to minimize the distortion but we can't hope to get rid of it completely. 

But even when we limit our goals and recognize that the map can't ever be perfect, it's very hard to create a suitable map for even a few stars, and virtually _impossible_ to do so for thousands of them&hellip;

<p class="scream">&hellip; UNLESS YOU HAVE THINKING MACHINES THAT CAN DO THE WORK FOR YOU.</p>

Yes. Thanks to the amazing thing that is general purpose computing, and thanks to a particularly clever algorithm by the Finnish academician [Teuvo Kohonen][], we can leave the work to the machines.

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

Turns out a star's 3D coordinates can be seen as multi-_dimensional_ data. Because that's what they are. :)


## Motivation

It would be nice to see a fictional empire, federation, space-faring nation or civilization that inhabits stars that are actually close to each other. 

There are exceptions to the rule, of course. The tabletop role-playing game [2300AD][] lets you play in a [realistic 3D map of nearby stars][], for example. But  the 3D aspect is confusing

[2300AD]: http://en.wikipedia.org/wiki/2300_AD
[realistic 3D map of stars]: http://evildrganymede.net/2012/02/13/stellar-mapping-2300ad-near-star-map/

----


<p>You are anxious to find out more about this “egamebook” thing. You open the page at <a href="http://www.egamebook.com/">egamebook.com</a> in your <script>var userAgent = navigator.userAgent; if (userAgent.indexOf("Chrome") !== -1) {document.write("Chrome ");} else if (userAgent.indexOf("Firefox") !== -1) {document.write("Firefox ");} else if (userAgent.indexOf("Opera") !== -1) {document.write("Opera ");} else if (userAgent.indexOf("MSIE") !== -1) {document.write("Internet Explorer ");} else if (userAgent.indexOf("Safari") !== -1) {document.write("Safari ");}</script>browser and you read its contents.  The following is written on the page:</p>

> Egamebook is a project which strives to bring the [gamebook][] (aka Choose-Your-Own-Adventure) experience to the ‘new media’ platforms (mobile, tablet, web, ...). True, there are already great examples of electronic gamebooks out there, but they are not much more than a copy of the old, paper gamebooks – you merely choose between different paragraphs to read.
>
> This was a necessity in the old medium. In a book, you couldn’t – for example – run a simulation and then describe its changing state in natural language. But there is nothing stopping you from this today.

Interesting. You scratch your head and read some more.

> Well, actually, there is something stopping you. Existing electronic gamebook platforms are not ready for any of this. They are stuck in the book mindset. At best, they keep track of a few simple variables (e.g. number of gold coins), they do elementary computations on them, and then report the results in short messages.
>
> Imagine reading a book where you can do much more than just choose a path. Imagine a book where your actions have realistic and meaningful impact on the fictional, simulated world.
>
> <img class="knight" src="img/knight-illustration.jpg" alt="Knight illustration" />
>
> 1. You are playing as a bandit and choose your base of attacks to be in a forest between two villages. Your actions lead to one of villages having a shortage of goods, leading to higher prices there. It also leads to the forest acquiring a fame of being home to some _supernatural_ evil, because none of your victims makes it out alive.
>
> 2. You are a starship pilot with an asteroid in tow. When confronted with a much bigger, hostile ship, you execute a maneuvre which sends the asteroid flying toward it. The asteroid hits, dealing structural damage, and disabling some of the ship’s outer systems, including the scanner and two thrusters. This allows you to make your escape.
>
> 3. You are a boxer in the midst of a championship fight. Your opponent is shifting his weight as if to prepare for a massive left hook. You decide to call his bluff, expose your side, and deal a punch to the face in order to throw him off balance. He was not bluffing, though, and before you can hit, his left hook lands squarely on your exposed face, sending you flying to the ground.

Your eyebrows go way up. _Okay,_ you think, _nice. But how is this possible? I’m sure it’s fun to dream up things like these, but the big question is whether there’s a way to actually make them work._ You skip a few other examples. Then a subtitle catches your attention.

> ## A living, breathing world – through scripting
>
> Existing electronic gamebook systems work with either scripting languages (like JavaScript) or – more often – with something even simpler (something that only allows variables and conditional statements and not much else). In contrast, egamebook (this project) is build on [Dart][], which is a mature, structured programming environment. Authors can do as little as simple arithmetic assignments, or as much as running [physics simulations][] or complex ecologies.
>
> ![Illustration of a plane](img/plane-illustration.jpg)
>
> There is no limit to what the authors can implement. They have all the tooling and structure that they need for implementing complex mechanics like the ones above. Actually, in this respect, the tooling is better than for many [AAA games][]. 
>
> In the development of titles like Skyrim, most work is spent on the visual representation. The world needs to look as realistic as possible in 3D (not just graphics, but also the way people act, walk and talk, in 3D – that’s a lot of work). Scripting (including the world ‘simulation’ logic) is often done in languages like [Lua][], or in something like Skyrim’s [Papyrus][], and tends to be the last thing to worry about. In contrast – for an egamebook – scripting is _all you do_ (apart from writing, of course), so it makes perfect sense to give it a little more attention.
>
> An egamebook author can use libraries like [Box2D] for 2D physics, [AStar][] for pathfinding, [darwin][] for genetic algorithms, [Backy][] for neural networks – to name just a few. Authors can also easily create their own libraries, which they can test independently from the gamebook.
>
> Let’s say you need to keep track of each city in a game world – their population, economic characteristics, diplomacy status, and much more. In a language like Dart, the complexity is manageable: you create a `City` class and its logic, you test it, and when it's ready, you then use it in your egamebook.

<img class="cleaner" src="img/cleaner-illustration.jpg" alt="Cleaner illustration" />

All this starts to feel like a lot of BS. It looks good in theory, yes, but is there actually something that _works_?

> ## Current status
>
> The system is being developed alongside with the first true egamebook, called _The Bodega Incident_.
>
> It can already do all the basic stuff and much more, but it doesn’t make sense to release it just yet. The world doesn’t need another ‘okay’ electronic gamebook system. It needs a polished system, with a shining example of a gamebook.

It looks like you can sign up for a mailing list at this point (in case you’re interested in playing – or creating – an egamebook in the future).

<ul class="choices">
	<li class="button preferred"><a href="signup.html"><strong>Sign up</strong> (and receive no more than one email a month).</a></li>
	<li class="button"><a href="https://plus.google.com/communities/117415708119099457420">Join the Google+ Community.</a></li>
	<li class="button"><a href="http://www.youtube.com/watch?v=oHg5SJYRHA0">“I don’t want to ever hear about this thing again.”</a></li>
</ul>

[egamebook]: http://www.egamebook.com
[gamebook]: http://en.wikipedia.org/wiki/Gamebook
[Dart]: http://www.dartlang.org/
[physics simulations]: https://plus.google.com/111783114889748547827/posts/Jguy38GJbsy
[AAA games]: http://en.wikipedia.org/wiki/AAA#Games
[Lua]: http://en.wikipedia.org/wiki/Lua_(programming_language)
[Papyrus]: http://www.creationkit.com/Papyrus_Introduction
[Box2D]: http://pub.dartlang.org/packages/box2d
[AStar]: http://pub.dartlang.org/packages/a_star
[darwin]: http://pub.dartlang.org/packages/darwin
[Backy]: http://pub.dartlang.org/packages/backy
[RickRoll]: http://www.youtube.com/watch?v=oHg5SJYRHA0

