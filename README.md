# ProductHunt - Products of the day scraper

This is a synchronous scraper that gets information about all products of the date from ProductHunt from a given date or list of dates.

## Usage 

JSON Input

``{ "dates" : "2023/08/15"}`` 

or

``{ "dates" : ["2023/08/15", "2023/08/14", "2023/08/13"]}``

## Output
The output is a Python list of JSON objects that include the following information about each product:
<pre>
```
{
  "ph_url": "https://www.producthunt.com/posts/lottielab",
  "company_url": "lottielab.com",
  "name": "Lottielab",
  "featured_date": "2023/08/15",
  "tagline": "Create and ship lottie animations to sites and apps faster",
  "description": "Create and export Lottie animations to your websites and apps easily!\n\n- Import SVGs, Lotties, from Figma or create from scratch\n- Animate with a simple but powerful timeline\n- Export as Lottie, Gif or MP4 to any platform\n- Collaborate with your team",
  "ranking": "1",
  "upvotes": 1048,
  "product_category": "Design Tools",
  "comments": 199,
  "makers": [
    "Alistair Thomson",
    "Andrew Ologunebi",
    "David Davidovi\u0107",
    "Daryl Patigas",
    "Hugo Daniel",
    "Pius Chong",
    "Erwan Ameil",
    "Harvey",
    "Ayo Oluwanusin"
  ]
}
```
</pre>