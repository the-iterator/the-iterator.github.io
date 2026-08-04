---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
======
* Ph.D in Version Control Theory, GitHub University, 2018 (expected)
* M.S. in Jekyll, GitHub University, 2014
* B.S. in GitHub, GitHub University, 2012

Work experience
======
* Spring 2024: Academic Pages Collaborator
  * GitHub University
  * Duties includes: Updates and improvements to template
  * Supervisor: The Users

* Fall 2015: Research Assistant
  * GitHub University
  * Duties included: Merging pull requests
  * Supervisor: Professor Hub

* Summer 2015: Research Assistant
  * GitHub University
  * Duties included: Tagging issues
  * Supervisor: Professor Git
  
Skills
======
* Skill 1
* Skill 2
  * Sub-skill 2.1
  * Sub-skill 2.2
  * Sub-skill 2.3
* Skill 3

Publications
{% include base_path %}

{% for post in site.publications reversed %}
  <div style="margin-bottom: 20px; font-size: 0.95em; line-height: 1.5;">
    <!-- 1. Publication Text (Authors, Year, Title, Journal) -->
    <span style="color: #333;">
      {% if post.citation %}
        {{ post.citation }}
      {% else %}
        <strong>{{ post.title }}</strong>. Published in <i>{{ post.venue }}</i>, {{ post.date | default: "1900-01-01" | date: "%Y" }}.
      {% endif %}
    </span>
    <!-- 2. Minimalist Direct Link -->
    {% if post.paperurl %}
      <span style="font-size: 0.9em; margin-left: 5px;">
        👉 <a href="{{ post.paperurl }}" target="_blank" style="font-weight: bold; color: #0076a3; text-decoration: underline;">Official Link</a>
      </span>
    {% endif %}
  </div>
{% endfor %}
  
Talks
======
  <ul>{% for post in site.talks reversed %}
    {% include archive-single-talk-cv.html  %}
  {% endfor %}</ul>
  
Teaching
======
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Service and leadership
======
* Currently signed in to 43 different slack teams
