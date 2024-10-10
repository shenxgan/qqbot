// .vitepress/theme/index.js
import DefaultTheme from 'vitepress/theme'
import "element-plus/dist/index.css";

/** @type {import('vitepress').Theme} */
export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // 注册自定义全局组件
    // app.component('MyGlobalComponent' /* ... */)
    import("element-plus").then((module) => {
      app.use(module);
    });
  }
}
