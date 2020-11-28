import click
import pathlib

from deertracker import photo, visualize
from deertracker.photo import PhotoProcessor


def find_files(photos):
    exts = []
    exts.extend(photo.PHOTO_EXTS)
    exts.extend([ext.upper() for ext in photo.PHOTO_EXTS])
    exts.extend(photo.VIDEO_EXTS)
    exts.extend([ext.upper() for ext in photo.VIDEO_EXTS])
    return [
        str(x)
        for ext in exts
        for x in pathlib.Path(photos).glob(f"**/*{ext}")
        if x.is_file()
    ]


@click.group()
def main():
    pass


@main.command(help="Add camera location")
@click.option("--name", required=True, help="Name of camera")
@click.option("--lat", required=True, help="Latitude of camera location")
@click.option("--lon", required=True, help="Longitude of camera location")
def add_camera(name, lat, lon):
    camera = photo.add_camera(name, lat, lon)
    print(camera)


@main.command(help="Import photos")
@click.option("--photos", required=True, help="Location of photos to process")
@click.option(
    "--camera", required=True, help="Name of trail cam to associate with photos"
)
@click.option(
    "--ignore-time",
    default=False,
    is_flag=True,
    required=False,
    help="Process photos that are missing EXIF Datetime",
)
def import_photos(photos, camera, ignore_time):
    p = PhotoProcessor(camera, ignore_time, find_files(photos))
    for result in p.import_photos():
        print(result)


@main.command(help="Show predictions for photos")
@click.option("--photos", required=True, help="Location of photos to process")
def show_predictions(photos):
    visualize.show_predictions(find_files(photos))


if __name__ == "__main__":
    main()