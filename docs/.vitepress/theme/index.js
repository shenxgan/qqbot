// .vitepress/theme/index.js
import DefaultTheme from 'vitepress/theme'
import "element-plus/dist/index.css";
import { ID_INJECTION_KEY } from 'element-plus'

/** @type {import('vitepress').Theme} */
export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // 注册自定义全局组件
    // app.component('MyGlobalComponent' /* ... */)

    // 当使用 Element Plus 在 SSR 场景下开发时，
    // 您需要在 SSR 期间进行特殊处理，以避免水合错误。
    // https://element-plus.org/zh-CN/guide/ssr.html
    // 除了添加 <ClientOnly> 之外，添加这个可以避免直接访问页面时，第一次无数据的情况；
    // 加上之后首次无论如何直接刷新都会有数据了
    app.provide(ID_INJECTION_KEY, {
      prefix: 1024,
      current: 0,
    });
    import("element-plus").then((module) => {
      app.use(module);
    });
  }
}
