# wide-language-index

A listing of publicly available audio samples of a large number of different languages.

## Overview

The Wide Language Index is an attempt to curate a set of examples of a wide variety of languages from public podcasts. The index itself contains a listing of samples and information about them. The audio files themselves are not bundled in, but can be downloaded as needed.

The full dataset is meant to be downloaded from OS X or Linux. If your system meets the required dependencies, fetching examples of different languages should be as simple as running: `make fetch`.

## Dependencies

To use the tools that accompany this dataset, your computer should have installed:

- `python3.4`
- `pip`
- `virtualenv`
- `make`

Run `make audit` to check if the tools are working.

## Layout

The `index/` folder contains references to publicly accessible audio samples for which the principal language has been pre-determined. Each sample is represented by a JSON file containing, at minimum:

- `language`: the ISO 693-3 code for the language
- `media_urls`: the URL of the raw sample file
- `source_name`: what venue or outlet published the audio file
- `title`: the title of the podcast or sample
- `date`: the date of publication of the sample
- `checksum`: an md5 checksum of the language

It may also contain the optional fields:

- `source_url`: the URL of the page containing the podcast, for context
- `description`: a description of the contents, in English or in the source language

Each sample's file is named as `<language>/<language>-<checksum>.json`.

## License

This index is provided under the [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/). In short, you are free to use this data non-commercially as long as you provide a reference back to this project. If you have a use case where this would be onerous, please send me an email.

## Contributing

See [Contributing](https://github.com/larsyencken/wide-language-index/blob/master/CONTRIBUTING.md).

Lars Yencken <lars@yencken.org>
