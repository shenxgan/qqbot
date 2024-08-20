import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Python QQbot",
  description: "python learning qqbot",
  lang: "zh-CN",
  base: '/qqbot/',
  lastUpdated: true,
  head: [
    ['link', { rel: 'icon', href: '/static/img/logo.png' }],
    ['link', { rel: 'stylesheet', href: '/static/css/style.css' }],
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
  themeConfig: {
    logo: '/static/img/logo.png',
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: '指南', link: '/guide/5170' },
      { text: '插件', link: '/plugin/3490' }
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
          ]
        }
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
