namespace MetaDataApp

partial class MainForm(System.Windows.Forms.Form):
	private components as System.ComponentModel.IContainer = null
	
	protected override def Dispose(disposing as bool):
		if disposing:
			if components is not null:
				components.Dispose()
		super(disposing)
	
	// This method is required for Windows Forms designer support.
	// Do not change the method contents inside the source code editor. The Forms designer might
	// not be able to load this method if it was changed manually.
	def InitializeComponent():
		self.btn_mySQL_connection = System.Windows.Forms.Button()
		self.label1 = System.Windows.Forms.Label()
		self.maskedTextBox_DSN = System.Windows.Forms.MaskedTextBox()
		self.listBox_tables = System.Windows.Forms.ListBox()
		self.button_deselect = System.Windows.Forms.Button()
		self.button_select = System.Windows.Forms.Button()
		self.listBox_spareTables = System.Windows.Forms.ListBox()
		self.label2 = System.Windows.Forms.Label()
		self.SuspendLayout()
		# 
		# btn_mySQL_connection
		# 
		self.btn_mySQL_connection.Location = System.Drawing.Point(13, 30)
		self.btn_mySQL_connection.Name = "btn_mySQL_connection"
		self.btn_mySQL_connection.Size = System.Drawing.Size(75, 23)
		self.btn_mySQL_connection.TabIndex = 0
		self.btn_mySQL_connection.Text = "mySQL"
		self.btn_mySQL_connection.UseVisualStyleBackColor = true
		self.btn_mySQL_connection.Click += self.Btn_mySQL_connectionClick as System.EventHandler
		# 
		# label1
		# 
		self.label1.Location = System.Drawing.Point(13, 8)
		self.label1.Name = "label1"
		self.label1.Size = System.Drawing.Size(78, 18)
		self.label1.TabIndex = 2
		self.label1.Text = "mySQL DSN:"
		# 
		# maskedTextBox_DSN
		# 
		self.maskedTextBox_DSN.Location = System.Drawing.Point(107, 5)
		self.maskedTextBox_DSN.Name = "maskedTextBox_DSN"
		self.maskedTextBox_DSN.Size = System.Drawing.Size(160, 20)
		self.maskedTextBox_DSN.TabIndex = 3
		# 
		# listBox_tables
		# 
		self.listBox_tables.FormattingEnabled = true
		self.listBox_tables.Location = System.Drawing.Point(107, 53)
		self.listBox_tables.Name = "listBox_tables"
		self.listBox_tables.Size = System.Drawing.Size(229, 95)
		self.listBox_tables.TabIndex = 4
		# 
		# button_deselect
		# 
		self.button_deselect.Location = System.Drawing.Point(357, 51)
		self.button_deselect.Name = "button_deselect"
		self.button_deselect.Size = System.Drawing.Size(32, 23)
		self.button_deselect.TabIndex = 5
		self.button_deselect.Text = ">>"
		self.button_deselect.UseVisualStyleBackColor = true
		self.button_deselect.Click += self.Button_deselectClick as System.EventHandler
		# 
		# button_select
		# 
		self.button_select.Location = System.Drawing.Point(357, 101)
		self.button_select.Name = "button_select"
		self.button_select.Size = System.Drawing.Size(32, 23)
		self.button_select.TabIndex = 6
		self.button_select.Text = "<<"
		self.button_select.UseVisualStyleBackColor = true
		self.button_select.Click += self.Button_selectClick as System.EventHandler
		# 
		# listBox_spareTables
		# 
		self.listBox_spareTables.FormattingEnabled = true
		self.listBox_spareTables.Location = System.Drawing.Point(421, 51)
		self.listBox_spareTables.Name = "listBox_spareTables"
		self.listBox_spareTables.Size = System.Drawing.Size(229, 95)
		self.listBox_spareTables.TabIndex = 7
		# 
		# label2
		# 
		self.label2.Font = System.Drawing.Font("Microsoft Sans Serif", 8.25, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, cast(System.Byte,0))
		self.label2.Location = System.Drawing.Point(155, 31)
		self.label2.Name = "label2"
		self.label2.Size = System.Drawing.Size(100, 20)
		self.label2.TabIndex = 8
		self.label2.Text = "Selected"
		self.label2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# MainForm
		# 
		self.AutoScaleDimensions = System.Drawing.SizeF(6, 13)
		self.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		self.ClientSize = System.Drawing.Size(792, 266)
		self.Controls.Add(self.label2)
		self.Controls.Add(self.listBox_spareTables)
		self.Controls.Add(self.button_select)
		self.Controls.Add(self.button_deselect)
		self.Controls.Add(self.listBox_tables)
		self.Controls.Add(self.maskedTextBox_DSN)
		self.Controls.Add(self.label1)
		self.Controls.Add(self.btn_mySQL_connection)
		self.Name = "MainForm"
		self.Text = "MetaData App - Creates SQLAlchemy MetaData from MSSQL/mySQL"
		self.ResumeLayout(false)
		self.PerformLayout()
	private label2 as System.Windows.Forms.Label
	private listBox_spareTables as System.Windows.Forms.ListBox
	private button_select as System.Windows.Forms.Button
	private button_deselect as System.Windows.Forms.Button
	private listBox_tables as System.Windows.Forms.ListBox
	private maskedTextBox_DSN as System.Windows.Forms.MaskedTextBox
	private label1 as System.Windows.Forms.Label
	private btn_mySQL_connection as System.Windows.Forms.Button

