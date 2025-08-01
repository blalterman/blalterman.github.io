---
layout: single
title: Publications
permalink: /publications/
classes: wide publications-page
description: Comprehensive list of B. L. Alterman's publications with citation metrics from NASA ADS.
keywords:
  - publications
  - research papers
  - NASA ADS
  - heliophysics
---

## Statistics

This page is automatically generated using data from [NASA ADS](https://ui.adsabs.harvard.edu/search/q=orcid%3A{{ site.ads_orcid }}&sort=date%20desc,%20bibcode%20desc&p_=0){:target="_blank" rel="noopener"} and is updated weekly.

- **h-index**: {{ site.data.ads_metrics["indicators"]["h"] }}
- **Total papers**: {{ site.data.ads_metrics["basic stats"]["number of papers"] }}
- **Total citations**: {{ site.data.ads_metrics["citation stats"]["total number of citations"] }}
- **Refereed papers**: {{ site.data.ads_metrics["basic stats refereed"]["number of papers"] }}
- **Refereed citations**: {{ site.data.ads_metrics["citation stats refereed"]["total number of citations"] }}

## Publication List

{% assign pubs_by_type = site.data.ads_publications | group_by: "publication_type" %}
{% assign custom_order = "phdthesis,article,inproceedings,abstract,techreport,eprint" | split: "," %}

{% for type in custom_order %}
{% assign group = nil %}
{% for g in pubs_by_type %}
{% if g.name == type %}
{% assign group = g %}
{% endif %}
{% endfor %}

{% if group %}

{% if group.name == "phdthesis" %}

<h3>PhD Thesis</h3>

{% elsif group.name == "article" %}

<h3>Refereed Publications</h3>

{% elsif group.name == "inproceedings" %}

<h3>Conference Proceedings</h3>

{% elsif group.name == "abstract" %}

<h3>Conference Presentations</h3>

{% elsif group.name == "techreport" %}

<h3>White Papers</h3>

{% elsif group.name == "eprint" %}

<h3>Pre-Prints</h3>

{% else %}

<h3>{{ group.name | capitalize }}</h3>

{% endif %}

{% assign pubs = group.items | sort: "year" | reverse %}
{% assign pub_count = pubs | size %}

{% if group.name == "phdthesis" %}
<ul class="publication-list unnumbered">
  {% for pub in pubs %}
    {% include publication_entry.liquid pub=pub %}
  {% endfor %}
</ul>
{% else %}
<ol class="publication-list" reversed start="{{ pub_count }}">
  {% for pub in pubs %}
    {% include publication_entry.liquid pub=pub %}
  {% endfor %}
</ol>
{% endif %}

{% endif %}
{% endfor %}

<style>
.publication-list {
  list-style-type: decimal;
  padding-left: 1.5em;
}
.publication-list li {
  margin-bottom: 1.2em;
  line-height: 1.5em;
}
.publication-list a {
  text-decoration: none;
  color: #0645ad;
}
.publication-list a:hover {
  text-decoration: underline;
}
.publication-list.unnumbered {
  list-style-type: none;
  padding-left: 0;
}
</style>
