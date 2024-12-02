# Python Package Example

## 示例内容说明

- 针对场景：可以发布到`PyPI`的`Python`库。

- 用法：创建`Github`仓库时可以选择为模板，已经创建仓库的可以手动参照调整。

- 需要注意修改的：`pyproject.toml` 和 `README` 中的名称和描述；`python_package` 文件夹重命名为库名

- 包含内容：`pdm` 配置（`pyproject.toml`）、文档结构（`README`、`CHANGELOG`、`docs`（用户文档））、代码目录结构（`tests`（单元测试）、`integrated_tests`（集成测试）、`examples`（用法示例））、`.gitignore`、`LICENSE`

- 备注：

    - 有测试数据文件要放时，在 `tests` 或 `integrated_tests` 目录下创建 `sample` 文件夹

    - 用户文档有图片时，在 `docs` 目录下创建 `images` 文件夹

