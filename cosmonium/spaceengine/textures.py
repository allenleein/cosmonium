from __future__ import print_function
from __future__ import absolute_import

from ..textures import VirtualTextureSource, TextureSourceFactory, AutoTextureSource
from ..dircontext import defaultDirContext

import os

class SpaceEngineVirtualTextureSource(VirtualTextureSource):
    face_str = [
                #SE Axis :
                # X : Right -> X
                # Y : Up -> Z
                # Z : Forward -> -Y
                'pos_x',
                'neg_x',
                'pos_z',
                'neg_z',
                'pos_y',
                'neg_y',
                ]

    def __init__(self, root, ext, size, channel=None, alpha_channel=None, attribution=None):
        VirtualTextureSource.__init__(self, root, ext, size, attribution)
        self.channel = channel
        self.alpha_channel = alpha_channel
        if channel is None:
            self.channel_text = ''
        else:
            self.channel_text = '_' + channel
        if self.alpha_channel is None:
            self.alpha_channel_text = ''
        else:
            self.alpha_channel_text = '_' + alpha_channel

    def child_texture_name(self, patch):
        dir_name = self.face_str[patch.face]
        return self.root + '/' + dir_name + "/%d_%d_%d%s.%s" % (patch.lod + 1, patch.y * 2, patch.x * 2, self.channel_text, self.ext)

    def texture_name(self, patch):
        dir_name = self.face_str[patch.face]
        return self.root + '/' + dir_name + "/%d_%d_%d%s.%s" % (patch.lod, patch.y, patch.x, self.channel_text, self.ext)

    def alpha_texture_name(self, patch):
        if self.alpha_channel is not None:
            dir_name = self.face_str[patch.face]
            return self.root + '/' + dir_name + "/%d_%d_%d%s.%s" % (patch.lod, patch.y, patch.x, self.alpha_channel_text, self.ext)

class SpaceEngineTextureSourceFactory(TextureSourceFactory):
    def create_source(self, filename, context=defaultDirContext):
        filename = context.find_texture(filename)
        if os.path.isdir(filename):
            all_faces = True
            for face in SpaceEngineVirtualTextureSource.face_str:
                if not os.path.isdir(os.path.join(filename, face)):
                    all_faces = False
            if all_faces:
                channel = None
                alpha_channel = None
                if os.path.exists(os.path.join(filename, 'base.jpg')):
                    channel = ''
                else:
                    if os.path.exists(os.path.join(filename, 'base_c.jpg')):
                        channel = 'c'
                    if os.path.exists(os.path.join(filename, 'base_a.jpg')):
                        alpha_channel = 'a'
                return SpaceEngineVirtualTextureSource(filename, 'jpg', 258, channel, alpha_channel)
        return None

#TODO: Should be done in Cosmonium main class
AutoTextureSource.register_source_factory(SpaceEngineTextureSourceFactory(), [], 1)
