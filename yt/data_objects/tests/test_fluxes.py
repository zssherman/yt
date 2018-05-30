import os
import shutil
import tempfile

import numpy as np

from unittest import TestCase

from yt.testing import fake_random_ds, assert_almost_equal, assert_equal, \
    requires_file
from yt.convenience import load

def setup():
    from yt.config import ytcfg
    ytcfg["yt","__withintesting"] = "True"

def test_flux_calculation():
    ds = fake_random_ds(64, nprocs=4)
    dd = ds.all_data()
    surf = ds.surface(dd, "x", 0.51)
    assert_equal(surf["x"], 0.51)
    flux = surf.calculate_flux("ones", "zeros", "zeros", "ones")
    assert_almost_equal(flux.value, 1.0, 12)
    assert_equal(str(flux.units), 'cm**2')

def test_sampling():
    ds = fake_random_ds(64, nprocs=4)
    dd = ds.all_data()
    for i, ax in enumerate('xyz'):
        surf = ds.surface(dd, ax, 0.51)
        surf.get_data(ax, "vertex")
        assert_equal(surf.vertex_samples[ax], surf.vertices[i,:])
        assert_equal(str(surf.vertices.units), 'code_length')
        dens = surf['density']
        vert_shape = surf.vertices.shape
        assert_equal(dens.shape[0], vert_shape[1]//vert_shape[0])
        assert_equal(str(dens.units), 'g/cm**3')

ISOGAL = 'IsolatedGalaxy/galaxy0030/galaxy0030'

class ExporterTests(TestCase):

    def setUp(self):
        self.curdir = os.getcwd()
        self.tmpdir = tempfile.mkdtemp()
        os.chdir(self.tmpdir)

    def tearDown(self):
        os.chdir(self.curdir)
        shutil.rmtree(self.tmpdir)

    def test_export_ply(self):
        ds = fake_random_ds(64, nprocs=4)
        dd = ds.all_data()
        surf = ds.surface(dd, 'x', 0.51)
        surf.export_ply('my_ply.ply', bounds=[(0, 1), (0, 1), (0, 1)])
        assert os.path.exists('my_ply.ply')
        surf.export_ply('my_ply2.ply', bounds=[(0, 1), (0, 1), (0, 1)],
                        sample_type='vertex', color_field='density')
        assert os.path.exists('my_ply2.ply')

    def test_export_obj(self):
        ds = fake_random_ds(16, nprocs=4, particles=16**3,
                            fields=("density", "temperature"),
                            units=('g/cm**3', 'K'))
        sp = ds.sphere("max", (1.0, "cm"))
        surf = ds.surface(sp, "density", 0.5)
        surf.export_obj("my_galaxy", transparency=1.0, dist_fac=1.0)
        assert os.path.exists('my_galaxy.obj')
        assert os.path.exists('my_galaxy.mtl')

        mi, ma = sp.quantities.extrema('temperature')
        rhos = [0.5, 0.25]
        trans = [0.5, 1.0]
        for i, r in enumerate(rhos):
            surf = ds.surface(sp,'density',r)
            surf.export_obj("my_galaxy_color".format(i),
                            transparency=trans[i],
                            color_field='temperature', dist_fac=1.0,
                            plot_index=i, color_field_max=ma,
                            color_field_min=mi)

        assert os.path.exists('my_galaxy_color.obj')
        assert os.path.exists('my_galaxy_color.mtl')

        def _Emissivity(field, data):
            return (data['density']*data['density'] *
                    np.sqrt(data['temperature']))
        ds.add_field("emissivity", sampling_type='cell', function=_Emissivity,
                     units=r"g**2*sqrt(K)/cm**6")
        for i, r in enumerate(rhos):
            surf = ds.surface(sp,'density',r)
            surf.export_obj("my_galaxy_emis".format(i),
                            transparency=trans[i],
                            color_field='temperature',
                            emit_field='emissivity',
                            dist_fac=1.0, plot_index=i)

        assert os.path.exists('my_galaxy_emis.obj')
        assert os.path.exists('my_galaxy_emis.mtl')

@requires_file(ISOGAL)
def test_correct_output_unit():
    # see issue #1368
    ds = load(ISOGAL)
    x = y = z = .5
    sp1 = ds.sphere((x,y,z), (300, 'kpc'))
    Nmax = sp1.max('HI_Density')
    sur = ds.surface(sp1,"HI_Density", .5*Nmax)
    sur['x'][0]

def test_correct_output_unit_fake_ds():
    # implementing test_correct_output_unit() with fake dataset
    ds = fake_random_ds(64, nprocs=4, particles=16**3)
    x = y = z = .5
    sp1 = ds.sphere((x, y, z), (300, 'kpc'))
    Nmax = sp1.max('density')
    sur = ds.surface(sp1, "density", .5*Nmax)
    sur['x'][0]

def test_radius_surface():
    # see #1407
    ds = fake_random_ds(64, nprocs=4, particles=16**3)
    reg = ds.all_data()
    sp = ds.sphere(ds.domain_center, (0.5, 'code_length'))
    for obj in [reg, sp]:
        for rad in [0.05, .1, .4]:
            surface = ds.surface(obj, 'radius', (rad, 'code_length'))
            assert_almost_equal(
                surface.surface_area.v, 4*np.pi*rad**2, decimal=2)
            verts = surface.vertices
            for i in range(3):
                assert_almost_equal(
                    verts[i, :].min().v, 0.5-rad, decimal=2)
                assert_almost_equal(
                    verts[i, :].max().v, 0.5+rad, decimal=2)
