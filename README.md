# Deer Tracker

Identify and track wildlife using trail cameras and object detection.

[Development notes](docs/NOTES.md)

[Prediction Examples](docs/EXAMPLES.md)

[Datasets](docs/DATASETS.md)

## Install env

```bash
sudo apt-get install -y tk-dev
pyenv install 3.8.2
pyenv global 3.8.2
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .
```

## Add camera

```bash
deertracker add-camera \
    --name "Southwest Stand" \
    --lat 46.399995 \
    --lon -90.772639

deertracker add-camera \
    --name "Turkey Blind" \
    --lat 46.400041 \
    --lon -90.768497
```

Go here to find the lat/lon for your trail cam:

[Find lat/lon](https://www.latlong.net/)

## Run import

```bash
deertracker import-photos \
    --photos ~/Google\ Drive/Trail\ Cam \
    --camera "Soutwest Stand"

deertracker import-photos \
    --photos ~/Google\ Drive/Trail\ Cam \
    --camera "Turkey Blind"
```

Passing `--training` will flag photos as training data and disable the `--camera` option.
Training photos do not require EXIF Datetime.

## Show prediction

```bash
deertracker show-prediction --photo ~/Google\ Drive/Trail\ Cam/001.jpg
```

## Show classification

```bash
deertracker show-classes --photo ~/Google\ Drive/Trail\ Cam/001.jpg --model-dir ./models/dt-0094/
```

`--model-dir` is optional

## Import caltech crops

```bash
deertracker caltech \
  --photos ~/Downloads/caltech/cct_images \
  --bboxes ~/Downloads/caltech/caltech_bboxes_20200316.json
  [--show] plots the bounding boxes instead of creating crops
```

* Output is to `.data/photos/training/`

## Sort caltech labeled photos

Sort caltech photos into label folders, these uncropped images can be selectively
imported back into the databsae as crops using th `import-photos --training` command.

```bash
deertracker caltech \
  --photos ~/Downloads/caltech/cct_images \
  --bboxes ~/Downloads/caltech/caltech_bboxes_20200316.json
  --labels ~/Downloads/caltech/caltech_images_20200316.json
```

* Output is to `.data/photos/uncropped/`

## Import NA Bird crops

```bash
deertracker nabirds \
  --image-ids nabirds/images.txt \
  --bboxes nabirds/bounding_boxes.txt \
  --labels nabirds/image_class_labels.txt \
  --classes nabirds/classes.txt \
  --photos nabirds/images/
```

## Import ENA-24 crops

```bash
deertracker ena24 \
  --photos ena24/images/
  --bboxes ena24/ena24.json
```

## Run training

```bash
deertracker train $name\
 --images ./training_imgs/ \
 --model-dir ./models/ \
 --min-images 1000 \
 --epochs 500
```

`$name` is the name of the model, the rest of the flags are optional

### Training can be done in a python notebook like colab.research.google.com with a small amount of code

```notebook

# pull down the training code
! git clone https://github.com/lukeforehand/deertracker
% cd /content/deertracker/
! git pull
! git checkout main

# install requirements
% pip install --quiet -r requirements.txt

# mount google drive to load training data and save model output
from google.colab import drive
drive.mount("/content/drive", force_remount=True)

# untar the training dataset from google drive
! tar xfz --keep-old-files ../drive/MyDrive/deertracker_crops.tar.gz

# train, saving the model checkpoints to google drive incase google colab disconnects.
! python -m deertracker.main train dt \
  --images "training_imgs" \
  --model-dir ../drive/MyDrive/deertracker \
  --min-images 200 \
  --epochs 1000

```
