import aud
import bpy
from bpy_extras.io_utils import ImportHelper
import mathutils

from scipy.fftpack import fft
from scipy.signal import savgol_filter
import numpy as np


class GRAPH_OT_sound_curve(bpy.types.Operator):
    bl_idname = "graph.sound_curve"
    bl_label = "transform a fcurve into an audio vizualizer"
    bl_options = {'REGISTER', 'UNDO'}
    
    multiplier: bpy.props.FloatProperty(
        name="multiplier",
        description="the maximum height of the curve",
        default=1.,
    )
    sample_size: bpy.props.FloatProperty(
        name = "sample_size",
        description = "the size of the sample.\nbigger sample size can get a higher frequency range but tend to smoothe kicks and fast high-pitched loud sounds.",
        default = 0.3,
        min=0.001,
    )
    min_freq: bpy.props.IntProperty(
        name="minimum_frequency",
        description="the lower limit of the frequencies to get.\nthe human ear usually cannot hear under 20hz",
        default=20,
        min=0
    )
    max_freq: bpy.props.IntProperty(
        name="maximum_frequency",
        description="the higher limit of the frequencies to get.\nthe human ear usually cannot hear over 20000hz",
        default=20000,
        min=1,
    )
    smoothing: bpy.props.IntProperty(
        name="smooth_factor",
        description="the window size to smoothe the curve, 1 for none",
        default=30,
        min=1,
    )
    polynomial: bpy.props.IntProperty(
        name="smooth_quality",
        description="the polynomial factor of the smoothing, think of it as a quality slider.\nmust be smaller than the smooth factor",
        default=3,
        min=1,
    )
    file: bpy.props.StringProperty(
        name="file",
        description="the file path for the audio file to process",
        subtype="FILE_PATH",
        default="",
    )
    
    @classmethod
    def poll(cls, context):
        print(type(context.selected_visible_fcurves), len(context.selected_visible_fcurves))
        if type(context.visible_fcurves)!=list:
            print("no")
            return False 
        elif len(context.selected_visible_fcurves)>0:
            print("yes")
            return True
        else:
            print("nono")
            return False
    
    def execute(self, context):
        if (self.file!=""):
            #create the audio device for audio preview
            #device = aud.Device()

            # load the sound to analyze
            sound = aud.Sound(bpy.path.abspath(self.file)).rechannel(1).cache()

            # play the audio preview
            #handle = device.play(sound)
            data = sound.data()
            rate = sound.specs[0]

            #extract the first part of the audio for numpy, the second part being the datatype
            a=data[0:,0]
            #this naïve approch vas 10x slower
            """
            c=fft(a)
            d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
            plt.plot(abs(c[:(d-1)]))
            plt.show()
            """

            # inintialize the parameters
            mult = self.multiplier
            sample_size=int(self.sample_size*rate)
            step=int(rate//bpy.context.scene.render.fps)
            ptr=sample_size
            lo_freq=self.min_freq
            hi_freq=self.max_freq
            decay = 0.1
            stay = 0.5
            rstay = bpy.context.scene.render.fps*stay
            maxfreq=[]

            #compute the max of the fft for every frame
            while ptr<len(data):
                c=fft(a[ptr-sample_size:ptr])
                d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
                r=abs(c[:(d-1)])
                maxfreq.append(max(r[lo_freq:hi_freq]))
                ptr+=step
            #normalize it all
            m=max(maxfreq)
            m2=maxfreq/m*mult

            #smoothe the output to make it less jiggly
            smoothing_window_size=self.smoothing
            polynomial_order = self.polynomial
            m3=savgol_filter(m2, smoothing_window_size, polynomial_order)
            #clear the current fcurve
            c=bpy.data.actions['CubeAction'].fcurves[0]
            c.convert_to_keyframes(0, len(m3)+1)
            k=c.keyframe_points
            k.clear()
            #add all they keyframes we need
            k.add(len(m3))

            for i in range(len(m3)):
                k[i].co=mathutils.Vector([i, m3[i]])
                
            #concert it back to samples to avoid modifications
            c.convert_to_samples(0,len(m3)+1)
            #plt.plot(m2,'r')
            #plt.show()    
            #device.stopAll()
        return {'FINISHED'}

# add all that cool stuff to the modifiers panel of the graph editor
class GRAPH_PT_sound_curve(bpy.types.Panel):
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Modifiers"
    bl_label = "audio anim"
    
    def draw(self, context):
        row=self.layout.row()
        row.operator("graph.sound_curve",text="generate curve",icon="IPO_ELASTIC")

#tell blender to actually use all of that
def register():
    bpy.utils.register_class(GRAPH_PT_sound_curve)
    bpy.utils.register_class(GRAPH_OT_sound_curve)
def unregister():
    bpy.utils.unregister_class(GRAPH_PT_sound_curve)
    bpy.utils.unregister_class(GRAPH_OT_sound_curve)
if __name__=="__main__":
    register()
