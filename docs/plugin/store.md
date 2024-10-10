---
layout: page
footer: false
sidebar: false
---

<div style="display:flex; justify-content:center; align-content:center">
<el-container style="width: 100%; max-width: 980px;">
<el-main>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="name" label="插件">
      <template #default="scope">
        <el-link type="primary" :href="scope.row.documentUrl" target="_blank">{{ scope.row.name }}</el-link>
      </template>
    </el-table-column>
    <el-table-column prop="desc" label="介绍" min-width="150" />
    <el-table-column prop="author" label="作者" />
    <el-table-column prop="" label="">
      <template #default="scope">
        <el-link type="primary" :href="scope.row.downloadUrl" target="_blank">源码</el-link>
      </template>
    </el-table-column>
  </el-table>
</el-main>
</el-container>
</div>

<script setup>
const tableData = [
  {
    name: '成语接龙',
    desc: '开启后识别成语，自动接龙',
    author: '@古一',
    documentUrl: '/qqbot/plugin/1296',
    downloadUrl: 'https://github.com/shenxgan/qqbot/tree/main/ws/plugins/idiom',
  },
  {
    name: '豆包 AI',
    desc: '接入抖音豆包 AI，提供 AI 文字聊天',
    author: '@古一',
    documentUrl: '/qqbot/plugin/9234',
    downloadUrl: 'https://github.com/shenxgan/qqbot/tree/main/ws/plugins/ai_doubao',
  },
  {
    name: '入群欢迎',
    desc: '在有新人入群时发送欢迎（文字、图片或其他）',
    author: '@古一',
    documentUrl: '/qqbot/plugin/4233',
    downloadUrl: 'https://github.com/shenxgan/qqbot/tree/main/ws/plugins/welcome',
  },
]
</script>
