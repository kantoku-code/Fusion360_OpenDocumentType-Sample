#FusionAPI_python addin
#Author-kantoku
#Description-Opened document type

import traceback
import adsk.core
import adsk.fusion


_app = adsk.core.Application.cast(None)
_ui  = adsk.core.UserInterface.cast(None)
_handlers = []


def run(context):
    ui = None
    try:
        global _app, _ui
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        onDocumentOpened = MyDocumentOpenedHandler()
        _app.documentOpened.add(onDocumentOpened)
        _handlers.append(onDocumentOpened)

    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class MyDocumentOpenedHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.DocumentEventArgs):
        msg = ""

        match args.document.dataFile.fileExtension:
            case "f2d":
                msg = "DocumentOpened - Drawing"
            case "f3d":
                if len(args.document.dataFile.childReferences) > 0:
                    msg = "DocumentOpened - Assembly"
                else:
                    msg = "DocumentOpened - Part"
            case _:
                return

        if len(msg) > 0:
            _app.log(msg)
            _ui.messageBox(msg)


def stop(context):
    try:
        _handlers = []

    except:
        print('Failed:\n{}'.format(traceback.format_exc()))