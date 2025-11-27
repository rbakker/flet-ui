#!/usr/bin/env python3
from dicom_folder_picker import dicom_folder_picker

from nicegui import ui


async def pick_file() -> None:
    result = await dicom_folder_picker('~',upper_limit=None, multiple=True)
    ui.notify(f'You chose {result}')


@ui.page('/')
def index():
    ui.button('Choose file', on_click=pick_file, icon='folder')


ui.run()
