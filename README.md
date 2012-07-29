# BDD using Behat #

1. download and install the sashi driver http://sahi.co.in/w/sahi
2. run the sahi driver ~/sashi/bin/sahi.sh
3. when writeing tests that you need javascript in remember to use @mink:sahi as a decorator for your Scenario definition

i.e.

> 
> @mink:sahi
> Scenario: This test uses javascript via a real browser and the sahi driver (chrome by default)

