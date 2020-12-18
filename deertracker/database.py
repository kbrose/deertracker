import sqlite3

from contextlib import contextmanager
from datetime import datetime

from deertracker import DEFAULT_DATABASE, schema


@contextmanager
def conn():
    c = Connection()
    try:
        yield c
    finally:
        c.close()


# FIXME: foreign key constraints don't work
class Connection:
    def __init__(self, database=DEFAULT_DATABASE):
        conn = sqlite3.connect(database)
        conn.execute(schema.CREATE_TABLE_CAMERA)
        conn.execute(schema.INSERT_TRAINING_CAMERA)
        conn.execute(schema.CREATE_TABLE_BATCH)
        conn.execute(schema.CREATE_TABLE_PHOTO)
        conn.execute(schema.CREATE_TABLE_OBJECT)
        self.conn = conn

    def close(self):
        self.conn.close()

    def insert_camera(self, camera):
        try:
            sql = "INSERT INTO camera(name, lat, lon) VALUES(?, ?, ?)"
            cur = self.conn.cursor()
            cur.execute(sql, camera)
            self.conn.commit()
            return self._camera_from_tuple(camera)
        except sqlite3.IntegrityError:
            return {"error": f"Camera `{camera[0]}` already exists."}

    def select_camera(self, camera_name):
        return self._camera_from_tuple(
            self.conn.cursor()
            .execute("SELECT * FROM camera WHERE name = ?", [camera_name])
            .fetchone()
        )

    def _camera_from_tuple(self, camera):
        if camera is None:
            return None
        return {
            "name": camera[0],
            "lat": camera[1],
            "lon": camera[2],
        }

    def select_photo(self, photo_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM photo WHERE id = ?", [photo_id])
        return cur.fetchone()

    def insert_batch(self):
        batch_time = datetime.now()
        sql = "INSERT INTO batch(id, time) VALUES(NULL, ?)"
        cur = self.conn.cursor()
        cur.execute(sql, [batch_time])
        cur.execute("SELECT LAST_INSERT_ROWID()")
        batch_id = cur.fetchone()[0]
        self.conn.commit()
        return {"id": batch_id, "time": batch_time}

    def insert_photo(self, photo):
        try:
            sql = "INSERT INTO photo(id, path, batch_id) VALUES(?, ?, ?)"
            cur = self.conn.cursor()
            cur.execute(sql, photo)
            self.conn.commit()
            return {"id": photo[0], "path": photo[1]}
        except sqlite3.IntegrityError:
            return {"error": f"Photo `{photo[1]}` already exists."}

    def insert_object(self, obj):
        try:
            sql = "INSERT INTO object(id, path, lat, lon, time, label, confidence, ground_truth, photo_id, camera_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cur = self.conn.cursor()
            cur.execute(sql, obj)
            self.conn.commit()
            return {
                "id": obj[0],
                "path": obj[1],
                "lat": obj[2],
                "lon": obj[3],
                "time": obj[4],
                "label": obj[5],
                "confidence": obj[6],
                "ground_truth": obj[7],
                "photo_id": obj[8],
                "camera_id": obj[9],
            }
        except sqlite3.IntegrityError:
            return {"error": f"Object `{obj[1]}` already exists."}

    def select_objects(self):
        return [
            self._object_from_tuple(obj)
            for obj in self.conn.cursor()
            .execute("SELECT * FROM object WHERE ground_truth IS FALSE")
            .fetchall()
        ]

    def _object_from_tuple(self, obj):
        if obj is None:
            return None
        return {
            "id": obj[0],
            "path": obj[1],
            "lat": obj[2],
            "lon": obj[3],
            "time": obj[4],
            "label": obj[5],
            "confidence": obj[6],
            "ground_truth": obj[7],
            "camera_id": obj[8],
            "photo_id": obj[9],
        }

    def set_object_ground_truth(self):
        cur = self.conn.cursor()
        cur.execute("UPDATE object SET ground_truth = TRUE")
        self.conn.commit()
