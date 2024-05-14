from helpers.common import *


class Debug:
    def __init__(self, app, name):
        self.app = app
        self.name = name

    def screenshot(self, folder=None, suffix_name=None, quality=100, logging=True):
        if suffix_name and logging:
            log(f"Debug | screenshot -> {self.name}/{suffix_name}")

        output = f"{get_date_for_log()}/{self.name}"
        if folder is not None:
            output += f"/{str(folder)}"

        _region = self.app.get_window_region()
        debug_save_screenshot(
            region=_region,
            output=output,
            suffix_name=suffix_name,
            quality=quality,
            ext='png'
        )
