using System;
using Gtk;
using System.Diagnostics;

public partial class MainWindow: Gtk.Window
{	
	private Boolean inLaunch;
	/// <summary>
	/// Initializes a new instance of the <see cref="MainWindow"/> class.
	/// </summary>
	public MainWindow(): base (Gtk.WindowType.Toplevel)
	{
		Build();
		this.Title = "Flash Mission Control";
		this.inLaunch = false;
	}

	/// <summary>
	/// Cleans up the window session
	/// </summary>
	/// <param name='sender'>Sender.</param>
	/// <param name='a'>A.</param>
	protected void OnDeleteEvent(object sender, DeleteEventArgs a)
	{
		Process.Start("thunderPyController.py", "-s");
		Application.Quit();
		a.RetVal = true;
	}
	
	/// <summary>
	/// Launches the missile.
	/// </summary>
	/// <param name='sender'>The calling event.</param>
	/// <param name='e'>The event arguments</param>
	protected void Launch(object sender, EventArgs e)
	{
		Process.Start("thunderPyController.py", "-f");
		this.inLaunch = true;
		System.Threading.Thread.Sleep(4000);
		this.inLaunch = false;
	}

	/// <summary>
	/// Moves the turret up.
	/// </summary>
	/// <param name='sender'>The calling event.</param>
	/// <param name='e'>The event arguments</param>
	protected void MoveUp(object sender, EventArgs e)
	{
		if(!inLaunch)
			Process.Start("thunderPyController.py", "-c -u");
	}
	
	/// <summary>
	/// Moves the turret right.
	/// </summary>
	/// <param name='sender'>The calling event.</param>
	/// <param name='e'>The event arguments</param>
	protected void MoveRight(object sender, EventArgs e)
	{
		if(!inLaunch)
			Process.Start("thunderPyController.py", "-c -r");
	}
	
	/// <summary>
	/// Moves the turret down.
	/// </summary>
	/// <param name='sender'>The calling event.</param>
	/// <param name='e'>The event arguments</param>
	protected void MoveDown(object sender, EventArgs e)
	{
		if(!inLaunch)
			Process.Start("thunderPyController.py", "-c -d");
	}
	
	/// <summary>
	/// Moves the turret left.
	/// </summary>
	/// <param name='sender'>The calling event.</param>
	/// <param name='e'>The event arguments</param>
	protected void MoveLeft(object sender, EventArgs e)
	{
		if(!inLaunch)
			Process.Start("thunderPyController.py", "-c -l");
	}

	/// <summary>
	/// Stops all current movement.
	/// </summary>
	/// <param name='sender'>The calling event.</param>
	/// <param name='e'>The event arguments</param>
	protected void Stop(object sender, EventArgs e)
	{
		if(!inLaunch)
			Process.Start("thunderPyController.py", "-s");
	}
}
