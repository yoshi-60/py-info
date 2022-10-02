Sub jump_cell(ctag As String)
  Dim wb1 As Workbook
  Dim wb2 As Workbook
  Dim ws1 As Worksheet
  Dim ws2 As Worksheet
  Dim wc1 As Range
  Dim wc2 As Range
  Dim bname As String
  Dim sname As String
  Dim cname As String
  Dim rnum As Long
  Dim cnum As Long

  bname = Range("D3").Value
  Set wb1 = ThisWorkbook
  Set ws1 = wb1.Worksheets("ShowWs")
  Set wb2 = Workbooks(bname)

  rnum = ws1.Range(ctag).Row
  cnum = ws1.Range(ctag).Column
  sname = ws1.Cells(rnum, cnum + 2).Value
  cname = ws1.Cells(rnum, cnum + 3).Value
  
  Set ws2 = wb2.Worksheets(sname)
  wb2.Activate
  ws2.Activate
  ws2.Range(cname).Select
  
End Sub

Sub jump_init()
  Dim r As Long
  Dim c As Long
  r = 6
  c = 6
  ActiveSheet.Shapes("ボタン1").OnAction = "ShowWs.xlsm!'jump_cell ""B7""'"
  ActiveSheet.Shapes("ボタン2").OnAction = "ShowWs.xlsm!'jump_cell ""B8""'"
  ActiveSheet.Shapes("ボタン3").OnAction = "ShowWs.xlsm!'jump_cell ""B9""'"
  ActiveSheet.Shapes("ボタン1").TextFrame.Characters.Text = Cells(r + 1, c).Value
  ActiveSheet.Shapes("ボタン2").TextFrame.Characters.Text = Cells(r + 2, c).Value
  ActiveSheet.Shapes("ボタン3").TextFrame.Characters.Text = Cells(r + 3, c).Value
End Sub
