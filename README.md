# VLBI Imaging Script  [![license badge][license-badge]][license-link] [![stable version][stable version-badge]][release] [![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive)

[license-badge]: https://img.shields.io/packagist/l/doctrine/orm.svg
[license-link]:  https://github.com/rstofi/VLBI_Imaging_Script/blob/master/LICENSE
[stable version-badge]: https://img.shields.io/badge/stable-v0.1-blue.svg
[release]: https://github.com/rstofi/VLBI_Imaging_Script/releases

Python module for imaging VLBI data based on *difmap*. It contains a growing library with functions for imaging and modelling (pre-calibrated e.g. with AIPS) VLBI observations. These scripts are designed for automatic imaging and modeling of hundreds or thoustand 'typical' sources. The script was tested on the VIPS survey (see our [paper][]), nevertheless more simple examples are presented here.

[paper]: https://arxiv.org/abs/1701.04037

## Dependencies

The required dependiences to run the script:

- [Python][] version 3.6+
- [Numpy][] >= 1.11.3
- [Matplotlib][] >= 2.0
- [AstroPy][] >= 1.3
- [difmap][] >= 2.4

The script was tested on Ubuntu 16.04.2 LTS release.

## Development

This package is meant to be a widely used imaging tool, thus further developments are encouraged. Using [Git][] version contol package, you can check out the latest sources from [GitHub][] using:

	git clone https://github.com/rstofi/VLBI_Imaging_Script.git

## Contribution

The package goal is to be an effective and useful tool for radio astronomy community, thus the gereral guidelines for contribution are the following:

Any contribution should be done trough GitHub pull request system using the 'developer' branch. All submitted code should be well-commented and documented. It is reccomended to also submit an example for the submitted funcitons if the cahnge is huge/make diffrence.

## Authors
### Package Authos

* [Kristóf Rozgonyi][] `<rstofi@gmail.com>`
* Sándor Frey `<frey.sandor@csfk.mta.hu>`

[Python]: http://www.python.org
[Numpy]: http://www.numpy.org
[Matplotlib]: http://matplotlib.org
[AstroPy]: http://www.astropy.org/
[difmap]: https://science.nrao.edu/facilities/vlba/docs/manuals/oss2013a/post-processing-software/difmap
[Git]: http://git-scm.com/
[GitHub]: http://www.github.com
[Kristóf Rozgonyi]: https://github.com/rstofi
