# ImgScraper

Image scraper to get images from the web and build a training dataset from these images.

This scraper uses selenium as a way to automate the process of searching and storing the images.

# Disclaimer

- This scraper was built only for learning purposes. 
- Use this scraper with caution. Be sure to not break any laws or terms of service.

# Script usage

Be sure to download the correct [selenium driver](https://www.selenium.dev/downloads/) and store it in the path of your choice.

Also here is the new link for the [chromedriver](https://sites.google.com/chromium.org/driver/downloads).

## Arguments

- `-st` or `--searchterm` receives the term to be searched.
- `-dp` or `--driverpath` receives the path to driver file.
- `-n` or `--numofimages` receives the number or images to be saved.
- `-o` or `--output` receives the path to the output directory.

## Usage

This is an example of the usage using Google Images:

```
python image_scraper_g.py \
  -st "auto" \
  -dp /home/user/Downloads/chromedriver \
  -n 5 \
  -o /home/user/ImgScraper/
```

This is an example of the usage using Mercado Libre

```
python image_scraper_ml.py \
  -st "auto" \
  -dp /home/user/Downloads/chromedriver \
  -n 5 \
  -o /home/user/ImgScraper/
```

This is an example of the usage using Bing

```
python image_scraper_ml.py \
  -st "auto" \
  -dp /home/user/Downloads/chromedriver \
  -n 5 \
  -o /home/user/ImgScraper/
  -lk <bing_link>
```

While using the Bing scraper make sure to look for the ´nofocus´ class after the ´img´ tag.

# Acknowledgments

The script was taken from [Towards Data Science ](https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d). 
The secondary script is a modification to work with local pages. 
