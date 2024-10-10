---
layout: page
footer: false
sidebar: false
---

<div style="display:flex; justify-content:center; align-content:center">
<el-container style="width: 100%; max-width: 980px;">
<el-main>
  <el-table :data="data.tableData" style="width: 100%">
    <el-table-column prop="name" label="插件">
      <template #default="scope">
        <el-link v-if="scope" type="primary" :href="scope.row.documentUrl" target="_blank">{{ scope.row.name }}</el-link>
      </template>
    </el-table-column>
    <el-table-column prop="desc" label="介绍" min-width="150" />
    <el-table-column prop="author" label="作者" />
    <el-table-column prop="" label="">
      <template #default="scope">
        <el-link v-if="scope" type="primary" :href="scope.row.downloadUrl" target="_blank">源码</el-link>
      </template>
    </el-table-column>
  </el-table>
</el-main>
</el-container>
</div>

<script setup>
import { data } from './store.data.js'
</script>
