<template>
  <div>
    <p v-if="latex">{{ latex }}</p>
    <div id="signature_pad" v-if="showPad">
      <VueSignaturePad
        width="512px"
        height="512px"
        ref="signaturePad"
        v-bind:options="{ minWidth:1.5, maxWidth: 1.5, throttle: 0, backgroundColor: 'rgba(255,255,255)' }"
        v-bind:customStyle="{ border: 'black 3px solid' }"
      />
      <div id="operation">
        <Button type="primary" @click="undo">撤销</Button>
        <Button type="primary" @click="clearPad">清空</Button>
        <Button type="primary" @click="uploadSignature" :disabled="loading">上传</Button>
      </div>
    </div>
    <div id="upload">
      <Upload action="/" :before-upload="handleUpload">
        <Button type="primary" icon="ios-cloud-upload-outline">选择文件</Button>
      </Upload>
      <Button type="primary" @click="upload" :disabled="uploadDisabled">开始上传</Button>
      <Button type="primary" @click="clear">清空上传文件</Button>
      <Button type="primary" @click="togglePad">显示输入Pad</Button>
      <div>
        <img v-if="img !== null" :src="img" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      file: null,
      loading: false,
      img: null,
      res: null,
      showPad: false,
      latex: null
    }
  },
  mounted() {
    window.vue = this
  },
  methods: {
    handleUpload(file) {
      let form = new FormData()
      form.append('input_image', file)
      this.file = form
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => {
        this.img = reader.result
      }
      return false
    },
    async upload() {
      this.loading = true
      console.log(this.file)
      const res = await this.$axios({
        method: 'post',
        url: '/api/upload_image',
        headers: { 'Content-Type': 'multipart/form-data' },
        data: this.file
      })
      console.log(res)
      this.res = res
      this.latex = res.data
      this.loading = false
    },
    uploadSignature() {
      if (this.$refs.signaturePad.isEmpty()) {
        alert('pad is empty!')
        return
      }
      let data = this.$refs.signaturePad.saveSignature().data
      let parts = data.split(';base64,')
      let contentType = parts[0].split(':')[1]
      let raw = window.atob(parts[1])
      let rawLength = raw.length
      let uInt8Array = new Uint8Array(rawLength)
      for (let i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i)
      }
      let form = new FormData()
      form.append(
        'input_image',
        new Blob([uInt8Array], { type: contentType }),
        'input_image.png'
      )
      this.file = form
      console.log(this.file)
      this.upload()
    },
    clear() {
      this.file = null
      this.img = null
      this.res = null
      this.latex = null
    },
    undo() {
      this.$refs.signaturePad.undoSignature()
    },
    clearPad() {
      this.$refs.signaturePad.clearSignature()
      this.latex = null
      this.file = null
    },
    togglePad() {
      this.showPad = !this.showPad
    }
  },
  computed: {
    uploadDisabled() {
      if (this.loading) {
        return true
      }
      return this.file === null
    }
  }
}
</script>

<style lang="css" scoped>
img {
  max-height: 500px;
  max-width: 750px;
  vertical-align: middle;
}

#signature_pad {
  width: 520px;
  height: 600px;
}

#operation {
  margin-top: 10px;
}
</style>