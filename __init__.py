"""SS7 Op.Python実行を使いやすくするためのモジュール

To do:
    * SS7 1.1.1.19以降をインストールする
    * SS7 Op.Python実行のライセンスを取得する
    * Microsoft版でない公式版Python3.9で実行する
"""

import os
from . import Ss7Python
from typing import Callable
from functools import wraps


def raise_error(func) -> Callable:
    """都度エラーを確認するためのデコレータ"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> bool:
        self: SS7_Python = args[0]
        if self.data is None:
            return True
        else:
            func(*args, **kwargs)
            return self.isError()
    return wrapper


class SS7_Python:
    """SS7 Op.Python実行を使いやすくするためのクラス

        Attributes:
            data: 読み込んだ物件データ
            cwd: Current Working Directory. Ss7Pythonモジュールがワーキングディレクトリを移動するため、相対パスでのパス指定を実現するために必要

    解析実行、CSV出力などが出来る。
    各関数はエラーでTrueを返す。
    """
    data: Ss7Python.Ss7Data = None
    cwd: str = os.getcwd()

    def __init__(
        self,
        relative_path: str,
    ) -> None:
        """SS7 Op.Python実行を扱うためのクラス

        Args:
            - relative_path:
                - 読み込む物件のディレクトリ「????.ikn」の相対パス
                - `.csv`の場合、csvファイルを読み取ってSS7ファイルを生成する。
        """
        abs_path: str = self.absolute_path(relative_path)
        Ss7Python.Init()
        Ss7Python.Start(None, 1)
        if self.isError():
            raise Exception()
        elif relative_path.endswith(".ikn"):
            self.data = Ss7Python.Open(abs_path, 2, 2)
            self.isError()
        elif relative_path.endswith(".csv"):
            abs_path = Ss7Python.CreateDataCsv(abs_path, abs_path.replace(".csv", ".ikn"), 1)
            self.data = Ss7Python.Open(abs_path, 2, 2)
            self.isError()

    def absolute_path(self, relative_path: str) -> str:
        return os.path.realpath(os.path.join(self.cwd, relative_path))

    def isError(self) -> bool:
        err: Ss7Python.Ss7ErrInfo = Ss7Python.GetLastError()
        if not err.IsOK():
            print(err.GetErrorMessage())
            return True
        else:
            return False

    @raise_error
    def calculate(self, result: str, calculation: str) -> None:
        """<result>で指定した結果に、<calculation>で指定した解析を実行して保存する

        Args:
            - result:
                - 結果1
                - 結果2
                - 結果3
                - 結果4
                - 結果5
            - calculation
                - 準備計算
                - 応力解析(一次)
                - 偏心率・剛性率
                - 基礎による応力
                - 断面算定
                - 耐力計算
                - 応力解析(二次)
                - 必要保有水平耐力
                - 積算
        """
        self.data.Calculate(result, calculation)

    @raise_error
    def save(self) -> None:
        self.data.Save()

    @raise_error
    def restore(self, result: str) -> None:
        self.data.Restore(result)

    @raise_error
    def delete_result(self, result: str) -> None:
        self.data.DeleteResult(result)

    @raise_error
    def create_document(self, result: str, relative_path: str) -> None:
        self.data.GetResultData(result).CreateDocument(None, self.absolute_path(relative_path), 1)

    @raise_error
    def export_input_csv(self, result: str, relative_path: str) -> None:
        """<result>で指定した結果の入力データを、<relative_path>に保存する。

        Args:
            - result
                - 結果1
                - 結果2
                - 結果3
                - 結果4
                - 結果5
            - relative_path 保存するファイルの相対パス
        """
        self.data.GetResultData(result).ExportInputCsv(self.absolute_path(relative_path), 1, 1)

    @raise_error
    def export_result_csv(self, result: str, relative_path: str, outputs: str = None) -> None:
        """<result>で指定した結果を、<relative_path>に保存する。

        Args:
            - result
                - 結果1
                - 結果2
                - 結果3
                - 結果4
                - 結果5
            - relative_path: 保存するファイルの相対パス
            - outputs: 出力項目名
        """
        self.data.GetResultData(result).ExportResultCsv(outputs, self.absolute_path(relative_path), 1, 1, 1)

    @raise_error
    def export_cad7(self, result: str, relative_path: str) -> None:
        self.data.GetResultData(result).ExportCad7(self.absolute_path(relative_path), 1)

    def __del__(self) -> None:
        if self.data is not None:
            self.save()
            self.data.Close(2)
        Ss7Python.End(2)
