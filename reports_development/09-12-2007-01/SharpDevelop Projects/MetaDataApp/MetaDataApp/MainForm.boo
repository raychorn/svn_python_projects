namespace MetaDataApp

import System
import System.Collections
import System.Drawing
import System.Windows.Forms

import Microsoft.Data.Odbc

partial class MainForm:
	private global_spareList as List = []
	private global_tableList as List = []

	def constructor():
		// The InitializeComponent() call is required for Windows Forms designer support.
		InitializeComponent()
		maskedTextBox_DSN.Text = 'reports_development'
	
	private def connectionString():
		return "DSN=" + maskedTextBox_DSN.Text
		
	private def conn():
		return OdbcConnection(connectionString())
		
	private def Btn_mySQL_connectionClick(sender as object, e as System.EventArgs):
		reader as OdbcDataReader
		listBox_spareTables.DataSource = []
		cn = conn()
		cmd = OdbcCommand('SHOW TABLES')
		cmd.Connection = cn
		cn.Open()
		reader = cmd.ExecuteReader()
		while reader.Read():
			global_tableList.Add(reader.GetString(0))
		reader.Close()
		cn.Close()
		listBox_tables.DataSource = global_tableList.ToArray()
	
	private def Button_deselectClick(sender as object, e as System.EventArgs):
		global_spareList.Add(listBox_tables.Text)
		global_spareList.Sort()
		listBox_spareTables.DataSource = global_spareList.ToArray()
		i as int = global_tableList.IndexOf(listBox_tables.Text)
		global_tableList.RemoveAt(i)
		listBox_tables.DataSource = global_tableList.ToArray()
	
	private def Button_selectClick(sender as object, e as System.EventArgs):
		global_tableList.Add(listBox_spareTables.Text)
		global_tableList.Sort()
		listBox_tables.DataSource = global_tableList.ToArray()
		i as int = global_spareList.IndexOf(listBox_spareTables.Text)
		global_spareList.RemoveAt(i)
		listBox_spareTables.DataSource = global_spareList.ToArray()
	
[STAThread]
def Main(argv as (string)):
	Application.EnableVisualStyles()
	Application.SetCompatibleTextRenderingDefault(false)
	Application.Run(MainForm())

