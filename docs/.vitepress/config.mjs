import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Python QQbot",
  description: "python learning qqbot",
  lang: "zh-CN",
  base: '/qqbot/',
  lastUpdated: true,
  head: [
    ['link', { rel: 'icon', href: '/qqbot/static/img/logo.png' }],
    ['link', { rel: 'stylesheet', href: '/qqbot/static/css/style.css' }],
    [
      'script',
      { async: '', src: 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3829557881750869', crossorigin: 'anonymous' }
    ],
    [
      'script',
      { async: '', src: 'https://www.googletagmanager.com/gtag/js?id=G-KTBK3TKH1D' }
    ],
    [
      'script',
      {},
      `window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-KTBK3TKH1D');`
    ],
  ],
  cleanUrls: true,  // 干净的路由，不带 .html
  ignoreDeadLinks: true,
  themeConfig: {
    logo: '/static/img/logo.png',
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: '指南', link: '/guide/5170' },
      { text: '插件', link: '/plugin/3490' },
      { text: '插件市场', link: '/plugin/store' },
      { text: 'OneBot 11', link: '/onebot-11/README' },
      { text: 'QQ 群交流', link: 'http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=g6Fq9551gFIq6PyL0Q6JHTV9NPwuKVUk&authKey=38yO%2Bevi%2BxcvNLp87MouhCYhZuVQ7PePL974tCBbFSpCqTUKV8ErIdhEMrVmIPTs&noverify=0&group_code=855013471' },
    ],

    sidebar: {
      '/guide/': [
        {
          text: '介绍',
          items: [
            { text: '简要介绍', link: '/guide/5170' },
            { text: '安装使用', link: '/guide/7947' },
          ]
        }
      ],
      '/plugin/': [
        {
          text: '插件',
          items: [
            { text: '插件介绍', link: '/plugin/3490' },
            { text: '如何创建插件', link: '/plugin/5640' },
          ]
        },
        {
          text: '内置插件',
          items: [
            { text: 'Python 关键字', link: '/plugin/5941' },
            { text: '运行代码', link: '/plugin/0210' },
            { text: '成语接龙', link: '/plugin/1296' },
            { text: '豆包 AI', link: '/plugin/9234' },
            { text: '设置专属头衔', link: '/plugin/7595' },
            { text: '入群欢迎', link: '/plugin/4233' },
          ]
        }
      ],
      '/onebot-11/': [
        { text: 'OneBot 11 标准', link: 'https://github.com/botuniverse/onebot-11' },
        {
          text: '通信',
          collapsed: false,
          items: [
            { text: '通信概述', link: '/onebot-11/communication/README' },
            { text: 'HTTP', link: '/onebot-11/communication/http' },
            { text: 'HTTP POST', link: '/onebot-11/communication/http-post' },
            { text: '正向 WebSocket', link: '/onebot-11/communication/ws' },
            { text: '反向 WebSocket', link: '/onebot-11/communication/ws-reverse' },
            { text: '鉴权', link: '/onebot-11/communication/authorization' },
          ]
        },
        {
          text: '消息',
          collapsed: false,
          items: [
            { text: '消息概述', link: '/onebot-11/message/README' },
            { text: '字符串格式', link: '/onebot-11/message/string' },
            { text: '数组格式', link: '/onebot-11/message/array' },
            { text: '消息段类型', link: '/onebot-11/message/segment' },
          ]
        },
        {
          text: 'API',
          collapsed: false,
          items: [
            { text: 'API 概述', link: '/onebot-11/api/README' },
            { text: '公开 API', link: '/onebot-11/api/public' },
            { text: '隐藏 API', link: '/onebot-11/api/hidden' },
          ]
        },
        {
          text: '事件',
          collapsed: false,
          items: [
            { text: '事件概述', link: '/onebot-11/event/README' },
            { text: '消息事件', link: '/onebot-11/event/message' },
            { text: '通知事件', link: '/onebot-11/event/notice' },
            { text: '请求事件', link: '/onebot-11/event/request' },
            { text: '元事件', link: '/onebot-11/event/meta' },
          ]
        },
      ],
    },

    outline: {
      level: 'deep',
    },
    lastUpdated: {
      text: '最后更新于',
    },
    search: {
      provider: 'local'
    },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/shenxgan/qqbot' }
    ]
  }
})
