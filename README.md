# Blender_Audiowave_Extension
a poweful and customizable animation curve from audio generator for blender

![exemple of the extension in action](https://cdn.discordapp.com/attachments/725041161001107456/1249000537563861173/clipboard.png?ex=6665b5e5&is=66646465&hm=284db788010f7086ac08133e9480d8a2fee86e57419dc1496d2a48395c5656f8&)

## Depensencies
this extension heavily relies on scipy, for the savgol_filter and the fast fourier transform.

## installation
first **make sure you're using blender 4.2 or later with extensions support enabled**
```bash
git clone https://github.com/heredos/Blender_Audiowave_Extension.git
cd Blender_Audiowave_Extension
```
grab the [latest scipy release wheels for your platform](https://github.com/scipy/scipy/releases), and put it in wheels.  
then, open blender_manifest.toml, scroll all the way down to the "wheels" part line 50, and replace the paths by the path to the wheel you just downloaded.  
go back to your terminal, and run `blender --command extension build`
it should give you a zip.  
now, open blender, go to Edit>preferences>Extensions, click on the down arrow in the top right corner, and Install from disk. Now, navigate to the zip file you just created and you should be good to go!  

## usage
create an fcurve, open it in the graph editors, go to the modifiers and click the generate curve button.  
you'll see a little redo panel in the bottom left corner of the curve editor, open it, tweak the settings, select a file, and boom, you got a curve, just like that.  
while you *can* modify the settings after a file has been selected, that does not mean you *should*. it can take 2~3 seconds to generate a 7 minute audio curve on a decent computer, but if you want to do it anyway, do it with your keyboard instead of your mouse, it'll be easier to get to the expected result.

## More on this project
this was made during my 2 month internship at WEGL, a 3d and fx company (more or less, i think, they do a ton of stuff), and is more or less my first blender addon, so there may be a lot of things to improve.  

## why can't i find it on the blender extension store?
because the scipy wheels are too big.  
the maximum size for an extension there is 10mb, and a single scipy wheel is over 30mb. And i would need 5 wheels in total to make it work everywhere. If you're a blender extension store developper reading this, please increase the limit or set a pip packages to install field in the manifest, and i'd gladly publish it!
