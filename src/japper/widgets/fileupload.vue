<template>
  <div>
    <input ref="fileInput" type="file" multiple style="display:none" accept=".yml"
           @change="addFiles($event.target.files)"/> <!--  -->
    <v-btn color="blue-grey" class="white--text" small @click="uploadClicked">
      <v-icon left dark>mdi-cloud-upload</v-icon>
      Choose File(s)
    </v-btn>
    <v-sheet color="grey lighten-3" class="d-flex flex-column mt-2 pa-2 overflow-y-auto overflow-x-hidden" width="350px"
             height="305px">
      <v-sheet transition="fade-transition" v-for="(item, index) in file_info" :itemKey="index"
               :color="item.status == 'done'?'green darken-1':(item.status=='uploading'?'lime darken-2':'grey darken-1')"
               class="pa-2 ma-1 d-flex fileinput-item align-center ">
        <div style="width:90%" class="mr-1">
          <span class="fileinput-item-filename">{{ item.name }}</span>
          <div class="d-flex">
            <span class="fileinput-item-size">{{ humanFileSize(item.size, true) }}</span>
            <span class="fileinput-item-size ml-auto">{{ item.status }}</span>
          </div>

        </div>
        <div class="ml-auto">
          <v-progress-circular :indeterminate="item.status == 'pending'" v-show="item.status != 'done'" size="22"
                               :value="item.progress" width="2" color="white" style="font-size:12px;">
            {{ item.status == 'uploading' ? item.progress : '' }}
          </v-progress-circular>
          <v-btn v-show="item.status == 'done'" fab dark x-small color="rgba(0,0,0,.5)" width="24px" height="24px"
                 @click="removeFile(index)">
            <v-icon dark> mdi-delete-outline</v-icon>
          </v-btn>
        </div>


      </v-sheet>
    </v-sheet>


  </div>
</template>

<style>
.fileinput-item {
  font-weight: 500;
  width: 98%;
  font-size: 14px;
  color: white !important;
  line-height: 1;
}

.fileinput-item-filename {
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  display: block;
  font-size: 12px;
}

.fileinput-item-size {
  font-size: 12px;
  opacity: .6;
}
</style>

<script>
modules.export = {
  created() {
    this.chunk_size = 5 * 1024 * 1024;
    this.abort = false;
    this.file_id_pool = 1000;
    this.native_file_info = [];
  },
  methods: {
    humanFileSize(B, i) {
      var e = i ? 1e3 : 1024;
      if (Math.abs(B) < e) return B + " B";
      var a = i ? ["kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"] : ["KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"],
          t = -1;
      do B /= e, ++t; while (Math.abs(B) >= e && t < a.length - 1);
      return B.toFixed(1) + " " + a[t]
    },
    uploadClicked() {
      this.$refs['fileInput'].click();
    },
    addFiles(filelist) {
      for (f of filelist) {
        f.id = this.file_id_pool;
        this.file_id_pool += 1;
        this.native_file_info.push(f);
      }

      file_cnt = 0
      for (f of filelist) {
        info = {};
        info.id = f.id;
        info.name = f.name;
        info.size = f.size;
        info.lastModified = f.lastModified;
        info.type = f.type;
        info.status = 'pending';
        info.progress = 0;

        this.file_info.push(info);
        file_cnt += 1;
      }

      this.vueCall(this.file_added, file_cnt);
    },
    removeFile(fileIndex) {
      this.file_removed(this.file_info[fileIndex].id);
      this.file_info.splice(fileIndex, 1);
      this.native_file_info.splice(fileIndex, 1);

    },
    clear() {
      this.file_info = [];
      this.native_file_info = [];
    },
    vueCall(func, args) {
      setTimeout(() => func(args), 100);
    },
    getFileInfoById(file_id) {
      for (f of this.file_info) {
        if (f.id == file_id)
          return f;
      }
      return null;
    },
    getNativeFileInfoById(file_id) {
      for (f of this.native_file_info) {
        if (f.id == file_id)
          return f;
      }
      return null;
    },

    jupyter_startUpload(file_id) {
      file_info = this.getFileInfoById(file_id);
      if (file_info == null)
        return;

      file_info.status = 'uploading';

      (async (file_info) => {
        const file = this.getNativeFileInfoById(file_info.id);
        if (file == null) return;
        let to_do = file_info.size;
        let sub_offset = 0;

        while (to_do > 0) {
          const sub_length = Math.min(to_do, this.chunk_size);
          const blob = file.slice(sub_offset, sub_offset + sub_length);
          const buff = await blob.arrayBuffer();
          this.upload(file_info.id, [buff]);

          to_do -= sub_length;
          sub_offset += sub_length;

          if (this.abort)
            return;
          await new Promise(r => setTimeout(r, 100));

          file_info.progress = Math.round((1.0 - (to_do / file.size)) * 100);

          // console.log(file_info.id, file.id, to_do, file.size, Math.round((1.0 - (to_do / file.size)) * 100));
        }

        file_info.status = 'done';
        this.upload_done(file_info.id);
      })(file_info);
    },
    jupyter_openDialog() {
      this.uploadClicked();
    },

    jupyter_cancelUpload() {
      this.abort = true;
      this.clear();
    },
  },
};
</script>
