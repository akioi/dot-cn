# akioi.cn

一个恶搞项目，纯为好玩，请勿当真。

未来打算做到自动集成 + 泛域名解析， PR 被合并后服务器会自动部署。（不过得等域名备案搞完了再说 ... ）

### 原理

`gen.py` 会自动遍历 `src` 下目录的文件并找到对应的主题进行渲染，并自动部署到 Github Pages。

### 贡献

您可以贡献人物或主题。
详情可以参考 `src` 和 `themes` 下的示例。

详细注意事项您可以参考 wiki ，下面是一些简要的说明：
* 请您务必阅读 [ PR 的格式](https://github.com/akioi/dot-cn/wiki/PR-%E7%9A%84%E6%A0%BC%E5%BC%8F)
* 您在编写主题时可以使用 `{{ key }}` 的格式来获取配置中值为 `key` 的内容，如果不存在这样配置则不会被替换

### Demo

* owenowl.akioi.cn

### License

GPL-3.0