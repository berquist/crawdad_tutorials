#!/usr/bin/env python2

import numpy as np
import scipy as sp
import scipy.linalg as spl

##############################################################################

# Step #1: Nuclear Repulsion Energy

# Read the nuclear repulsion energy from the enuc.dat file.

def read_vnn():
    vnn_handle = open("enuc.dat", "r")
    vnn = float(vnn_handle.read())
    print "Nuclear Repulsion Energy:", vnn
    return vnn

Vnn = read_vnn()

##############################################################################

# Step #2: One-Electron Integrals

# Read the AO-basis overlap,

# S_{\mu \nu} \equiv \int \phi_\mu({\mathbf r}) \phi_{\nu}({\mathbf r}) d{\mathbf r}

# kinetic-energy,

# T_{\mu \nu} \equiv \int \phi_\mu({\mathbf r}) \left( -\frac{1}{2} \nabla^2_{\mathbf r} \right) \phi_\nu({\mathbf r}) d{\mathbf r}

# and nuclear-attraction integrals,

# V_{\mu \nu} \equiv \int \phi_\mu({\mathbf r}) \left( -\sum_A^N \frac{Z}{r_A} \right) \phi_\nu({\mathbf r}) d{\mathbf r},

# and store them in appropriately constructed matrices. Then form the "core Hamiltonian":

# H^{\rm core}_{\mu \nu} = T_{\mu \nu} + V_{\mu \nu}.

# Note that the one-electron integrals provided include only the permutationally unique integrals, but you should store the full matrices for convenience. Note also that the AO indices on the integrals in the files start with "1" rather than "0".

def read_s_ao():
    s_ao_handle = open("s.dat", "r")
    s_ao_file = s_ao_handle.readlines()
    matsize = int(s_ao_file[-1].split()[0])
    s_ao = np.zeros(shape=(matsize, matsize))
    for line in s_ao_file:
        tmp1, tmp2, tmp3 = line.split()
        mu, nu, s_mu_nu = int(tmp1)-1, int(tmp2)-1, float(tmp3)
        s_ao[mu][nu] = s_ao[nu][mu] = s_mu_nu
    return s_ao

def read_t_ao():
    t_ao_handle = open("t.dat", "r")
    t_ao_file = t_ao_handle.readlines()
    matsize = int(t_ao_file[-1].split()[0])
    t_ao = np.zeros(shape=(matsize, matsize))
    for line in t_ao_file:
        tmp1, tmp2, tmp3 = line.split()
        mu, nu, t_mu_nu = int(tmp1)-1, int(tmp2)-1, float(tmp3)
        t_ao[mu][nu] = t_ao[nu][mu] = t_mu_nu
    return t_ao

def read_v_ao():
    v_ao_handle = open("v.dat", "r")
    v_ao_file = v_ao_handle.readlines()
    matsize = int(v_ao_file[-1].split()[0])
    v_ao = np.zeros(shape=(matsize, matsize))
    for line in v_ao_file:
        tmp1, tmp2, tmp3 = line.split()
        mu, nu, v_mu_nu = int(tmp1)-1, int(tmp2)-1, float(tmp3)
        v_ao[mu][nu] = v_ao[nu][mu] = v_mu_nu
    return v_ao

S_AO = read_s_ao()
T_AO = read_t_ao()
V_AO = read_v_ao()

print "AO Overlap Integrals:"
print S_AO
print "AO Kinetic Energy Integrals:"
print T_AO
print "AO Nuclear Attraction Integrals:"
print V_AO

H_AO_Core = T_AO + V_AO
print "AO Core Hamiltonian:"
print H_AO_Core

##############################################################################

# Step #3: Two-Electron Integrals

# Read the two-electron repulsion integrals from the eri.dat file. The integrals in this file are provided in Mulliken notation over real AO basis functions:

# (\mu \nu | \lambda \sigma) \equiv \int \phi_\mu({\mathbf r}_1) \phi_\nu({\mathbf r}_1) r_{12}^{-1} \phi_\lambda({\mathbf r}_2) \phi_\sigma({\mathbf r}_2) d{\mathbf r}_1 d{\mathbf r}_2.

# Hence, the integrals obey the eight-fold permutational symmetry relationships:

# (\mu \nu | \lambda \sigma) = (\nu \mu | \lambda \sigma) = (\mu \nu | \sigma \lambda ) = (\nu \mu | \sigma \lambda) = (\lambda \sigma | \mu \nu) = (\sigma \lambda | \mu \nu) = (\lambda \sigma | \nu \mu) = (\sigma \lambda | \nu \mu),

# and only the permutationally unique integrals are provided in the file, with the restriction that, for each integral, the following relationships hold:

# \mu \geq \nu,\ \ \ \ \ \lambda \geq \sigma,\ \ \ \ \ \ {\rm and}\ \ \ \ \ \ \mu\nu \geq \lambda\sigma,

# where

# \mu\nu \equiv \mu(\mu+1)/2 + \nu\ \ \ \ \ \ {\rm and} \ \ \ \ \ \ \lambda\sigma \equiv \lambda(\lambda+1)/2 + \sigma.

# Note that the two-electron integrals may be stored efficiently in a one-dimensional array and the above relationship used to map between given \mu, \nu, \lambda, and \sigma indices and a "compound index" defined as:

# \mu\nu\lambda\sigma \equiv \mu\nu(\mu\nu+1)/2 + \lambda\sigma.

def read_eri_ao():
    eri_ao_handle = open("eri.dat", "r")
    eri_ao_file = eri_ao_handle.readlines()
    matsize = int(eri_ao_file[-1].split()[0])
    eri_ao = np.zeros(shape=(matsize, matsize, matsize, matsize))
    for line in eri_ao_file:
        tmp1, tmp2, tmp3, tmp4, tmp5 = line.split()
        mu, nu, lam, sig, eri_val = int(tmp1)-1, int(tmp2)-1, int(tmp3)-1, int(tmp4)-1, float(tmp5)
        eri_ao[mu][nu][lam][sig] = eri_ao[mu][nu][sig][lam] = eri_ao[nu][mu][lam][sig] = eri_ao[nu][mu][sig][lam] = eri_ao[lam][sig][mu][nu] = eri_ao[lam][sig][mu][nu] = eri_ao[sig][lam][mu][nu] = eri_ao[sig][lam][nu][mu] = eri_val
    return eri_ao

ERI_AO = read_eri_ao()

print "AO Electron Repulsion Integrals:"
print ERI_AO

##############################################################################

# Step #4: Build the Orthogonalization Matrix

# Diagonalize the overlap matrix:

# {\mathbf S} {\mathbf L}_S = {\mathbf L}_S \Lambda_S,

# where {\mathbf L}_S is the matrix of eigenvectors (columns) and \Lambda_S is the diagonal matrix of corresponding eigenvalues.

# Build the symmetric orthogonalization matrix using:

# {\mathbf S}^{-1/2} \equiv {\mathbf L}_S \Lambda^{-1/2} {\mathbf {\tilde L}}_S,

# where the tilde denotes the matrix transpose.

Lam_S_AO, L_S_AO = spl.eig(S_AO, b=None, left=True, right=False)
Lam_S_AO = Lam_S_AO * np.eye(len(Lam_S_AO))

print "matrix of eigenvectors (columns):"
print L_S_AO
print "diagonal matrix of corresponding eigenvalues:"
print Lam_S_AO

Lam_sqrt_inv_AO = np.sqrt(spl.inv(Lam_S_AO))
Symm_Orthog = np.dot(L_S_AO, np.dot(Lam_sqrt_inv_AO, L_S_AO.T))

print "Symmetric Orthogonalization Matrix:"
print Symm_Orthog

##############################################################################

# Step #5: Build the (Inital) Guess Density

# Form an initial (guess) Fock matrix in the orthonormal AO basis using the core Hamiltonian as a guess:

# {\mathbf F}'_0 \equiv {\mathbf {\tilde S}}^{-1/2} {\mathbf H}^{\rm core} {\mathbf S}^{-1/2}

F_prime_0_AO = np.dot(Symm_Orthog.T, np.dot(H_AO_Core, Symm_Orthog))

print "Initial (guess) Fock Matrix:"
print F_prime_0_AO

# Diagonalize the Fock matrix:

# {\mathbf F}'_0 {\mathbf C}'_0 = {\mathbf C}'_0 \epsilon_0.

eps_0_AO, C_prime_0_AO = spl.eig(F_prime_0_AO, b=None, left=False, right=True)
eps_0_AO = eps_0_AO * np.eye(len(eps_0_AO))

print C_prime_0_AO
print eps_0_AO