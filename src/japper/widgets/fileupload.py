"""
File upload widget
"""
import ipyvuetify as v
import traitlets
import os


class FileUpload(v.VuetifyTemplate):
    template_file = os.path.join(os.path.dirname(__file__), 'fileupload.vue')
    file_info = traitlets.List().tag(sync=True)

    def __init__(self, **kwargs):
        self.file_info = []
        self.files_by_id = {}
        self.uploading_queue = []
        self.uploading_cnt = 0
        super().__init__(**kwargs)

    def get_file_info_by_id(self, id):
        for file_info in self.file_info:
            if file_info['id'] == id:
                return file_info
        return None

    def vue_file_added(self, added_cnt):
        for i in range(added_cnt, 0, -1):
            indx = len(self.file_info) - i
            id = self.file_info[indx]['id']
            self.files_by_id[id] = bytearray()
            self.uploading_queue.append(id)

        self.start_next_upload()
        # self.send({'method': 'startUpload', 'args': [indx]})

    def start_next_upload(self):
        while self.uploading_cnt < 3 and len(self.uploading_queue) != 0:
            self.uploading_cnt += 1
            file_id = self.uploading_queue.pop(0)
            self.send({'method': 'startUpload', 'args': [file_id]})

    def start_upload(self, file_id):
        if len(self.uploading_queue) >= 3:
            return

        self.send({'method': 'startUpload', 'args': [file_id]})

    def vue_upload(self, file_id, buffs):
        if file_id in self.files_by_id:
            self.files_by_id[file_id] += buffs[0]

    def vue_file_removed(self, file_id):
        del self.files_by_id[file_id]
        # del self.file_info[file_index]

    def vue_upload_done(self, file_id):
        self.uploading_cnt -= 1
        self.start_next_upload()

    def cancel(self):
        # when parent closes the dialog
        self.send({'method': 'cancelUpload', 'args': []})
        self.files_by_id = {}
        self.uploading_cnt = 0

    def write_files_to_storage(self, base_path='./'):
        for info in self.file_info:
            file_id = info['id']
            if file_id not in self.files_by_id:
                continue

            with open(os.path.join(base_path, info['name']), 'wb') as f:
                f.write(self.files_by_id[file_id])


__all__ = ['FileUpload']
