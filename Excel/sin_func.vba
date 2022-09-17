Function sin_bstr(x As Double, Optional b As String = "10", Optional v As Double = 0.125) As Double
  Dim xr As Double
  Dim nx As Integer
  Dim nxr As Integer
  Dim pi As Double
  Dim blen As Integer
  Dim wsel() As Integer
  Dim wn As Integer
  
  pi = 4 * Atn(1)
  blen = Len(b)
  wsel() = wave_select(b)
  nx = Int(x / (blen * pi))
  xr = x - (nx * blen * pi)
  nxr = Int(2 * xr / pi)
  wn = wsel(nxr + 1)
  If wn = 3 Then
    sin_bstr = 1 - v * (1 + Cos(2 * xr))
  ElseIf wn = 2 Then
    sin_bstr = -Sin(xr)
  ElseIf wn = 1 Then
    sin_bstr = Sin(xr)
  Else
    sin_bstr = -1 + v * (1 + Cos(2 * xr))
  End If
End Function

Function wave_select(b As String) As Integer()
  Dim blen As Integer
  Dim slen As Integer
  Dim slist() As Integer
  Dim sidx As Integer
  Dim bstr As String
  Dim b0, b1 As String
  Dim ib As Integer
  blen = Len(b)
  slen = 2 * blen
  bstr = Right(b, 1) & b & Left(b, 1)
  ReDim slist(slen)
  sidx = 1
  For ib = 1 To blen
    b0 = Mid(bstr, ib, 2)
    b1 = Mid(bstr, ib + 1, 2)
    If b0 = "01" And (ib Mod 2) = 1 Then
      slist(sidx) = 1
    ElseIf b0 = "01" Then
      slist(sidx) = 2
    ElseIf b0 = "10" And (ib Mod 2) = 1 Then
      slist(sidx) = 2
    ElseIf b0 = "10" Then
      slist(sidx) = 1
    ElseIf b0 = "11" Then
      slist(sidx) = 3
    Else
      slist(sidx) = 0
    End If
    sidx = sidx + 1
    If b1 = "01" And (ib Mod 2) = 1 Then
      slist(sidx) = 2
    ElseIf b1 = "01" Then
      slist(sidx) = 1
    ElseIf b1 = "10" And (ib Mod 2) = 1 Then
      slist(sidx) = 1
    ElseIf b1 = "10" Then
      slist(sidx) = 2
    ElseIf b1 = "11" Then
      slist(sidx) = 3
    Else
      slist(sidx) = 0
    End If
    sidx = sidx + 1
  Next ib
  wave_select = slist()
End Function
