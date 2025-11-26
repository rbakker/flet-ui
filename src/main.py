import flet as ft
import os, os.path as op

def main(page: ft.Page):
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            e.path if e.path else "Cancelled!"
        )
        selected_files.update()

        allFiles = []
        print(e.path)
        for (root,dirs,files) in os.walk(e.path,topdown=True):
            for f in files:
                allFiles.append(f)
        print(allFiles)
        dicom_stats.value = '\n'.join(allFiles)
        dicom_stats.update()    

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    dicom_stats = ft.Text()

    page.overlay.append(pick_files_dialog)

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Select DICOM directory",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.get_directory_path(),
                ),
                selected_files,
            ]
        ),
        ft.Row(
            [
                dicom_stats
            ]
        )
    )


ft.app(main)
