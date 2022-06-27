namespace HeartRate
{
    partial class HeartRateForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(HeartRateForm));
            this.uxBpmNotifyIcon = new System.Windows.Forms.NotifyIcon(this.components);
            this.uxNotifyIconContextMenu = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.selectIconFontToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.editFontColorToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.editIconFontWarningColorToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem2 = new System.Windows.Forms.ToolStripSeparator();
            this.selectWindowFontToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.doNotScaleFontToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.editWindowFontColorToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.editWindowFontWarningColorToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.textAlignmentToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripSeparator1 = new System.Windows.Forms.ToolStripSeparator();
            this.setCSVOutputFileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.unsetCSVOutputFileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.setHeartRateFileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.unsetHeartRateFileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.setIBIFileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.unsetIBIFileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem3 = new System.Windows.Forms.ToolStripSeparator();
            this.selectBackgroundImageToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.removeBackgroundImageToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.backgroundImagePositionToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem1 = new System.Windows.Forms.ToolStripSeparator();
            this.uxEditSettingsMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.uxExitMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.uxBpmLabel = new System.Windows.Forms.Label();
            this.uxNotifyIconContextMenu.SuspendLayout();
            this.SuspendLayout();
            // 
            // uxBpmNotifyIcon
            // 
            this.uxBpmNotifyIcon.ContextMenuStrip = this.uxNotifyIconContextMenu;
            this.uxBpmNotifyIcon.Text = "notifyIcon1";
            this.uxBpmNotifyIcon.Visible = true;
            this.uxBpmNotifyIcon.MouseClick += new System.Windows.Forms.MouseEventHandler(this.uxBpmNotifyIcon_MouseClick);
            // 
            // uxNotifyIconContextMenu
            // 
            this.uxNotifyIconContextMenu.ImageScalingSize = new System.Drawing.Size(20, 20);
            this.uxNotifyIconContextMenu.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {

            this.uxEditSettingsMenuItem,
            this.uxExitMenuItem});


            // 
            // toolStripMenuItem1
            // 
            this.toolStripMenuItem1.Name = "toolStripMenuItem1";
            this.toolStripMenuItem1.Size = new System.Drawing.Size(246, 6);
            // 
            // uxEditSettingsMenuItem
            // 
            this.uxEditSettingsMenuItem.Name = "uxEditSettingsMenuItem";
            this.uxEditSettingsMenuItem.Size = new System.Drawing.Size(249, 22);
            this.uxEditSettingsMenuItem.Text = "Edit settings XML...";
            this.uxEditSettingsMenuItem.Click += new System.EventHandler(this.uxMenuEditSettings_Click);
            // 
            // uxExitMenuItem
            // 
            this.uxExitMenuItem.Name = "uxExitMenuItem";
            this.uxExitMenuItem.Size = new System.Drawing.Size(249, 22);
            this.uxExitMenuItem.Text = "Exit";
            this.uxExitMenuItem.Click += new System.EventHandler(this.uxExitMenuItem_Click);
            // 
            // uxBpmLabel
            // 
            this.uxBpmLabel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.uxBpmLabel.ContextMenuStrip = this.uxNotifyIconContextMenu;
            this.uxBpmLabel.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.uxBpmLabel.Font = new System.Drawing.Font("Ubuntu Mono", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.uxBpmLabel.Location = new System.Drawing.Point(0, 0);
            this.uxBpmLabel.Name = "uxBpmLabel";
            this.uxBpmLabel.Size = new System.Drawing.Size(309, 130);
            this.uxBpmLabel.TabIndex = 0;
            this.uxBpmLabel.Text = "Starting...";
            this.uxBpmLabel.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.uxBpmLabel.UseCompatibleTextRendering = true;
            this.uxBpmLabel.Click += new System.EventHandler(this.uxBpmLabel_Click);
            // 
            // HeartRateForm
            // 
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.None;
            this.ClientSize = new System.Drawing.Size(308, 129);
            this.ContextMenuStrip = this.uxNotifyIconContextMenu;
            this.Controls.Add(this.uxBpmLabel);
            this.Font = new System.Drawing.Font("Ubuntu Mono", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "HeartRateForm";
            this.ShowInTaskbar = false;
            this.Text = "Heart rate monitor";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.HeartRateForm_FormClosing);
            this.Load += new System.EventHandler(this.HeartRateForm_Load);
            this.ResizeEnd += new System.EventHandler(this.HeartRateForm_ResizeEnd);
            this.uxNotifyIconContextMenu.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion
        private System.Windows.Forms.NotifyIcon uxBpmNotifyIcon;
        private System.Windows.Forms.Label uxBpmLabel;
        private System.Windows.Forms.ContextMenuStrip uxNotifyIconContextMenu;
        private System.Windows.Forms.ToolStripMenuItem uxEditSettingsMenuItem;
        private System.Windows.Forms.ToolStripMenuItem uxExitMenuItem;
        private System.Windows.Forms.ToolStripMenuItem editFontColorToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem editIconFontWarningColorToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem editWindowFontColorToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem editWindowFontWarningColorToolStripMenuItem;
        private System.Windows.Forms.ToolStripSeparator toolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem selectIconFontToolStripMenuItem;
        private System.Windows.Forms.ToolStripSeparator toolStripMenuItem2;
        private System.Windows.Forms.ToolStripMenuItem selectWindowFontToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem selectBackgroundImageToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem removeBackgroundImageToolStripMenuItem;
        private System.Windows.Forms.ToolStripSeparator toolStripSeparator1;
        private System.Windows.Forms.ToolStripMenuItem textAlignmentToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem backgroundImagePositionToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem doNotScaleFontToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem setCSVOutputFileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem unsetCSVOutputFileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem setHeartRateFileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem unsetHeartRateFileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem unsetIBIFileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem setIBIFileToolStripMenuItem;
        private System.Windows.Forms.ToolStripSeparator toolStripMenuItem3;
    }
}

