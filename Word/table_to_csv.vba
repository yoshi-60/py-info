Sub tbl2csv()

  Dim myFD As FileDialog
  Dim myFDPath As String
  Dim myDoc As Document
  Dim myTbl As Table
  Dim myTblNum As Integer
  Dim myTblCnt As Integer
  Dim myOutFile As String
  Dim myOutPath As String
  Dim myOutFnum As Integer
  Dim rowNum As Long
  Dim colNum As Long
  Dim irow As Long
  Dim icol As Long
  Dim cellStr As String
  Dim rowStr As String
  
  'フォルダパスを設定
  myFDPath = "C:\Users\Ymorooka\Documents"
  '出力ファイル名を設定
  myOutFile = "WordTblOut.txt"

  'ファイルの選択ダイアログ
  Set myFD = Application.FileDialog(msoFileDialogFilePicker)

  'ダイアログボックスのタイトルを設定
  myFD.Title = "Wordファイルを選択してください"
  '複数ファイルの選択をオフ
  myFD.AllowMultiSelect = False
  '表示するファイルの種類の設定
  myFD.Filters.Clear
  myFD.Filters.Add "すべてのWordファイル", "*.doc; *.docx"
  '最初に表示するフォルダを設定
  myFD.InitialFileName = myFDPath
  'ファイルを選択して「OK」ボタンをクリックした場合の処理
  If myFD.Show = -1 Then
    Set myDoc = Documents.Open(myFD.SelectedItems(1))
    Debug.Print myDoc.Name
    MsgBox "ファイル： " & myDoc.Name & " を開きました。"
  Else
    MsgBox "終了します"
    Exit Sub
  End If
  
  '表示するファイルの種類の設定を解除
  myFD.Filters.Clear
  Set myFD = Nothing

  '出力ファイルの設定
  myOutPath = myDoc.Path & Application.PathSeparator & myOutFile
  Debug.Print myOutPath
  MsgBox "出力ファイル：" & myOutPath
  
  '表の数をカウント
  myTblNum = myDoc.Tables.Count
  MsgBox "表の数： " & myTblNum

  '出力ファイルオープン
  myOutFnum = FreeFile
  Open myOutPath For Output As myOutFnum

  '全ての表をループ
  myTblCnt = 0
  For Each myTbl In myDoc.Tables
    myTblCnt = myTblCnt + 1
    rowNum = myTbl.Rows.Count
    colNum = myTbl.Columns.Count
    'Debug.Print "No_" & myTblCnt, myTbl.ID, ":", myTbl.Title, ",", rowNum, ",", colNum
    'MsgBox "No_" & myTblCnt & myTbl.ID & ":" & myTbl.Title & "," & rowNum & "," & colNum
    Print #myOutFnum, "Table_No" & myTblCnt & "," & rowNum & "," & colNum
    For irow = 1 To rowNum
      rowStr = irow & ""
      For icol = 1 To colNum
        On Error Resume Next 'データが無い場合のエラー対策
        cellStr = myTbl.Cell(irow, icol).Range.Text
        'cellStr = myTbl.Rows(irow).Cells(icol).Range.Text
        If Err.Number = 0 Then
          cellStr = Left(cellStr, Len(cellStr) - 2) 'Wordのセル内の最終改行文字 Chr(13) & Chr(7) 削除
          cellStr = Replace(cellStr, vbCr, vbLf) 'Wordのセル内改行文字をExcelの改行文字に置換
        Else
          cellStr = ""
        End If
        rowStr = rowStr & "," & cellStr
        On Error GoTo 0
      Next icol
      Print #myOutFnum, rowStr
    Next irow
  Next myTbl
  
  'ファイルクローズ
  Close myOutFnum
  myDoc.Close SaveChanges:=False
  Set myDoc = Nothing

End Sub
