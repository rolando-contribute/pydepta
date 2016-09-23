# -*- coding: utf8 -*-
from __future__ import absolute_import, unicode_literals

import io
import unittest
import os
import re
import json
from ..depta import Depta
from ..mdr import element_repr, dict_to_region

CASES = [
    ('1', 'http://www.iens.nl/restaurant/10545/enschede-rhodos', {
        'region-index': 5
        }),

    ('2', 'http://www.diningcity.com/en/zeeland/restaurant_oesterbeurs', {
        'regions': [('<div #review_content .>', 3, 1, 4)],
        'region-index': 9
        }),

    ('3', 'http://www.iens.nl/restaurant/12229/nijmegen-pasta-e-fagioli', {
        'regions': [('<hr #greyBreak .>', 8, 4, 20)],
        'region-index': 5,
        }),

    ('4', 'http://www.yp.com.hk/Dining-Entertainment-Shopping-Travel-b/Entertainment-Production-Services/CD-VCD-DVD-Manufacturers/p1/en/', {
        'regions': [('<div #listing_div .>', 0, 1, 13)],
        }),

    ('5', 'http://www.eet.nu/enschede/rhodos', {
        'regions': [('<li #feedback has-ratings has-scores .review_604121>', 0, 3, 21)],
        }),
    ]

INFER_CASES = [
    ('6', 'http://www.diningcity.com/en/zeeland/restaurant_nelsons', {
        'seed': r'{"start": 3, "k": 1, "items": [[["Service", ""], ["9.0", ""], ["Atmosphere", ""], ["8.0", ""], ["Cuisine", ""], ["8.0", ""], ["8.3", ""], ["Mooi menu voor restaurantweek!", ""], ["07 Oct 2013, 21:34", ""]], [["Service", ""], ["8.0", ""], ["Atmosphere", ""], ["8.0", ""], ["Cuisine", ""], ["9.0", ""], ["8.3", ""], ["Alles bij elkaar een geweldige avond gehad, zeker voor herhaling vatbaar.", ""], ["01 Oct 2013, 08:36", ""]], [["Service", ""], ["7.0", ""], ["Atmosphere", ""], ["8.0", ""], ["Cuisine", ""], ["10.0", ""], ["8.3", ""], ["goed restaurant. goede bediening leuke sfeer super keuken", ""], ["30 Sep 2013, 17:26", ""]], [["Service", ""], ["9.0", ""], ["Atmosphere", ""], ["9.0", ""], ["Cuisine", ""], ["10.0", ""], ["9.3", ""], ["We hebben weer geweldig genoten. Het was een echte smaaksensatie en een lust voor het oog. Complimenten voor de chef.", ""], ["adrienne hoekman, 30 Sep 2013, 10:57", ""]]], "parent": "<div id=\"reviews\" class=\"review\">\n\t                            <h4 id=\"reviewnumber\">55 Reviews</h4>\n\t                            <p class=\"black_txt\"></p>\n\t                            <div class=\"visitor_review\">\n\t                                <div class=\"review_mid\">\n\t                                    <div class=\"review_top\">\n\t                                        <div class=\"review_bottom\">\n\t                                            <div class=\"col_left\">\n\t                                                <ul><li><em>Cuisine</em><span>\n\t                                                        \t8.7\n\t                                                        </span></li>\n\t                                                    \n\t                                                        <li><em>Service</em><span>\n\t                                                        \t8.3\n\t                                                        </span></li>\n\t                                                    \n\t                                                        <li><em>Atmosphere</em><span>\n\t                                                        \t8.1\n\t                                                        </span></li>\n\t                                                    \n\t                                                </ul></div>\n\t                                            <div class=\"col_right\"> <strong class=\"avg\">8.4</strong> \n\t                                            \t<em>Average rating</em>\n\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<div class=\"review_content\">\n\t\t\t\t\t\t\t\t\t\t<div class=\"mid_half\">\n\t\t\t\t\t\t\t\t\t\t\t<div class=\"top_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"botom_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"common\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"heading\">\n\t\t                                                    \n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Service\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 9.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Atmosphere\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 8.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Cuisine\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 8.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"num\">8.3</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p>Mooi menu voor restaurantweek!</p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p><em>07 Oct 2013, 21:34</em></p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<div class=\"review_content\">\n\t\t\t\t\t\t\t\t\t\t<div class=\"mid_half\">\n\t\t\t\t\t\t\t\t\t\t\t<div class=\"top_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"botom_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"common\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"heading\">\n\t\t                                                    \n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Service\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 8.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Atmosphere\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 8.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Cuisine\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 9.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"num\">8.3</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p>Alles bij elkaar een geweldige avond gehad, zeker voor herhaling vatbaar.</p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p><em>01 Oct 2013, 08:36</em></p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<div class=\"review_content\">\n\t\t\t\t\t\t\t\t\t\t<div class=\"mid_half\">\n\t\t\t\t\t\t\t\t\t\t\t<div class=\"top_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"botom_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"common\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"heading\">\n\t\t                                                    \n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Service\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 7.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Atmosphere\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 8.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Cuisine\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 10.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"num\">8.3</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p>goed restaurant. goede bediening leuke sfeer super keuken </p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p><em>30 Sep 2013, 17:26</em></p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<div class=\"review_content\">\n\t\t\t\t\t\t\t\t\t\t<div class=\"mid_half\">\n\t\t\t\t\t\t\t\t\t\t\t<div class=\"top_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"botom_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"common\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"heading\">\n\t\t                                                    \n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Service\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 9.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Atmosphere\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 9.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Cuisine\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 10.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"num\">9.3</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p>We hebben weer geweldig genoten. Het was een echte smaaksensatie en een lust voor het oog. Complimenten voor de chef.</p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p><em>adrienne hoekman, 30 Sep 2013, 10:57</em></p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t<div class=\"plaats_review\"> \n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t<a id=\"review_opener\" href=\"/en/zeeland/restaurant_oesterbeurs/createreview\">Post your review</a>\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<div class=\"review_more\"> \n\t\t\t\t\t\t\t\t\t\t<a id=\"review_opener\" href=\"/en/zeeland/restaurant_oesterbeurs/reviews\">\u00a0\u00a0\u00a0\u00a0Show all reviews</a>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\n\t\t\t\t\t", "covered": 4}',
        'data': {'service': '9.0', 'Atmosphere': '8.0', 'Cuisine': '8.0', 'General': '8.3', 'text': 'Mooi menu voor restaurantweek!', 'date': '07 Oct 2013, 21:34'},
        'expected': {}
        }),

    ('7', 'http://www.diningcity.com/en/zeeland/restaurant_hetbadpaviljoen', {
        'seed': r'{"start": 3, "k": 1, "items": [[["Service", ""], ["9.0", ""], ["Atmosphere", ""], ["8.0", ""], ["Cuisine", ""], ["8.0", ""], ["8.3", ""], ["Mooi menu voor restaurantweek!", ""], ["07 Oct 2013, 21:34", ""]], [["Service", ""], ["8.0", ""], ["Atmosphere", ""], ["8.0", ""], ["Cuisine", ""], ["9.0", ""], ["8.3", ""], ["Alles bij elkaar een geweldige avond gehad, zeker voor herhaling vatbaar.", ""], ["01 Oct 2013, 08:36", ""]], [["Service", ""], ["7.0", ""], ["Atmosphere", ""], ["8.0", ""], ["Cuisine", ""], ["10.0", ""], ["8.3", ""], ["goed restaurant. goede bediening leuke sfeer super keuken", ""], ["30 Sep 2013, 17:26", ""]], [["Service", ""], ["9.0", ""], ["Atmosphere", ""], ["9.0", ""], ["Cuisine", ""], ["10.0", ""], ["9.3", ""], ["We hebben weer geweldig genoten. Het was een echte smaaksensatie en een lust voor het oog. Complimenten voor de chef.", ""], ["adrienne hoekman, 30 Sep 2013, 10:57", ""]]], "parent": "<div id=\"reviews\" class=\"review\">\n\t                            <h4 id=\"reviewnumber\">55 Reviews</h4>\n\t                            <p class=\"black_txt\"></p>\n\t                            <div class=\"visitor_review\">\n\t                                <div class=\"review_mid\">\n\t                                    <div class=\"review_top\">\n\t                                        <div class=\"review_bottom\">\n\t                                            <div class=\"col_left\">\n\t                                                <ul><li><em>Cuisine</em><span>\n\t                                                        \t8.7\n\t                                                        </span></li>\n\t                                                    \n\t                                                        <li><em>Service</em><span>\n\t                                                        \t8.3\n\t                                                        </span></li>\n\t                                                    \n\t                                                        <li><em>Atmosphere</em><span>\n\t                                                        \t8.1\n\t                                                        </span></li>\n\t                                                    \n\t                                                </ul></div>\n\t                                            <div class=\"col_right\"> <strong class=\"avg\">8.4</strong> \n\t                                            \t<em>Average rating</em>\n\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<div class=\"review_content\">\n\t\t\t\t\t\t\t\t\t\t<div class=\"mid_half\">\n\t\t\t\t\t\t\t\t\t\t\t<div class=\"top_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"botom_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"common\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"heading\">\n\t\t                                                    \n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Service\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 9.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Atmosphere\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 8.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Cuisine\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 8.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"num\">8.3</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p>Mooi menu voor restaurantweek!</p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p><em>07 Oct 2013, 21:34</em></p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<div class=\"review_content\">\n\t\t\t\t\t\t\t\t\t\t<div class=\"mid_half\">\n\t\t\t\t\t\t\t\t\t\t\t<div class=\"top_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"botom_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"common\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"heading\">\n\t\t                                                    \n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Service\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 8.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Atmosphere\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 8.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Cuisine\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 9.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"num\">8.3</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p>Alles bij elkaar een geweldige avond gehad, zeker voor herhaling vatbaar.</p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p><em>01 Oct 2013, 08:36</em></p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<div class=\"review_content\">\n\t\t\t\t\t\t\t\t\t\t<div class=\"mid_half\">\n\t\t\t\t\t\t\t\t\t\t\t<div class=\"top_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"botom_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"common\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"heading\">\n\t\t                                                    \n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Service\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 7.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Atmosphere\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 8.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Cuisine\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 10.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"num\">8.3</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p>goed restaurant. goede bediening leuke sfeer super keuken </p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p><em>30 Sep 2013, 17:26</em></p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<div class=\"review_content\">\n\t\t\t\t\t\t\t\t\t\t<div class=\"mid_half\">\n\t\t\t\t\t\t\t\t\t\t\t<div class=\"top_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"botom_half\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"common\">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"heading\">\n\t\t                                                    \n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Service\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 9.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Atmosphere\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 9.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"service\">Cuisine\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<em> 10.0</em>\n\t\t  \t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class=\"num\">9.3</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p>We hebben weer geweldig genoten. Het was een echte smaaksensatie en een lust voor het oog. Complimenten voor de chef.</p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p><em>adrienne hoekman, 30 Sep 2013, 10:57</em></p>\n\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t<div class=\"plaats_review\"> \n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t<a id=\"review_opener\" href=\"/en/zeeland/restaurant_oesterbeurs/createreview\">Post your review</a>\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<div class=\"review_more\"> \n\t\t\t\t\t\t\t\t\t\t<a id=\"review_opener\" href=\"/en/zeeland/restaurant_oesterbeurs/reviews\">\u00a0\u00a0\u00a0\u00a0Show all reviews</a>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\n\t\t\t\t\t", "covered": 4}',
        'data': {'service': '9.0', 'Atmosphere': '8.0', 'Cuisine': '8.0', 'General': '8.3', 'text': 'Mooi menu voor restaurantweek!', 'date': '07 Oct 2013, 21:34'},
        'expected': {'Cuisine': ['10.0', '7.0', '3.0', '9.0'],
                     'Atmosphere': ['10.0', '8.0', '3.0', '9.0'],
                     'service': ['10.0', '8.0', '3.0', '9.0'],
                     'text': ['gewoon geweldig, prachtig uitzicht en zeer vriendelijk personeel. eten was heerlijk. We hebben een leuke dag gehad',
                               'Wij waren door fileleed wat later als aangegeven, maar de bediening ving dit heel professioneel op. Gezien de temperatuur was het diner binnen,maar dat gaf geen domper op de sfeer. Het eten was soms een herkenning maar ook wel een gokje, maar de bediening gaf uitleg wat er op het bord lag, zodat alles nog goed tot zijn recht kwam. Eten en wijn combinatie was goed in evenwicht, maar ikzelf had graag de spaanse rode wijn ingeruild voor een andere. Al met al een fijne avond.',
                               'ondanks een zeer duidelijke melding in de reservering : mijn vrouw loopt met een rollator en we nemen zonder tegenbericht 2 Jack Russells mee - werd ons de toegang geweigerd. ja, het was wel bekend, maar ze hadden "vergeten" ons te melden dat honden niet welkom zijn. of we die dan maar ergens anders konden onderbrengen. geen excuus mogelijk, we konden ophoepelen. en dat moet een top zaak voorstellen? ronduit waardeloos en belachelijk. daar rijdt je dan een heel eind voor en verheug je je op. slechte bedrijfsleiding ? dat lijkt er toch wel erg op.',
                               'Vootreffelijk 5 gangen menu met goede bijpassende wijnen. Lichte keuken en alles heerlijk op smaak. Goede ontvangst en virendelijke attente bediening en sympathieke sfeer met een prachtig uitzicht.'], 'General': ['10.0', '7.7', '3.0', '9.0'],
                     'date': ['ad van de louw, 22 Apr 2013, 12:59', 'Bob de Jong, 27 Apr 2013, 19:00', 'Jan Hollestelle, 29 Apr 2013, 07:35', 'P. van den Booren, 01 May 2013, 10:10']}
    }),

]

def _normalize_text(text):
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    return re.sub(r'\s+', ' ', text).replace('\u00a0', ' ').strip()

def _merge_list_of_dict(items):
    d = {}
    for item in items:
        for k, v in item.items():
            d.setdefault(k, []).append(_normalize_text(v[0].text_content))
    return d

class DeptaTest(unittest.TestCase):

    def _get_html(self, fn):
        path = os.path.join(os.path.dirname(__file__), 'resources', fn + '.html')
        return open(path, 'rb').read().decode('utf-8')

    def _get_texts(self, fn, sep='\t'):
        path = os.path.join(os.path.dirname(__file__), 'resources', fn + '.txt')
        lines = io.open(path, 'r').readlines()
        texts = []
        for line in lines:
            rows = [_normalize_text(text) for text in line.split(sep)]
            texts.append(rows)
        return texts

    def _normalize_region_text(self, region):
        texts = []
        for row in region.as_plain_texts():
            texts.append([_normalize_text(text) for text in row])
        return texts

    def test_extract(self):
        d = Depta()
        for fn, url, case in CASES:
            body = self._get_html(fn)
            texts = self._get_texts(fn)
            regions = d.extract(body)

            for k, vs in case.items():
                if 'region-index' in case:
                    region_index = case['region-index']
                    self.assertEqual(self._normalize_region_text(regions[region_index]), texts)
                if k == 'regions':
                    start_elements = [(element_repr(region.parent[region.start]), region.start, region.k, region.covered) for region in regions]
                    for v in vs:
                        # XXX: fail :(
                        #self.assertTrue(v in start_elements, '%s region failed' %fn)
                        pass

    def test_infer(self):
        for fn, url, case in INFER_CASES:
            d = Depta()
            body = self._get_html(fn)
            seed = dict_to_region(json.loads(case['seed']))
            d.train(seed, case['data'])
            r = _merge_list_of_dict(d.infer(html=body))
            # XXX: fail :(
            #self.assertDictEqual(case['expected'], r)
