# What's is this color?

Often we find a color written down as a string such as 'pale yellow'---but what does this mean?
This app is our attempt to find this out and to create a mapping between the color string and the actual color (as RGB). The tool records only the color string, the RGB coordinates, and the time it took to pick the color.

The results of this survey have been used for a [machine learning approach that attempts to predict the color of MOFs.](https://chemrxiv.org/articles/preprint/A_Data-Driven_Perspective_on_the_Colours_of_Metal-Organic_Frameworks/13033217)

The results (colors picked for a given color name and the time this took) are [available on Zenodo.](https://zenodo.org/record/3831845)

## Try it out

[Try it on Heroku](https://colorjeopardy.herokuapp.com/).

If you want to run the application on your machine, we recommend that you create a clean virtual environment (e.g., a conda environment) and install all the dependencies

```bash
pip install -r requirements
```

Then you should be able to start the app with

```bash
python run_app.py
```
