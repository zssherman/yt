"""
ART-specific fields

Author: Matthew Turk <matthewturk@gmail.com>
Affiliation: UCSD
Author: Chris Moody <matthewturk@gmail.com>
Affiliation: UCSC
Homepage: http://yt-project.org/
License:
  Copyright (C) 2010-2011 Matthew Turk.  All Rights Reserved.

  This file is part of yt.

  yt is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import numpy as np
from yt.data_objects.field_info_container import \
    FieldInfoContainer, \
    FieldInfo, \
    NullFunc, \
    TranslationFunc, \
    ValidateParameter, \
    ValidateDataField, \
    ValidateProperty, \
    ValidateSpatial, \
    ValidateGridType
import yt.data_objects.universal_fields
import yt.utilities.lib as amr_utils
from yt.utilities.physical_constants import mass_sun_cgs
from yt.frontends.art.definitions import *

KnownARTFields = FieldInfoContainer()
add_art_field = KnownARTFields.add_field
ARTFieldInfo = FieldInfoContainer.create_with_fallback(FieldInfo)
add_field = ARTFieldInfo.add_field

for f in fluid_fields:
    add_art_field(f, function=NullFunc, take_log=True,
                  validators=[ValidateDataField(f)])

def _convertDensity(data):
    return data.convert("Density")
KnownARTFields["Density"]._units = r"\rm{g}/\rm{cm}^3"
KnownARTFields["Density"]._projected_units = r"\rm{g}/\rm{cm}^2"
KnownARTFields["Density"]._convert_function = _convertDensity

def _convertTotalEnergy(data):
    return data.convert("GasEnergy")
KnownARTFields["TotalEnergy"]._units = r"\rm{g}\rm{cm}^2/\rm{s}^2"
KnownARTFields["TotalEnergy"]._projected_units = r"\rm{g}\rm{cm}^3/\rm{s}^2"
KnownARTFields["TotalEnergy"]._convert_function = _convertTotalEnergy

def _convertXMomentumDensity(data):
    tr = data.convert("Mass")*data.convert("Velocity")
    tr *= (data.convert("Density")/data.convert("Mass"))
    return tr
KnownARTFields["XMomentumDensity"]._units = r"\rm{g}/\rm{s}/\rm{cm}^3"
KnownARTFields["XMomentumDensity"]._projected_units = r"\rm{g}/\rm{s}/\rm{cm}^2"
KnownARTFields["XMomentumDensity"]._convert_function = _convertXMomentumDensity

def _convertYMomentumDensity(data):
    tr = data.convert("Mass")*data.convert("Velocity")
    tr *= (data.convert("Density")/data.convert("Mass"))
    return tr
KnownARTFields["YMomentumDensity"]._units = r"\rm{g}/\rm{s}/\rm{cm}^3"
KnownARTFields["YMomentumDensity"]._projected_units = r"\rm{g}/\rm{s}/\rm{cm}^2"
KnownARTFields["YMomentumDensity"]._convert_function = _convertYMomentumDensity

def _convertZMomentumDensity(data):
    tr = data.convert("Mass")*data.convert("Velocity")
    tr *= (data.convert("Density")/data.convert("Mass"))
    return tr
KnownARTFields["ZMomentumDensity"]._units = r"\rm{g}/\rm{s}/\rm{cm}^3"
KnownARTFields["ZMomentumDensity"]._projected_units = r"\rm{g}/\rm{s}/\rm{cm}^2"
KnownARTFields["ZMomentumDensity"]._convert_function = _convertZMomentumDensity

def _convertPressure(data):
    return data.convert("Pressure")
KnownARTFields["Pressure"]._units = r"\rm{g}/\rm{s}^2/\rm{cm}^1"
KnownARTFields["Pressure"]._projected_units = r"\rm{g}/\rm{s}^2"
KnownARTFields["Pressure"]._convert_function = _convertPressure

def _convertGamma(data):
    return 1.0
KnownARTFields["Gamma"]._units = r""
KnownARTFields["Gamma"]._projected_units = r""
KnownARTFields["Gamma"]._convert_function = _convertGamma

def _convertGasEnergy(data):
    return data.convert("GasEnergy")
KnownARTFields["GasEnergy"]._units = r"\rm{g}\rm{cm}^2/\rm{s}^2"
KnownARTFields["GasEnergy"]._projected_units = r"\rm{g}\rm{cm}^3/\rm{s}^2"
KnownARTFields["GasEnergy"]._convert_function = _convertGasEnergy

def _convertMetalDensitySNII(data):
    return data.convert('Density')
KnownARTFields["MetalDensitySNII"]._units = r"\rm{g}/\rm{cm}^3"
KnownARTFields["MetalDensitySNII"]._projected_units = r"\rm{g}/\rm{cm}^2"
KnownARTFields["MetalDensitySNII"]._convert_function = _convertMetalDensitySNII

def _convertMetalDensitySNIa(data):
    return data.convert('Density')
KnownARTFields["MetalDensitySNIa"]._units = r"\rm{g}/\rm{cm}^3"
KnownARTFields["MetalDensitySNIa"]._projected_units = r"\rm{g}/\rm{cm}^2"
KnownARTFields["MetalDensitySNIa"]._convert_function = _convertMetalDensitySNIa

def _convertPotentialNew(data):
    return data.convert("Potential")
KnownARTFields["PotentialNew"]._units = r"\rm{g}\rm{cm}^2/\rm{s}^2"
KnownARTFields["PotentialNew"]._projected_units = r"\rm{g}\rm{cm}^3/\rm{s}^2"
KnownARTFields["PotentialNew"]._convert_function = _convertPotentialNew

def _convertPotentialOld(data):
    return data.convert("Potential")
KnownARTFields["PotentialOld"]._units = r"\rm{g}\rm{cm}^2/\rm{s}^2"
KnownARTFields["PotentialOld"]._projected_units = r"\rm{g}\rm{cm}^3/\rm{s}^2"
KnownARTFields["PotentialOld"]._convert_function = _convertPotentialOld

####### Derived fields
def _temperature(field, data):
    tr = data["GasEnergy"]/data["Density"]
    tr /= data.pf.conversion_factors["GasEnergy"]
    tr *= data.pf.conversion_factors["Density"]
    tr *= data.pf.conversion_factors['tr']
    return tr

def _converttemperature(data):
    return 1.0
add_field("Temperature", function=_temperature,
          units=r"\mathrm{K}", take_log=True)
ARTFieldInfo["Temperature"]._units = r"\mathrm{K}"
ARTFieldInfo["Temperature"]._projected_units = r"\mathrm{K}"

def _metallicity_snII(field, data):
    tr = data["MetalDensitySNII"] / data["Density"]
    return tr
add_field("Metallicity_SNII", function=_metallicity_snII,
          units=r"\mathrm{K}", take_log=True)
ARTFieldInfo["Metallicity_SNII"]._units = r""
ARTFieldInfo["Metallicity_SNII"]._projected_units = r""

def _metallicity_snIa(field, data):
    tr = data["MetalDensitySNIa"] / data["Density"]
    return tr
add_field("Metallicity_SNIa", function=_metallicity_snIa,
          units=r"\mathrm{K}", take_log=True)
ARTFieldInfo["Metallicity_SNIa"]._units = r""
ARTFieldInfo["Metallicity_SNIa"]._projected_units = r""

def _metallicity(field, data):
    tr = data["Metal_Density"] / data["Density"]
    return tr
add_field("Metallicity", function=_metallicity,
          units=r"\mathrm{K}", take_log=True)
ARTFieldInfo["Metallicity"]._units = r""
ARTFieldInfo["Metallicity"]._projected_units = r""

def _x_velocity(field, data):
    tr = data["XMomentumDensity"]/data["Density"]
    return tr
add_field("x-velocity", function=_x_velocity,
          units=r"\mathrm{cm/s}", take_log=False)
ARTFieldInfo["x-velocity"]._units = r"\rm{cm}/\rm{s}"
ARTFieldInfo["x-velocity"]._projected_units = r"\rm{cm}/\rm{s}"

def _y_velocity(field, data):
    tr = data["YMomentumDensity"]/data["Density"]
    return tr
add_field("y-velocity", function=_y_velocity,
          units=r"\mathrm{cm/s}", take_log=False)
ARTFieldInfo["y-velocity"]._units = r"\rm{cm}/\rm{s}"
ARTFieldInfo["y-velocity"]._projected_units = r"\rm{cm}/\rm{s}"

def _z_velocity(field, data):
    tr = data["ZMomentumDensity"]/data["Density"]
    return tr
add_field("z-velocity", function=_z_velocity,
          units=r"\mathrm{cm/s}", take_log=False)
ARTFieldInfo["z-velocity"]._units = r"\rm{cm}/\rm{s}"
ARTFieldInfo["z-velocity"]._projected_units = r"\rm{cm}/\rm{s}"

def _metal_density(field, data):
    tr = data["MetalDensitySNIa"]
    tr += data["MetalDensitySNII"]
    return tr
add_field("Metal_Density", function=_metal_density,
          units=r"\mathrm{K}", take_log=True)
ARTFieldInfo["Metal_Density"]._units = r"\rm{g}/\rm{cm}^3"
ARTFieldInfo["Metal_Density"]._projected_units = r"\rm{g}/\rm{cm}^2"

# Particle fields
for f in particle_fields:
    add_art_field(f, function=NullFunc, take_log=True,
                  validators=[ValidateDataField(f)],
                  particle_type=True)
for ax in "xyz":
    add_art_field("particle_velocity_%s" % ax, function=NullFunc, take_log=True,
                  validators=[ValidateDataField(f)],
                  particle_type=True,
                  convert_function=lambda x: x.convert("particle_velocity_%s" % ax))
add_art_field("particle_mass", function=NullFunc, take_log=True,
              validators=[ValidateDataField(f)],
              particle_type=True,
              convert_function=lambda x: x.convert("particle_mass"))
add_art_field("particle_mass_initial", function=NullFunc, take_log=True,
              validators=[ValidateDataField(f)],
              particle_type=True,
              convert_function=lambda x: x.convert("particle_mass"))


def _particle_age(field, data):
    tr = data["particle_creation_time"]
    return data.pf.current_time - tr
add_field("particle_age", function=_particle_age, units=r"\mathrm{s}",
          take_log=True, particle_type=True)

def spread_ages(ages, spread=1.0e7*365*24*3600):
    # stars are formed in lumps; spread out the ages linearly
    da = np.diff(ages)
    assert np.all(da <= 0)
    # ages should always be decreasing, and ordered so
    agesd = np.zeros(ages.shape)
    idx, = np.where(da < 0)
    idx += 1  # mark the right edges
    # spread this age evenly out to the next age
    lidx = 0
    lage = 0
    for i in idx:
        n = i-lidx  # n stars affected
        rage = ages[i]
        lage = max(rage-spread, 0.0)
        agesd[lidx:i] = np.linspace(lage, rage, n)
        lidx = i
        # lage=rage
    # we didn't get the last iter
    n = agesd.shape[0]-lidx
    rage = ages[-1]
    lage = max(rage-spread, 0.0)
    agesd[lidx:] = np.linspace(lage, rage, n)
    return agesd

def _particle_age_spread(field, data):
    tr = data["particle_creation_time"]
    return spread_ages(data.pf.current_time - tr)

add_field("particle_age_spread", function=_particle_age_spread,
          particle_type=True, take_log=True, units=r"\rm{s}")

def _ParticleMassMsun(field, data):
    return data["particle_mass"]/mass_sun_cgs
add_field("ParticleMassMsun", function=_ParticleMassMsun, particle_type=True,
          take_log=True, units=r"\rm{Msun}")

# Particle Deposition Fields
ptypes = ["all", "darkmatter", "stars"]
names  = ["Particle", "Dark Matter", "Stellar"]

# Particle Mass Density Fields
for ptype, name in zip(ptypes, names):
    def particle_density(field, data):
        vol = data["CellVolume"]
        pos = np.column_stack([data[(ptype, "particle_position_%s" % ax)]
                               for ax in 'xyz'])
        pmass = data[(ptype, "particle_mass")]
        mass = data.deposit(pos, [pmass], method = "sum")
        return mass / vol
    add_field("%s_mass_density_deposit" % ptype, function=particle_density, 
              particle_type=False, take_log=True, units=r'g/cm^{3}',
              display_name="%s Density" % name, 
              validators=[ValidateSpatial()], projection_conversion='1')

# Particle Mass Fields
for ptype, name in zip(ptypes, names):
    def particle_count(field, data):
        pos = np.column_stack([data[(ptype, "particle_position_%s" % ax)]
                               for ax in 'xyz'])
        mass = data.deposit(pos, method = "sum")
        return mass
    add_field("%s_mass_deposit" % ptype, function=particle_density, 
              particle_type=False, take_log=True, units=r'1/cm^{3}',
              display_name="%s Mass Density" % name, 
              validators=[ValidateSpatial()], projection_conversion='1')

# Particle Number Density Fields
for ptype, name in zip(ptypes, names):
    def particle_count(field, data):
        vol = data["CellVolume"]
        pos = np.column_stack([data[(ptype, "particle_position_%s" % ax)]
                               for ax in 'xyz'])
        count = data.deposit(pos, method = "count")
        return count / vol
    add_field("%s_number_density_deposit" % ptype, function=particle_density, 
              particle_type=False, take_log=True, units=r'1/cm^{3}',
              display_name="%s Number Density" % name, 
              validators=[ValidateSpatial()], projection_conversion='1')

# Particle Number Fields
for ptype, name in zip(ptypes, names):
    def particle_count(field, data):
        pos = np.column_stack([data[(ptype, "particle_position_%s" % ax)]
                               for ax in 'xyz'])
        count = data.deposit(pos, method = "count")
        return count 
    add_field("%s_number_deposit" % ptype, function=particle_density, 
              particle_type=False, take_log=True, units=r'1/cm^{3}',
              display_name="%s Number" % name, 
              validators=[ValidateSpatial()], projection_conversion='1')

# Particle Velocity Fields
for ptype, name in zip(ptypes, names):
    for axis in 'xyz':
        def particle_velocity(field, data):
            pos = np.column_stack([data[(ptype, "particle_position_%s" % ax)]
                                   for ax in 'xyz'])
            vel = data[(ptype, "particle_velocity_%s" % axis)]
            vel_deposit = data.deposit(vel, method = "sum")
            return vel_deposit
        add_field("%s_velocity_%s_deposit" % (ptype, axis), 
                  function=particle_velocity, 
                  particle_type=False, take_log=False, units=r'cm/s',
                  display_name="%s Velocity %s" % (name, axis.upper()), 
                  validators=[ValidateSpatial()], projection_conversion='1')

# Particle Mass-weighted Velocity Fields
for ptype, name in zip(ptypes, names):
    for axis in 'xyz':
        def particle_velocity_weighted(field, data):
            pos = np.column_stack([data[(ptype, "particle_position_%s" % ax)]
                                   for ax in 'xyz'])
            vel  = data[(ptype, "particle_velocity_%s" % axis)]
            mass = data[(ptype, "particle_mass")]
            vel_deposit = data.deposit(vel * mass, method = "sum")
            norm = data.deposit(mass, method = "sum")
            return vel_deposit / norm
        add_field("%s_weighted_velocity_%s_deposit" % (ptype, axis), 
                  function=particle_velocity, 
                  particle_type=False, take_log=False, units=r'cm/s',
                  display_name="%s Velocity %s" % (name, axis.upper()), 
                  validators=[ValidateSpatial()], projection_conversion='1')

# Particle Mass-weighted Velocity Magnitude Fields
for ptype, name in zip(ptypes, names):
    def particle_velocity_weighted(field, data):
        pos = np.column_stack([data[(ptype, "particle_position_%s" % ax)]
                               for ax in 'xyz'])
        vels = np.column_stack([data[(ptype, "particle_position_%s" % ax)]
                               for ax in 'xyz'])
        vel = np.sqrt(np.sum(vels, axis=0))
        mass = data[(ptype, "particle_mass")]
        vel_deposit = data.deposit(vel * mass, method = "sum")
        norm = data.deposit(mass, method = "sum")
        return vel_deposit / norm
    add_field("%s_weighted_velocity_deposit" % (ptype), 
              function=particle_velocity, 
              particle_type=False, take_log=False, units=r'cm/s',
              display_name="%s Velocity" % name, 
              validators=[ValidateSpatial()], projection_conversion='1')
