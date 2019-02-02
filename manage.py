import argparse
import mapp
from commandmap import CommandMap


cm = CommandMap()
art = """
+------+.      +------+       +------+       +------+      .+------+
|`.    | `.    |\     |\      |      |      /|     /|    .' |    .'|
|  `+--+---+   | +----+-+     +------+     +-+----+ |   +---+--+'  |
|   |  |   |   | |    | |     |      |     | |    | |   |   |  |   |
+---+--+.  |   +-+----+ |     +------+     | +----+-+   |  .+--+---+
 `. |    `.|    \|     \|     |      |     |/     |/    |.'    | .'
   `+------+     +------+     +------+     +------+     +------+'
"""


@cm.register()
def launch(host: str, port: int):
    """
    launch the web server
    """
    app = mapp.create_app()
    app.run(host, port)


@cm.register()
def embed():
    """
    devel: embed inside app context, with database models in globals()
    """
    import models
    db = models.db
    Patient = models.Patient
    Payment = models.Payment
    from IPython import embed as iembed
    app = mapp.create_app()
    with app.app_context():
        iembed()


@cm.register()
def load_json(table_name, json_name):
    """
    # TODO: cm choices support
    :param table_name: a model's table name to load json to, possible values are 'patients' and 'payments'
    :param json_name: json name 0_0
    """
    app = mapp.create_app()
    with app.app_context():
        mapp.import_json(table_name, json_name)


if __name__ == "__main__":
    cm.parse_args()
    cm.launch()
