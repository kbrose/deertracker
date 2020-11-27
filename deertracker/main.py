import click
import pathlib

from deertracker import photo, visualize

from deertracker.model import MegaDetector


def file_generator(photos):
    exts = []
    exts.extend(photo.PHOTO_EXTS)
    exts.extend([ext.upper() for ext in photo.PHOTO_EXTS])
    exts.extend(photo.VIDEO_EXTS)
    exts.extend([ext.upper() for ext in photo.VIDEO_EXTS])
    for ext in exts:
        for x in pathlib.Path(photos).glob(f"**/*{ext}"):
            if x.is_file():
                yield str(x)


@click.group()
def main():
    pass


@main.command()
@click.option("--name", required=True, help="Name of camera")
@click.option("--lat", required=True, help="Latitude of camera location")
@click.option("--lon", required=True, help="Longitude of camera location")
def add_camera(name, lat, lon):
    camera = photo.add_camera(name, lat, lon)
    print(camera)


@main.command()
@click.option("--photos", required=True, help="Location of photos to process")
@click.option(
    "--camera", required=True, help="Name of trail cam to associate with photos"
)
def import_photos(photos, camera):
    results = photo.import_photos(camera, file_generator(photos))
    for i, result in enumerate(results):
        if results[i] is not None:
            print(results[i])


@main.command()
@click.option("--photos", required=True, help="Location of photos to process")
def show_prediction(photos):
    md = MegaDetector()
    for photo in file_generator(photos):
        visualize.show_prediction(photo, md)


if __name__ == "__main__":
    main()