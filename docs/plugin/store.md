---
layout: page
footer: false
sidebar: false
---

<div style="display:flex; justify-content:center; align-content:center">
<ClientOnly>
<el-container style="width: 100%; max-width: 980px;">
<el-main>
  <el-table :data="data.tableData" style="width: 100%">
    <el-table-column prop="name" label="插件" min-width="90">
      <template #default="scope">
        <el-link v-if="scope" type="primary" :href="scope.row.documentUrl" target="_blank">{{ scope.row.name }}</el-link>
      </template>
    </el-table-column>
    <el-table-column prop="desc" label="介绍" min-width="180" />
    <el-table-column prop="" label="类型" width="90">
      <template #default="scope">
        <el-tag v-if="scope" :type="types[scope.row.type].type">{{ types[scope.row.type].desc }}</el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="author" label="作者" />
    <el-table-column prop="" label="下载" width="90">
      <template #default="scope">
        <el-link v-if="scope" type="primary" :href="scope.row.downloadUrl" target="_blank">源码</el-link>
      </template>
    </el-table-column>
  </el-table>
</el-main>
</el-container>
</ClientOnly>
</div>

<script setup>
import { ref } from 'vue'
import { data } from './store.data.js'

const types = ref({
    message: {'type': 'primary', 'desc': '消息'},
    notice: {'type': 'success', 'desc': '事件'},
    cron: {'type': 'danger', 'desc': '定时'},
})
</script>
