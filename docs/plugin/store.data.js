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
        {
          name: '点歌',
          desc: '点歌后发送歌曲语音到群里',
          author: '@只会敲键盘的猿人',
          documentUrl: '',
          downloadUrl: '/qqbot/static/file/choose_a_song_v1.0.1.zip',
        },
        {
          name: '快递查询',
          desc: '查询快递物流信息',
          author: '@只会敲键盘的猿人',
          documentUrl: '',
          downloadUrl: '/qqbot/static/file/GetExpress_v1.0.0.zip',
        },
        {
          name: '疯狂星期四',
          desc: '在星期四的时候，识别关键字后发送疯狂星期四语录',
          author: '@古一',
          documentUrl: '',
          downloadUrl: '/qqbot/static/file/kfc.zip',
        },
        {
          name: '复读机',
          desc: '检测到复读机行为时，自动跟一条',
          author: '@古一',
          documentUrl: '',
          downloadUrl: '/qqbot/static/file/plus1.zip',
        },
        {
          name: 'IP 归属地查询',
          desc: '查询给定 IP 地址的归属地信息',
          author: '@快乐哈哈',
          documentUrl: '',
          downloadUrl: '/qqbot/static/file/ip.zip',
        },
      ]
    }
  }
}
