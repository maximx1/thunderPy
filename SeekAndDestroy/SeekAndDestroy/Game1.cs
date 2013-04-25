#region Using Statements
using System;
using System.Diagnostics;

using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Storage;
using Microsoft.Xna.Framework.Input;

using SeekAndDestroy.Input;

#endregion

namespace SeekAndDestroy
{
	/// <summary>
	/// This is the main type for your game
	/// </summary>
	public class Game1 : Game
	{
		GraphicsDeviceManager graphics;
		SpriteBatch spriteBatch;
		private Boolean inLaunch;
		private Boolean moving;
		private InputController ctrl;
		private Color scrnColor;

		public Game1()
		{
			graphics = new GraphicsDeviceManager(this);
			Content.RootDirectory = "Content";	            
			graphics.IsFullScreen = false;	
			this.inLaunch = false;
			this.moving = false;
			this.ctrl = new InputController(InputController.InputDeviceType.KEYBOARD);
			Window.Title = "Seek and Destroy Thunder Command";
			this.scrnColor = Color.CornflowerBlue;
		}

		/// <summary>
		/// Allows the game to perform any initialization it needs to before starting to run.
		/// This is where it can query for any required services and load any non-graphic
		/// related content.  Calling base.Initialize will enumerate through any components
		/// and initialize them as well.
		/// </summary>
		protected override void Initialize()
		{
			// TODO: Add your initialization logic here
			base.Initialize();
				
		}

		/// <summary>
		/// LoadContent will be called once per game and is the place to load
		/// all of your content.
		/// </summary>
		protected override void LoadContent()
		{
			// Create a new SpriteBatch, which can be used to draw textures.
			spriteBatch = new SpriteBatch(GraphicsDevice);

			//TODO: use this.Content to load your game content here 
		}

		/// <summary>
		/// Unloads the content.
		/// </summary>
		protected override void UnloadContent()
		{
			base.UnloadContent();
			Process.Start("thunderPyController.py", "-s");
		}

		/// <summary>
		/// Allows the game to run logic such as updating the world,
		/// checking for collisions, gathering input, and playing audio.
		/// </summary>
		/// <param name="gameTime">Provides a snapshot of timing values.</param>
		protected override void Update(GameTime gameTime)
		{
			ctrl.GetState();

			// For Mobile devices, this logic will close the Game when the Back button is pressed
			if(ctrl.PAUSE)
			{
				Exit();
			}

			//Movement controls

			if(ctrl.LEFT && !moving)
			{
				MoveLeft();
			}

			if(this.moving && !ctrl.LEFT)
			{
				Stop();
			}

			if(ctrl.UP && !moving)
			{
				MoveUp();
			}

			if(this.moving && !ctrl.UP)
			{
				Stop();
			}
			
			if(ctrl.RIGHT && !moving)
			{
				MoveRight();
			}

			if(this.moving && !ctrl.RIGHT)
			{
				Stop();
			}

			if(ctrl.DOWN && !moving)
			{
				MoveDown();
			}

			if(this.moving && !ctrl.DOWN)
			{
				Stop();
			}

			///Launching
			if(ctrl.LSHIFT)
			{
				this.inLaunch = true;
				this.scrnColor = Color.Red;
				//System.Threading.Thread.Sleep(4000);
				Launch();
				this.inLaunch = false;
			}
			else
			{
				this.scrnColor = Color.CornflowerBlue;
			}

			// TODO: Add your update logic here			
			base.Update(gameTime);
		}

		/// <summary>
		/// This is called when the game should draw itself.
		/// </summary>
		/// <param name="gameTime">Provides a snapshot of timing values.</param>
		protected override void Draw(GameTime gameTime)
		{
			graphics.GraphicsDevice.Clear(this.scrnColor);
		
			//TODO: Add your drawing code here
            
			base.Draw(gameTime);
		}
	
		/// <summary>
		/// Launches the missile.
		/// </summary>
		protected void Launch()
		{
			Console.WriteLine("Boom");
			Process.Start("thunderPyController.py", "-f");
		}

		/// <summary>
		/// Moves the turret up.
		/// </summary>
		protected void MoveUp()
		{
			if(!inLaunch)
			{
				Process.Start("thunderPyController.py", "-c -u");
				this.moving = true;
			}
		}
		
		/// <summary>
		/// Moves the turret right.
		/// </summary>
		protected void MoveRight()
		{
			if(!inLaunch)
			{
				Process.Start("thunderPyController.py", "-c -r");
				this.moving = true;
			}
		}
		
		/// <summary>
		/// Moves the turret down.
		/// </summary>
		protected void MoveDown()
		{
			if(!inLaunch)
			{
				Process.Start("thunderPyController.py", "-c -d");
				this.moving = true;
			}
		}
		
		/// <summary>
		/// Moves the turret left.
		/// </summary>
		protected void MoveLeft()
		{
			if(!inLaunch)
			{
				Process.Start("thunderPyController.py", "-c -l");
				this.moving = true;
			}
		}

		/// <summary>
		/// Stops all current movement.
		/// </summary>
		protected void Stop()
		{
			if(!inLaunch)
			{
				Process.Start("thunderPyController.py", "-s");
				this.moving = false;
			}
		}
	}
}

