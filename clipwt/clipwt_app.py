from clipwt.clipwt_constants import ClipAppStatus
from clipwt.clipwt_controller import ClipWtController
from clipwt.clipwt_model import ClipWtModel
from clipwt.clipwt_ui import ClipWtApp

def launch():
    model = ClipWtModel(ClipAppStatus.STOP, "", None)
    controller = ClipWtController(model)
    app = ClipWtApp(controller)
    app.show()