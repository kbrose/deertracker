# Deer Tracker

[Development notes](NOTES.md)

[Prediction Examples](EXAMPLES.md)

## install env

```bash
sudo apt-get install -y tk-dev
pyenv install 3.8.2
pyenv global 3.8.2
pip install --upgrade pip
pip install -r requirements.txt
```

## add camera

```bash
./dt add-camera \
    --name "Southwest Stand" \
    --lat 46.399995 \
    --lon -90.772639

./dt add-camera \
    --name "Turkey Blind" \
    --lat 46.400041 \
    --lon -90.768497
```

Go here to find the lat/lon for your trail cam:

[Find lat/lon](https://www.latlong.net/)

## run import

```bash
./dt import-photos \
    --photos ~/Google\ Drive/Trail\ Cam \
    --camera "Soutwest Stand"

./dt import-photos \
    --photos ~/Google\ Drive/Trail\ Cam \
    --camera "Turkey Blind"
```

Passing `--training` will flag photos as training data and disable the `--camera` option.
Training photos do not require EXIF Datetime.

## show prediction

```bash
./dt show-prediction --photo ~/Google\ Drive/Trail\ Cam/001.jpg
```

## import caltech crops

```bash
./dt caltech \
  --photos ~/Downloads/caltech/cct_images \
  --bboxes ~/Downloads/caltech/caltech_bboxes_20200316.json
  [--show] plots the bounding boxes instead of creating crops
```

Produces crops into category folders, i.e.:

```bash
./opossum/ecc990e36531d2c517849d4787e30829.jpg
./dog/199795365fc783ca6ff3ee88298631a2.jpg
...
```
