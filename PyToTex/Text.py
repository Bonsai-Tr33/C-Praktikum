from PyToTex import SendToTex
Mail = SendToTex('/Users/Moritz/Library/CloudStorage/OneDrive-Personal/Dokumente/Uni/Qutie FS5/C-Praktikum/PyToTex/Data')
Mail.SendValue(15, 'Nummer')
Mail.SendTable(2, ['col1', 'col2'], [[1,2,3,4,5],[10,20,30,40,50]], 'Liste')