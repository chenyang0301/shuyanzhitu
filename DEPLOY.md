# 官网 + Demo 上线教程（GitHub Pages，免费）

> 把 `website/` 下的 `index.html`、`beijing-demo.html`、`beijing-3d.html`、`beijing-3d-pro.html`
> 一起发布成一个公开网站，客户直接开链接就能看。

---

## 一、用 GitHub Pages 发布（海外，免费）

1. **注册 GitHub**：https://github.com （用常用邮箱注册）。
2. **新建仓库**：右上角 `New` → Repository name 填 `shuyanzhitu`（或 `company-site`）
   → 选 **Public** → 可选勾 `Add a README` → `Create repository`。
3. **上传文件**（最简单方式）：
   - 进仓库 → `Add file` → `Upload files`；
   - 把 `website/` 里这 4 个 html 文件**全选拖进去**；
   - 底部 `Commit changes` 提交。
   - ⚠️ 根目录必须有 `index.html`，否则访问不到首页。
4. **开启 Pages**：仓库 `Settings` → 左侧 `Pages`（或 `侧栏 Pages`）
   → Source 选 **main / master** 分支、目录 **/(root)** → `Save`。
5. **访问**：等 1–2 分钟，打开 `https://<你的用户名>.github.io/<仓库名>/` 即可。
6. 注意：Cesium / OSM 底图 / DataV 地图数据都**需联网**，确保访问环境可联网。

---

## 二、国内访问慢？换这些（任选其一）

- **码云 Gitee Pages**：国内快，需实名认证。
- **腾讯云静态网站托管 / 对象存储 COS + CDN**：稳定、国内快。
- **Vercel / Netlify**：海外免费，支持拖拽部署，体验好。
- 公司注册后：用园区给的服务器或自有云主机。

---

## 三、后续怎么更新

改完本地 html → 重新 `Upload files` / `git push` → GitHub Pages **自动更新**（通常几十秒）。

---

## 四、升级"真实建筑白模"（beijing-3d-pro.html）

1. 打开 https://ion.cesium.com 免费注册，复制你的 **Access Token**。
2. 用编辑器打开 `beijing-3d-pro.html`，把顶部
   `const ION_TOKEN = '';`
   的引号里填入你的 token：`const ION_TOKEN = '你的token';`
3. 重新上传该文件，访问它即可看到**真实地形 + OSM 建筑白模**。
4. 想让官网内嵌也升级：把 `index.html` 里 iframe 的 `src="beijing-3d.html"` 改成
   `src="beijing-3d-pro.html"`（前提是已填好 token）。

> 没 token 时，`beijing-3d-pro.html` 会自动用 OSM 公开影像兜底，不会白屏；
> 但地形和建筑白模必须填 token 才会出现。
