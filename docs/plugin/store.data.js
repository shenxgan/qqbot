export default {
  load() {
    return {
      tableData: [
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
        {
          name: '天气预报',
          desc: '查询指定城市的天气预报',
          author: '@彩铅木流年',
          documentUrl: '',
          downloadUrl: '/qqbot/static/file/weather.zip',
        },
      ]
    }
  }
}
