# ss7_python
- SS7 Op.Python実行がそのままだと勝手にディレクトリを移動し、実行した場所からの相対パスでの指定が出来なくなるので、最初のワーキングディレクトリを記憶し、相対パスでの指定を出来るようにしたラッパーです。
- 実行にはSs7Python.pydとSs7WrapCmd.dllがディレクトリ直下に必要です。