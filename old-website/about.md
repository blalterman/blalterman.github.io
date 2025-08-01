---
layout: single
permalink: /
description: B. L. Alterman is a NASA Research Astrophysicist studying the solar wind, space weather, and humanity’s place in the heliosphere using data from Wind, ACE, Parker Solar Probe, and Solar Orbiter.
author: B. L. Alterman
image: /assets/images/headshot.jpg
keywords:
  - B. L. Alterman
  - heliophysics
  - solar wind
  - space weather
---

<p>
  <img src="/assets/images/headshot.jpg" alt="B. L. Alterman headshot" class="about-headshot" />
  I'm a Research Astrophysicist based in Greenbelt, MD, where I study how the Sun drives the solar wind and shapes the space environment of our solar system. I earned my PhD in Applied Physics from the University of Michigan, where I focused on how Coulomb collisions and kinetic processes influence the solar wind. After a postdoc at the Southwest Research Institute in San Antonio—where I was later promoted to Research Scientist—I joined NASA as a civil servant to continue my work in heliophysics.
</p>

I consider myself a heliophysics generalist, working across the thermal and suprathermal solar wind. My research spans multiple spacecraft—including Wind, ACE, Parker Solar Probe, and Solar Orbiter—and timescales ranging from seconds to decades. I’m especially interested in how the composition and structure of the solar wind reflect both its solar source and the processes it undergoes during interplanetary travel. My recent work on helium abundance and heavy ion composition has opened up new questions about solar cycle variability and space weather forecasting.

At the heart of my work is a deep curiosity about our Sun, humanity’s place in the Universe, and how solar variability affects life on Earth through space weather. As a Fellow of The Explorers Club and an active member of the heliophysics community, I try to bring energy, creativity, and a systems-level perspective to everything I do.

You can find my research profiles at the links below. My publications are available [here](/publications/).

- <img src="/assets/images/orcid/ORCID-iD_icon_24x24.png" alt="ORCID logo" width="20" height="20"> [ORCID](https://orcid.org/{{ site.ads_orcid }})
- <img src="/assets/images/ads/ads.svg" alt="NASA ADS logo" width="20" height="20"> [NASA ADS](https://ui.adsabs.harvard.edu/search/q=orcid%3A{{ site.ads*orcid }}&sort=date%20desc,%20bibcode%20desc&p*=0)
- <img src="/assets/images/google-scholar/google-scholar.svg" alt="Google Scholar logo" width="20" height="20"> [Google Scholar](https://scholar.google.com/citations?user=yF0j6J8AAAAJ)
- <img src="/assets/images/arxiv/arxiv.svg" alt="arXiv logo" width="20" height="20"> [arXiv](https://arxiv.org/a/alterman_b_1)
- <img src="/assets/images/github/github-mark.svg" alt="GitHub logo" width="20" height="20"> [GitHub](https://github.com/blalterman)

<section class="about-columns">
  <div class="about-right">
    <h2>Education</h2>
    <table class="education-table">
      <thead>
        <tr>
          <th>Institution</th>
          <th>Department</th>
          <th>Location</th>
          <th>Dates</th>
        </tr>
      </thead>
      <tbody>
        {% for edu in site.data.education %}
        <tr>
          <td>{{ edu.Institution }}</td>
          <td>{{ edu.Department }}</td>
          <td>{{ edu.Location }}</td>
          <td>{{ edu.Dates }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  <h2>Experience</h2>
  <table class="positions-table">
  <thead>
    <tr>
      <th>Title</th>
      <th>Company</th>
      <th>Dates</th>
      <th>Location</th>
    </tr>
  </thead>
  <tbody>
    {% for pos in site.data.positions %}
    <tr>
      <td>{{ pos["Position Title"] }}</td>
      <td>{{ pos.Company }}</td>
      <td>{{ pos.Dates }}</td>
      <td>{{ pos.Location }}</td>
    </tr>
    {% endfor %}
</tbody>
</table>
</div>
</section>
