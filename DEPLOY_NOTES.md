Deploy Notes
============


Nov, 8 2013 - [fix-photos-to-s3]
----------------------------------

*. upgrade CICU so that it allows references to s3/3rd party urls and not just local MEDIA_URL

```
pip install -e git+https://github.com/rosscdh/clean-image-crop-uploader.git@rc_fixes#egg=clean-image-crop-uploader --upgrade
```